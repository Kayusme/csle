import time
from typing import Tuple, List
import logging
import threading
import docker
from concurrent import futures
import grpc
import socket
from confluent_kafka import Producer
from collections import deque
import csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc
import csle_collector.docker_stats_manager.docker_stats_manager_pb2
from csle_collector.docker_stats_manager.docker_stats import DockerStats
from csle_collector.docker_stats_manager.docker_stats_util import DockerStatsUtil
import csle_collector.constants.constants as constants


class DockerStatsThread(threading.Thread):
    """
    Thread that collects performance statistics of Docker containers
    """

    def __init__(self, container_names: List[str], emulation: str, sink_ip: str,
                 stats_queue_maxsize: int,
                 time_step_len_seconds: int, sink_port: int):
        """
        Initializes the thread

        :param container_names: list of container names to monitor
        :param emulation: name of the emulation to monitor
        :param sink_ip: the ip of the Kafka server to produce stats to
        :param stats_queue_maxsize: max length of the queue before sending to Kafka
        :param time_step_len_seconds: the length of a time-step before sending stats to Kafka
        """
        threading.Thread.__init__(self)
        self.container_names = container_names
        self.emulation = emulation
        self.client_1 = docker.from_env()
        self.client2 = docker.APIClient(base_url=constants.DOCKER_STATS.UNIX_DOCKER_SOCK_URL)
        self.containers = self.client_1.containers.list()
        self.containers = list(filter(lambda x: x.name in self.container_names, self.containers))
        streams = []
        for container in self.containers:
            stream = container.stats(decode=True, stream=True)
            streams.append((stream, container))
        self.stats_queue_maxsize = stats_queue_maxsize
        self.streams = streams
        self.stats_queues = {}
        self.time_step_len_seconds = time_step_len_seconds
        self.kafka_ip = sink_ip
        self.port = sink_port
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.conf = {'bootstrap.servers': f"{self.kafka_ip}:{self.port}", 'client.id': self.hostname}
        self.producer = Producer(**self.conf)
        self.stopped = False
        logging.info(f"Producer thread starting, emulation:{self.emulation}, kafka ip: {self.kafka_ip}, "
                     f"kafka port:{self.port}, time_step_len_seconds: {self.time_step_len_seconds}")

    def run(self) -> None:
        """
        Main loop of the thread

        :return: None
        """
        start = time.time()
        while not self.stopped:
            if time.time()-start >= self.time_step_len_seconds:
                aggregated_stats, avg_stats_dict = self.compute_averages()
                ts = time.time()
                record = f"{ts},{self.ip},{aggregated_stats.cpu_percent},{aggregated_stats.mem_current}," \
                         f"{aggregated_stats.mem_total},{aggregated_stats.mem_percent},{aggregated_stats.mem_percent}," \
                         f"{aggregated_stats.blk_read},{aggregated_stats.blk_write}," \
                         f"{aggregated_stats.net_rx},{aggregated_stats.net_tx}"
                self.producer.produce(constants.LOG_SINK.DOCKER_STATS_TOPIC_NAME, record)
                self.stats_queues = {}
                start = time.time()

            for stream, container in self.streams:
                stats_dict = next(stream)
                parsed_stats = DockerStatsUtil.parse_stats(stats_dict, container.name)
                if parsed_stats.container_name not in self.stats_queues:
                    self.stats_queues[parsed_stats.container_name] = deque([], maxlen=self.stats_queue_maxsize)
                self.stats_queues[parsed_stats.container_name].append(parsed_stats)

    def compute_averages(self) -> Tuple[DockerStats, dict]:
        """
        Compute averages and aggregates of the list of metrics
        :return: the average and aggregate metrics
        """
        avg_stats = {}
        avg_stats_l = []
        for k,v in self.stats_queues.items():
            avg_stat = DockerStats.compute_averages(list(v))
            avg_stats[k] = avg_stat
            avg_stats_l.append(avg_stat)
        aggregated_stats = DockerStats.compute_averages(avg_stats_l)
        aggregated_stats.pids = float("{:.1f}".format(aggregated_stats.pids*len(avg_stats_l)))
        aggregated_stats.mem_current = float("{:.1f}".format(aggregated_stats.mem_current * len(avg_stats_l)))
        aggregated_stats.mem_total = float("{:.1f}".format(aggregated_stats.mem_total * len(avg_stats_l)))
        aggregated_stats.blk_read = float("{:.1f}".format(aggregated_stats.blk_read * len(avg_stats_l)))
        aggregated_stats.blk_write = float("{:.1f}".format(aggregated_stats.blk_write * len(avg_stats_l)))
        aggregated_stats.net_rx = float("{:.1f}".format(aggregated_stats.net_rx * len(avg_stats_l)))
        aggregated_stats.net_tx = float("{:.1f}".format(aggregated_stats.net_tx * len(avg_stats_l)))
        return aggregated_stats, avg_stats


class DockerStatsManagerServicer(csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.DockerStatsManagerServicer):
    """
    gRPC server for managing a the docker statsm monitor server.
    Allows to start/stop the docker stats monitor remotely and also to query the
    state of the server.
    """

    def __init__(self) -> None:
        """
        Initializes the server
        """
        logging.basicConfig(filename="docker_stats_manager.log", level=logging.INFO)
        self.docker_stats_monitor_threads = []
        logging.info(f"Setting up DockerStatsManager")

    def getDockerStatsMonitorStatus(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.GetDockerStatsMonitorStatusMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Gets the state of the docker stats monitors

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats manager
        """
        new_docker_stats_monitor_threads = []
        for dsmt in self.docker_stats_monitor_threads:
            if dsmt.is_alive():
                new_docker_stats_monitor_threads.append(dsmt)
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        docker_stats_monitor_dto = csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors = len(self.docker_stats_monitor_threads)
        )
        return docker_stats_monitor_dto

    def stopDockerStatsMonitor(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.StopDockerStatsMonitorMsg,
            context: grpc.ServicerContext):
        """
        Stops the docker stats monitor server

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats monitor server
        """
        logging.info(f"Stopping the docker stats monitor for emulation:{request.emulation}")

        new_docker_stats_monitor_threads = []
        for dsmt in self.docker_stats_monitor_threads:
            if dsmt.emulation == request.emulation:
                dsmt.stopped = True
            else:
                if dsmt.is_alive():
                    new_docker_stats_monitor_threads.append(dsmt)
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        return csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors = len(self.docker_stats_monitor_threads)
        )

    def startDockerStatsMonitor(
            self, request: csle_collector.docker_stats_manager.docker_stats_manager_pb2.StartDockerStatsMonitorMsg,
            context: grpc.ServicerContext) \
            -> csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO:
        """
        Starts a new docker stats monitor

        :param request: the gRPC request
        :param context: the gRPC context
        :return: a clients DTO with the state of the docker stats monitor
        """
        logging.info(f"Starting the docker stats monitor for emulation:{request.emulation}")

        # Stop any existing thread with the same name
        new_docker_stats_monitor_threads = []
        for dsmt in self.docker_stats_monitor_threads:
            if dsmt.emulation == request.emulation:
                dsmt.stopped = True
            else:
                if dsmt.is_alive():
                    new_docker_stats_monitor_threads.append(dsmt)
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads

        docker_stats_monitor_thread = DockerStatsThread(request.containers, request.emulation, request.sink_ip,
                                                        request.stats_queue_maxsize, request.time_step_len_seconds,
                                                        request.sink_port)
        docker_stats_monitor_thread.start()
        self.docker_stats_monitor_threads.append(docker_stats_monitor_thread)
        new_docker_stats_monitor_threads = []
        for dsmt in self.docker_stats_monitor_threads:
            if dsmt.is_alive():
                new_docker_stats_monitor_threads.append(dsmt)
        self.docker_stats_monitor_threads = new_docker_stats_monitor_threads
        return csle_collector.docker_stats_manager.docker_stats_manager_pb2.DockerStatsMonitorDTO(
            num_monitors = len(self.docker_stats_monitor_threads)
        )


def serve(port: int = 50051) -> None:
    """
    Starts the gRPC server for managing clients

    :param port: the port that the server will listen to
    :return: None
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    csle_collector.docker_stats_manager.docker_stats_manager_pb2_grpc.add_DockerStatsManagerServicer_to_server(
        DockerStatsManagerServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"DockerStatsManager Server Started, Listening on port: {port}")
    server.wait_for_termination()


# Program entrypoint
if __name__ == '__main__':
    serve(port=50051)
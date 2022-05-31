from typing import List, Tuple
import grpc
import time
from csle_common.dao.emulation_config.emulation_env_config import EmulationEnvConfig
import csle_common.constants.constants as constants
import csle_collector.host_manager.host_manager_pb2_grpc
import csle_collector.host_manager.host_manager_pb2
import csle_collector.host_manager.query_host_manager
from csle_common.util.emulation_util import EmulationUtil
from csle_common.logging.log import Logger


class HostManager:

    @staticmethod
    def grpc_server_on(channel) -> bool:
        """
        Utility function to test if a given gRPC channel is working or not

        :param channel: the channel to test
        :return: True if working, False if timeout
        """
        try:
            grpc.channel_ready_future(channel).result(timeout=15)
            return True
        except grpc.FutureTimeoutError:
            return False

    @staticmethod
    def _start_host_managers_if_not_running(emulation_env_config: EmulationEnvConfig) -> None:
        """
        Utility method for checking if the host manager is running and starting it if it is not running

        :param emulation_env_config: the emulation env config
        :return: None
        """
        for c in emulation_env_config.containers_config.containers:
            # Connect
            EmulationUtil.connect_admin(emulation_env_config=emulation_env_config, ip=c.get_ips()[0])

            # Check if host_manager is already running
            cmd = constants.COMMANDS.PS_AUX + " | " + constants.COMMANDS.GREP \
                  + constants.COMMANDS.SPACE_DELIM + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                    conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))

            if not constants.COMMANDS.SEARCH_HOST_MANAGER in str(o):

                Logger.__call__().get_logger().info(f"Starting host manager on node {c.get_ips()[0]}")

                # Stop old background job if running
                cmd = constants.COMMANDS.SUDO + constants.COMMANDS.SPACE_DELIM + constants.COMMANDS.PKILL + \
                      constants.COMMANDS.SPACE_DELIM \
                      + constants.TRAFFIC_COMMANDS.HOST_MANAGER_FILE_NAME
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                        conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))

                # Start the host_manager
                cmd = constants.COMMANDS.START_HOST_MANAGER.format(
                    emulation_env_config.log_sink_config.secondary_grpc_port)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd,
                                                        conn=emulation_env_config.get_connection(ip=c.get_ips()[0]))
                time.sleep(5)

    @staticmethod
    def start_host_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the HostManager on every container
        to start the Host manager and the monitor thread

        :param emulation_env_config: the emulation env config
        :return: None
        """
        HostManager._start_host_managers_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:{emulation_env_config.log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_monitor_dto = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub)
                if not host_monitor_dto.running:
                    Logger.__call__().get_logger().info(
                        f"Host monitor thread is not running on {c.get_ips()[0]}, starting it.")
                    csle_collector.host_manager.query_host_manager.start_host_monitor(
                        stub=stub, kafka_ip=emulation_env_config.log_sink_config.container.get_ips()[0],
                        kafka_port=emulation_env_config.log_sink_config.kafka_port,
                        time_step_len_seconds=emulation_env_config.log_sink_config.time_step_len_seconds)


    @staticmethod
    def stop_host_monitor_thread(emulation_env_config: EmulationEnvConfig) -> None:
        """
        A method that sends a request to the HostManager on every container to stop the monitor threads

        :param emulation_env_config: the emulation env config
        :return: None
        """
        HostManager._start_host_managers_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{emulation_env_config.log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_monitor_dto = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub)
                Logger.__call__().get_logger().info(f"Stopping the Host monitor thread on {c.get_ips()[0]}.")
                csle_collector.host_manager.query_host_manager.stop_host_monitor(stub=stub)

    @staticmethod
    def get_host_monitor_thread_status(emulation_env_config: EmulationEnvConfig) -> \
            List[Tuple[csle_collector.host_manager.host_manager_pb2.HostMonitorDTO, str]]:
        """
        A method that sends a request to the HostManager on every container to get the status of the Host monitor thread

        :param emulation_env_config: the emulation config
        :return: List of monitor thread statuses
        """
        statuses = []
        HostManager._start_host_managers_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{emulation_env_config.log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                status = csle_collector.host_manager.query_host_manager.get_host_monitor_status(stub=stub)
                statuses.append((status, c.get_ips()[0]))
        return statuses


    @staticmethod
    def get_host_log_data(emulation_env_config: EmulationEnvConfig, failed_auth_last_ts: float,
                          login_last_ts: float) \
            -> List[csle_collector.host_manager.host_manager_pb2.HostMetricsDTO]:
        """
        A method that sends a request to the HostManager on every container to get contents of the Hostmetrics
        given timestamps

        :param emulation_env_config: the emulation env config
        :param failed_auth_last_ts: the timestamp to read the last failed login attempts from
        :param login_last_ts: the timestamp to read the last successful login attempts from
        :return: List of monitor thread statuses
        """
        host_metrics_data_list = []
        HostManager._start_host_managers_if_not_running(emulation_env_config=emulation_env_config)

        for c in emulation_env_config.containers_config.containers:
            # Open a gRPC session
            with grpc.insecure_channel(
                    f'{c.get_ips()[0]}:'
                    f'{emulation_env_config.log_sink_config.secondary_grpc_port}') as channel:
                stub = csle_collector.host_manager.host_manager_pb2_grpc.HostManagerStub(channel)
                host_metrics_data = csle_collector.host_manager.query_host_manager.get_host_metrics(
                    stub=stub, failed_auth_last_ts=failed_auth_last_ts, login_last_ts=login_last_ts)
                host_metrics_data_list.append(host_metrics_data)
        return host_metrics_data_list
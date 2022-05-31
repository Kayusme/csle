"""
CSLE runner

To see options, run:
`csle --help`
"""
from typing import List, Tuple, Union
from csle_common.dao.simulation_config.simulation_env_config import SimulationEnvConfig
import click

@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
def commands() -> None:
    """
    CSLE CLI Tool
    """
    pass


def attacker_shell(s: "EmulationEnvState") -> None:
    """
    An interactive shell for executing attacker actions in an emulation environment

    :param s: the state of the emulation
    :return: None
    """
    from csle_attacker.attacker import Attacker
    done = False
    while True:
        raw_input = input("> ")
        raw_input = raw_input.strip()
        if raw_input == "help":
            print("Enter an action id to execute the action, "
                  "press R to reset,"
                  "press S to print the state, press A to print the actions, "
                  "press D to check if done"
                  "press H to print the history of actions")
        elif raw_input == "A":
            print("Attacker actions:")
            for i, a in enumerate(s.attacker_action_config.actions):
                print(f"idx:{i}, a:{a}")
        elif raw_input == "S":
            print(s)
        elif raw_input == "D":
            print(done)
        elif raw_input == "R":
            print("Resetting the state")
            s.reset()
        else:
            # try:
            attacker_action_idx = int(raw_input)
            attacker_action = s.attacker_action_config.actions[attacker_action_idx]
            s = Attacker.attacker_transition(s=s, attacker_action=attacker_action)
            # except Exception as e:
            #     print("There was an error parsing the input, please enter an integer representing an attacker action")


def attacker_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations

@click.command("attacker", help="emulation-name")
@click.argument('emulation', default="", type=str, shell_complete=attacker_shell_complete)
def attacker(emulation : str) -> None:
    """
    Opens an attacker shell in the given emulation

    :param emulation: the emulation name
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState

    emulation_env_config = MetastoreFacade.get_emulation(name=emulation)
    if emulation_env_config is not None:
        s = EmulationEnvState(emulation_env_config=emulation_env_config)
        attacker_shell(s=s)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)


def list_csle_gym_envs() -> None:
    """
    Lists the registered OpenAI gym environments

    :return: None
    """
    import gym
    import csle_common.constants.constants as constants

    click.secho(f"Registered OpenAI gym environments:", fg="magenta", bold=True)
    for env in gym.envs.registry.all():
        if constants.CSLE.NAME in env.id:
            click.secho(f"{env.id}", bold=False)


def emulation_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations + ["emulation", "--host", "--stats", "--kafka", "--clients"]

@click.option('--host', is_flag=True, help='Check the status of the Host managers')
@click.option('--stats', is_flag=True, help='Check the status of the stats manager')
@click.option('--kafka', is_flag=True, help='Check the status of the Kafka manager')
@click.option('--ids', is_flag=True, help='Check the status of the IDS manager')
@click.option('--clients', is_flag=True, help='Check the number of active clients of the emulation')
@click.argument('emulation', default="", type=str, shell_complete=emulation_shell_complete)
@click.command("em", help="emulation-name")
def em(emulation : str, clients: bool, ids: bool, kafka: bool, stats: bool, host: bool) -> None:
    """
    Extracts status information of a given emulation

    :param emulation: the emulation name
    :param clients: if true, print information about the client population
    :param ids: if true, print information about the ids manager
    :param kafka: if true, print information about the kafka manager
    :param stats: if true, print information about the statsmanager
    :param host: if true, print information about the hostmanagers
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    from csle_common.controllers.traffic_manager import TrafficManager
    from csle_common.controllers.ids_manager import IDSManager
    from csle_common.controllers.log_sink_manager import LogSinkManager
    from csle_common.controllers.host_manager import HostManager

    emulation_env_config = MetastoreFacade.get_emulation(name=emulation)
    if emulation_env_config is not None:
        if clients:
            clients_dto = TrafficManager.get_num_active_clients(emulation_env_config=emulation_env_config)
            click.secho(f"Client population status for: {emulation}", fg="magenta", bold=True)
            click.secho(f"Active clients: {clients_dto.num_clients}", bold=False)
            if clients_dto.client_process_active:
                click.secho("Client process " + f" {click.style('[active]', fg='green')}", bold=False)
            else:
                click.secho("Client process " + f" {click.style('[inactive]', fg='red')}", bold=False)
            if clients_dto.producer_active:
                click.secho("Producer process " + f" {click.style('[active]', fg='green')}", bold=False)
            else:
                click.secho("Producer process " + f" {click.style('[inactive]', fg='red')}", bold=False)
            click.secho(f"Clients time-step length: {clients_dto.clients_time_step_len_seconds} seconds", bold=False)
            click.secho(f"Producer time-step length: {clients_dto.producer_time_step_len_seconds} seconds", bold=False)
        if ids:
            ids_monitors_statuses = IDSManager.get_ids_monitor_thread_status(emulation_env_config=emulation_env_config)
            for ids_monitor_status in ids_monitors_statuses:
                click.secho(f"IDS monitor status for: {emulation}", fg="magenta", bold=True)
                if ids_monitor_status.running:
                    click.secho("IDS monitor status: " + f" {click.style('[running]', fg='green')}", bold=False)
                else:
                    click.secho("IDS monitor status: " + f" {click.style('[stopped]', fg='red')}", bold=False)
        if kafka:
            kafka_dto = LogSinkManager.get_kafka_status(emulation_env_config=emulation_env_config)
            click.secho(f"Kafka manager status for: {emulation}", fg="magenta", bold=True)
            if kafka_dto.running:
                click.secho("Kafka broker status: " + f" {click.style('[running]', fg='green')}", bold=False)
            else:
                click.secho("Kafka broker status: " + f" {click.style('[stopped]', fg='red')}", bold=False)
            click.secho(f"Topics:", bold=True)
            for topic in kafka_dto.topics:
                click.secho(f"{topic}", bold=False)
        if stats:
            stats_manager_dto = ContainerManager.get_docker_stats_manager_status(
                log_sink_config=emulation_env_config.log_sink_config)
            click.secho(f"Docker stats manager status for: {emulation}", fg="magenta", bold=True)
            click.secho(f"Number of active monitors: {stats_manager_dto.num_monitors}", bold=False)

        if host:
            click.secho(f"Host manager statuses for: {emulation}", fg="magenta", bold=True)
            host_manager_dtos = HostManager.get_host_monitor_thread_status(emulation_env_config=emulation_env_config)
            for ip_hmd in host_manager_dtos:
                hmd, ip = ip_hmd
                if not hmd.running:
                    click.secho(f"Host manager on {ip} " + f" {click.style('[stopped]', fg='red')}", bold=False)
                else:
                    click.secho(f"Host manager on {ip}: " + f" {click.style('[running]', fg='green')}", bold=False)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)

def start_traffic_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations + ["--mu", "--lamb", "--t", "--nc"]

@click.option('--nc', default=None, type=int)
@click.option('--t', default=None, type=int)
@click.option('--lamb', default=None, type=int)
@click.option('--mu', default=None, type=float)
@click.argument('emulation', default="", type=str, shell_complete=start_traffic_shell_complete)
@click.command("start_traffic", help="emulation-name")
def start_traffic(emulation : str, mu: float, lamb: float, t: int,
                  nc: int) -> None:
    """
    Starts the traffic and client population on a given emulation

    :param emulation: the emulation to start the traffic of
    :param mu: the mu parameter of the service time of the client arrivals
    :param lamb: the lambda parameter of the client arrival process
    :param t: time-step length to measure the arrival process
    :param nc: number of commands per client
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    emulation_env_config = MetastoreFacade.get_emulation(name=emulation)
    if emulation_env_config is not None:
        if mu is not None:
            emulation_env_config.traffic_config.client_population_config.mu = mu
        if lamb is not None:
            emulation_env_config.traffic_config.client_population_config.lamb = lamb
        if t is not None:
            emulation_env_config.traffic_config.client_population_config.client_time_step_len_seconds = t
        if nc is not None:
            emulation_env_config.traffic_config.client_population_config.num_commands = nc
        EmulationEnvManager.start_custom_traffic(emulation_env_config=emulation_env_config)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)


def stop_traffic_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    return emulations

@click.argument('emulation', default="", shell_complete=stop_traffic_shell_complete)
@click.command("stop_traffic", help="emulation-name")
def stop_traffic(emulation : str) -> None:
    """
    Stops the traffic and client population on a given emulation

    :param emulation: the emulation to start the traffic of
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    emulation_env_config = MetastoreFacade.get_emulation(name=emulation)
    if emulation_env_config is not None:
        EmulationEnvManager.stop_custom_traffic(emulation_env_config=emulation_env_config)
    else:
        click.secho(f"name: {emulation} not recognized", fg="red", bold=True)

def materialize_shell_complete(ctx, param, incomplete):
    return ["<emulation> <path>"]

@click.argument('path', default="")
@click.argument('emulation', default="", shell_complete=materialize_shell_complete)
@click.command("materialize", help="emulation path")
def materialize(emulation: str, path: str) -> None:
    """
    Materializes the configuraiton of a given emulation to a given path

    :param emulation: the emulation to materialize
    :param path: the path to materialize the emulation's configuration
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    emulation_env_config = MetastoreFacade.get_emulation(name=emulation)
    if emulation_env_config is None:
        click.secho(f"Emulation: {emulation} not found", fg="red", bold=True)
    else:
        if path != "":
            materialize_emulation(emulation_env_config, path=path)
        else:
            click.secho(f"No path specified", fg="red", bold=True)


def shell_shell_complete(ctx, param, incomplete):
    from csle_common.controllers.container_manager import ContainerManager
    running_containers = ContainerManager.list_all_running_containers()
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    return containers

@click.argument('container', default="", shell_complete=shell_shell_complete)
@click.command("shell", help="container-name")
def shell(container: str) -> None:
    """
    Command for opening a shell inside a running container

    :param container: the name of the container
    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    running_containers= ContainerManager.list_all_running_containers()
    container_found = False
    for rc in running_containers:
        if rc[0] == container:
            container_found = True
            break
    if container_found:
        cmd = f"docker exec -it {container} /bin/bash"
        click.secho(f"To open a shell in container:{container}, run: '{cmd}'", bold=False)
    else:
        click.secho(f"Container: {container} not found among running containers", fg="red", bold=False)

def gen_shell_complete(ctx, param, incomplete):
    return ["<name> <num_envs> <min_users> <max_users> <min_flags> <max_flags> <min_nodes> <max_flags> <min_flags> "
            "<max_users> <min_users> <num_envs> <name> <gen>"]

@click.argument('max_mem', default=4, type=int)
@click.argument('min_mem', default=4, type=int)
@click.argument('max_cpus', default=1, type=int)
@click.argument('min_cpus', default=1, type=int)
@click.argument('max_nodes', default=10, type=int)
@click.argument('min_nodes', default=4, type=int)
@click.argument('max_flags', default=5, type=int)
@click.argument('min_flags', default=1, type=int)
@click.argument('max_users', default=5, type=int)
@click.argument('min_users', default=1, type=int)
@click.argument('num_envs', default=1, type=int)
@click.argument('name', default="", type=str, shell_complete=gen_shell_complete)
@click.command("gen", help="name min_users max_users min_flags max_flags min_nodes max_nodes")
def gen(name: str, num_envs: int, min_users: int, max_users: int, min_flags: int, max_flags: int, min_nodes: int,
        max_nodes: int, min_cpus: int, max_cpus: int, min_mem: int, max_mem: int) -> None:

    from csle_common.domain_randomization.emulation_env_config_generator import EmulationEnvConfigGenerator
    from csle_common.dao.emulation_config.emulation_env_generation_config import EmulationEnvGenerationConfig
    from csle_common.util.experiment_util import ExperimentUtil
    import csle_common.constants.constants as constants

    if name == "":
        click.secho(f"Please specify a name of the emulation to generate", fg="red", bold=False)
        return

    click.secho(f"Generating a random emulation configuration with {min_nodes}-{max_nodes} nodes, "
                f"{min_users}-{max_users} users, and {min_flags}-{max_flags} flags", bold=False)
    container_env_config = EmulationEnvGenerationConfig(
        min_num_users=min_users, max_num_users=max_users, min_num_flags=min_flags,
        max_num_flags=max_flags, min_num_nodes=min_nodes, max_num_nodes=max_nodes,
        container_pool=constants.CONTAINER_POOLS.CONTAINER_POOL,
        gw_vuln_compatible_containers=constants.CONTAINER_POOLS.GW_VULN_CONTAINERS,
        pw_vuln_compatible_containers=constants.CONTAINER_POOLS.PW_VULN_CONTAINERS,
        rce_vuln_compatible_containers=constants.CONTAINER_POOLS.RCE_CONTAINERS,
        sql_injection_vuln_compatible_containers=constants.CONTAINER_POOLS.SQL_INJECTION_CONTAINERS,
        priv_esc_vuln_compatible_containers=constants.CONTAINER_POOLS.PRIV_ESC_CONTAINERS,
        agent_containers=constants.CONTAINER_POOLS.AGENT_CONTAINERS,
        router_containers=constants.CONTAINER_POOLS.ROUTER_CONTAINERS,
        path=ExperimentUtil.default_output_dir(), subnet_id_blacklist=set(),
        subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}", min_cpus=min_cpus, max_cpus=max_cpus,
        min_mem_G=min_mem, max_mem_G=max_mem
    )
    created_emulations = EmulationEnvConfigGenerator.generate_envs(container_env_config, name=name, num_envs=num_envs)
    for em in created_emulations:
        click.secho(f"Successfully created emulation with name: {em.name} and configuration:",
                    fg="green", bold=True)
        print_emulation_config(emulation_env_config=em)


def run_emulation(emulation_env_config: "EmulationEnvConfig", no_traffic: bool) -> None:
    """
    Runs an emulation with the given config

    :param emulation_env_config: the config of the emulation to run
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :return: None
    """
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    click.secho(f"Starting emulation {emulation_env_config.name}", bold=False)
    EmulationEnvManager.run_containers(emulation_env_config=emulation_env_config)
    EmulationEnvManager.apply_emulation_env_config(emulation_env_config=emulation_env_config, no_traffic=no_traffic)


def separate_running_and_stopped_emulations(emulations : List["EmulationEnvConfig"]) -> Tuple[List[str], List[str]]:
    """
    Partitions the set of emulations into a set of running emulations and a set of stopped emulations

    :param emulations: the list of emulations
    :return: running_emulations, stopped_emulations
    """
    from csle_common.controllers.container_manager import ContainerManager

    rc_emulations = ContainerManager.list_running_emulations()
    stopped_emulations = []
    running_emulations = []
    for em in emulations:
        if em.name in rc_emulations:
            running_emulations.append(em.name)
        else:
            stopped_emulations.append(em.name)
    return running_emulations, stopped_emulations


def stop_emulation(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Stops the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation to stop
    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    click.secho(f"Stopping emulation {emulation_env_config.name}", bold=False)
    EmulationEnvManager.stop_containers(emulation_env_config=emulation_env_config)
    ContainerManager.stop_docker_stats_thread(log_sink_config=emulation_env_config.log_sink_config,
                                              containers_config=emulation_env_config.containers_config,
                                              emulation_name=emulation_env_config.name)

def clean_emulation_statistics() -> None:
    """
    Deletes emulation statistics from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho(f"Deleting all emulation statistics from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.EMULATION_STATISTICS_TABLE)


def clean_emulation_traces() -> None:
    """
    Deletes emulation traces from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho(f"Deleting all emulation traces from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.EMULATION_TRACES_TABLE)


def clean_simulation_traces() -> None:
    """
    Deletes simulation traces from the metastore

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    import csle_common.constants.constants as constants

    click.secho(f"Deleting all simulation traces from the metastore", bold=False)
    MetastoreFacade.delete_all(constants.METADATA_STORE.SIMULATION_TRACES_TABLE)


def clean_emulation(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Cleans the emulation with the given configuration

    :param emulation_env_config: the configuration of the emulation
    :return: None
    """
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    click.secho(f"Cleaning emulation {emulation_env_config.name}", bold=False)
    EmulationEnvManager.clean_emulation(emulation_env_config=emulation_env_config)


def materialize_emulation(emulation_env_config: "EmulationEnvConfig", path: str) -> None:
    """
    Materializes the emulation with the given config to a given path

    :param emulation_env_config: the config of the emulation
    :param path: the path to materialize the emulation to
    :return: None
    """
    from csle_common.domain_randomization.emulation_env_config_generator import EmulationEnvConfigGenerator
    import csle_common.constants.constants as constants
    import os

    path = os.path.join(os.getcwd(), path + constants.COMMANDS.SLASH_DELIM)
    click.secho(f"Materialize emulation {emulation_env_config.name} to path:{path}{emulation_env_config.name}",
                bold=False)
    EmulationEnvConfigGenerator.materialize_emulation_env_config(emulation_env_config=emulation_env_config)


def stop_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(
        emulations=MetastoreFacade.list_emulations())
    emulations = running_emulations
    running_containers = ContainerManager.list_all_running_containers()
    containers = running_containers
    containers = list(map(lambda x: x[0], containers))
    return ["prometheus", "node_exporter", "cadvisor", "grafana", "monitor",
            "statsmanager", "all"] + emulations + containers


@click.argument('entity', default="", shell_complete=stop_shell_complete)
@click.command("stop", help="prometheus | node_exporter | cadvisor | grafana | monitor | container-name | "
                            "emulation-name | statsmanager | all")
def stop(entity: str) -> None:
    """
    Stops an entity

    :param entity: the name of the container to stop or "all"
    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController
    from csle_common.metastore.metastore_facade import MetastoreFacade

    if entity == "all":
        ContainerManager.stop_all_running_containers()
        for emulation in MetastoreFacade.list_emulations():
            stop_emulation(emulation_env_config=emulation)
    elif entity == "node_exporter":
        MonitorToolsController.stop_node_exporter()
    elif entity == "prometheus":
        MonitorToolsController.stop_prometheus()
    elif entity == "cadvisor":
        MonitorToolsController.stop_cadvisor()
    elif entity == "grafana":
        MonitorToolsController.stop_grafana()
    elif entity == "monitor":
        MonitorToolsController.stop_monitor()
    elif entity == "statsmanager":
        MonitorToolsController.stop_docker_stats_manager()
    else:
        container_stopped = ContainerManager.stop_container(name=entity)
        if not container_stopped:
            emulation = MetastoreFacade.get_emulation(name=entity)
            if emulation is not None:
                 stop_emulation(emulation)
                 emulation_stopped = True
            else:
                emulation_stopped = False
            if not emulation_stopped:
                click.secho(f"name: {entity} not recognized", fg="red", bold=True)


@click.argument('port', default=50051, type=int, shell_complete=stop_shell_complete)
@click.command("statsmanager", help="port")
def statsmanager(port: int) -> None:
    """
    Starts the statsmanager locally

    :param port: the port that the statsmanager will listen to
    :return: None
    """
    import csle_collector.docker_stats_manager.docker_stats_manager as docker_stats_manager

    docker_stats_manager.serve(port=port)


def trainingjob_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    training_jobs = MetastoreFacade.list_training_jobs()
    training_jobs_ids = list(map(lambda x: x.id, training_jobs))
    return training_jobs_ids


@click.argument('id', default=None, type=int, shell_complete=trainingjob_shell_complete)
@click.command("trainingjob", help="id")
def trainingjob(id: int) -> None:
    """
    Starts a training job with the given id

    :param id: the id of the training job to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_agents.job_controllers.training_job_manager import TrainingJobManager

    training_job = MetastoreFacade.get_training_job_config(id=id)
    TrainingJobManager.run_training_job(job_config=training_job)


def systemidentificationjob_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    sys_id_jobs = MetastoreFacade.list_system_identification_jobs()
    sys_id_jobs_ids = list(map(lambda x: x.id, sys_id_jobs))
    return sys_id_jobs_ids

@click.argument('id', default=None, type=int, shell_complete=systemidentificationjob_shell_complete)
@click.command("systemidentificationjob", help="id")
def systemidentificationjob(id: int) -> None:
    """
    Starts a system identification job with the given id

    :param id: the id of the training job to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager

    sys_id_job = MetastoreFacade.get_data_collection_job_config(id=id)
    DataCollectionJobManager.run_data_collection_job(job_config=sys_id_job)


def start_docker_stats_manager() -> None:
    """
    Starts the stats manager as a daemon

    :return: None
    """
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    port = 50051
    started = MonitorToolsController.start_docker_stats_manager(port=port)
    if started:
        click.secho(f"Starting docker stats manager on port:{port}", bold=False)
    else:
        click.secho(f"Docker stats manager is already running on port:{port}", bold=False)


def start_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(
        emulations=MetastoreFacade.list_emulations())
    emulations = stopped_emulations
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names=ContainerManager.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return ["prometheus", "node_exporter", "grafana", "cadvisor", "monitor",
            "all",
            "statsmanager", "training_job", "system_id_job", "monitor", "--id", "--no_traffic"] + emulations + \
           containers + image_names


@click.option('--id', default=None, type=int)
@click.option('--no_traffic', is_flag=True, help='skip starting the traffic generators')
@click.argument('name', default="", type=str)
@click.argument('entity', default="", type=str, shell_complete=start_shell_complete)
@click.command("start", help="prometheus | node_exporter | grafana | cadvisor | monitor | "
                             "container-name | emulation-name | all | statsmanager | training_job "
                             "| system_id_job")
def start(entity : str, no_traffic: bool, name: str, id: int) -> None:
    """
    Starts a container or all containers

    :param entity: the container or emulation to start or "all"
    :param name: extra parameter for running a Docker image
    :param no_traffic: a boolean parameter that is True if the traffic generators should be skipped
    :param id: (optional) an id parameter to identify the entity to start
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController
    from csle_agents.job_controllers.training_job_manager import TrainingJobManager
    from csle_system_identification.job_controllers.data_collection_job_manager import DataCollectionJobManager

    if entity == "all":
        ContainerManager.start_all_stopped_containers()
    elif entity == "statsmanager":
        start_docker_stats_manager()
    elif entity == "node_exporter":
         MonitorToolsController.start_node_exporter()
    elif entity == "prometheus":
        MonitorToolsController.start_prometheus()
    elif entity == "cadvisor":
        MonitorToolsController.start_cadvisor()
    elif entity == "grafana":
        MonitorToolsController.start_grafana()
    elif entity == "training_job":
        training_job = MetastoreFacade.get_training_job_config(id=id)
        TrainingJobManager.start_training_job_in_background(training_job=training_job)
    elif entity == "system_id_job":
        system_id_job = MetastoreFacade.get_data_collection_job_config(id=id)
        DataCollectionJobManager.start_data_collection_job_in_background(
            data_collection_job=system_id_job)
    elif entity == "monitor":
        MonitorToolsController.start_monitor()
    else:
        container_started = ContainerManager.start_container(name=entity)
        if not container_started:
            emulation_env_config = MetastoreFacade.get_emulation(name=entity)
            if emulation_env_config is not None:
                run_emulation(emulation_env_config, no_traffic=no_traffic)
                emulation_started = True
            else:
                emulation_started =False
            if not emulation_started:
                image_started = run_image(image=entity, name=name)
                if not image_started:
                    click.secho(f"name: {entity} not recognized", fg="red", bold=True)


def run_image(image: str, name: str) -> bool:
    """
    Runs a container with a given image

    :param image: the image of the container
    :param name: the name that the container will be assigned
    :return: True if it was started successfully, False otherwise
    """
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    try:
        EmulationEnvManager.run_container(image=image, name=name)
        return True
    except Exception as e:
        return False


def rm_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    running_containers = ContainerManager.list_all_running_containers()
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names=ContainerManager.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return ["network-name", "container-name", "image-name", "networks", "images", "containers"] + emulations + \
           containers + image_names


@click.argument('entity', default="", shell_complete=rm_shell_complete)
@click.command("rm", help="network-name | container-name | image-name | networks | images | containers")
def rm(entity : str) -> None:
    """
    Removes a container, a network, an image, all networks, all images, or all containers

    :param entity: the container(s), network(s), or images(s) to remove
    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    if entity == "containers":
        ContainerManager.rm_all_stopped_containers()
    elif entity == "images":
        ContainerManager.rm_all_images()
    elif entity == "networks":
        ContainerManager.rm_all_networks()
    else:
        rm_name(name=entity)


def clean_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    running_containers = ContainerManager.list_all_running_containers()
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    return ["all", "containers", "emulations", "emulation_traces", "simulation_traces", "emulation_statistics",
            "name"] + emulations + containers


@click.argument('entity', default="", shell_complete=clean_shell_complete)
@click.command("clean", help="all | containers | emulations | emulation_traces | simulation_traces "
                             "| emulation_statistics | name")
def clean(entity : str) -> None:
    """
    Removes a container, a network, an image, all networks, all images, all containers, all traces, or all statistics

    :param entity: the container(s), network(s), or images(s) to remove
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager

    if entity == "all":
        ContainerManager.stop_all_running_containers()
        ContainerManager.rm_all_stopped_containers()
        for emulation in MetastoreFacade.list_emulations():
            clean_emulation(emulation_env_config=emulation)
    elif entity == "containers":
        ContainerManager.stop_all_running_containers()
        ContainerManager.rm_all_stopped_containers()
    elif entity == "emulations":
        for emulation in MetastoreFacade.list_emulations():
            clean_emulation(emulation_env_config=emulation)
    elif entity == "emulation_traces":
        clean_emulation_traces()
    elif entity == "simulation_traces":
        clean_simulation_traces()
    elif entity == "emulation_statistics":
        clean_emulation_statistics()
    else:
        clean_name(name=entity)


def install_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    image_names=ContainerManager.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return ["emulations", "simulations", "derived_images",
            "base_images", "metastore", "all"] + emulations + image_names + simulations


@click.argument('entity', default="", shell_complete=install_shell_complete)
@click.command("install", help="emulations | simulations | <emulation_name> | <simulation_name> | derived_images | "
                               "base_images | metastore | all")
def install(entity : str) -> None:
    """
    Installs emulations and simulations in the metastore and creates Docker images

    :param entity: entity to install
    :return: None
    """
    from csle_common.controllers.installation_controller import InstallationController

    if entity == "emulations":
        click.secho(f"Installing emulations in the metastore", bold=False)
        InstallationController.install_all_emulations()
    elif entity == "simulations":
        click.secho(f"Installing simulations in the metastore", bold=False)
        InstallationController.install_all_simulations()
    elif entity == "derived_images":
        click.secho(f"Installing derived Docker images", bold=False)
        InstallationController.install_derived_images()
    elif entity == "base_images":
        click.secho(f"Installing base Docker images", bold=False)
        InstallationController.install_base_images()
    elif entity == "metastore":
        click.secho(f"Installing metastore", bold=False)
        InstallationController.install_metastore()
    elif entity == "all":
        click.secho(f"Installing base Docker images", bold=False)
        InstallationController.install_base_images()
        click.secho(f"Installing derived Docker images", bold=False)
        InstallationController.install_derived_images()
        click.secho(f"Installing emulations in the metastore", bold=False)
        InstallationController.install_all_emulations()
        click.secho(f"Installing simulations in the metastore", bold=False)
        InstallationController.install_all_simulations()
    else:
        click.secho(f"Installing {entity}", bold=False)
        InstallationController.install_emulation(emulation_name=entity)
        InstallationController.install_simulation(simulation_name=entity)
        InstallationController.install_derived_image(image_name=entity)
        InstallationController.install_base_image(image_name=entity)


def uninstall_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    image_names=ContainerManager.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    return ["emulations", "simulations", "derived_images", "base_images",
            "metastore", "all"] + emulations + image_names + simulations


@click.argument('entity', default="", shell_complete=uninstall_shell_complete)
@click.command("uninstall", help="emulations | simulations | <emulation_name> | <simulation_name> | derived_images | "
                               "base_images | metastore | all")
def uninstall(entity : str) -> None:
    """
    Uninstall emulations and simulations from the metastore and removes Docker images

    :param entity: the entity to uninstall
    :return: None
    """
    from csle_common.controllers.installation_controller import InstallationController

    if entity == "emulations":
        click.secho(f"Uninstalling emulations in the metastore", bold=False)
        InstallationController.uninstall_all_emulations()
    elif entity == "simulations":
        click.secho(f"Uninstalling simulations in the metastore", bold=False)
        InstallationController.uninstall_all_simulations()
    elif entity == "derived_images":
        click.secho(f"Uninstalling derived Docker images", bold=False)
        InstallationController.uninstall_derived_images()
    elif entity == "base_images":
        click.secho(f"Uninstalling base Docker images", bold=False)
        InstallationController.uninstall_base_images()
    elif entity == "metastore":
        click.secho(f"Uninstalling metastore", bold=False)
        InstallationController.uninstall_metastore()
    elif entity == "all":
        click.secho(f"Uninstalling simulations in the metastore", bold=False)
        InstallationController.uninstall_all_simulations()
        click.secho(f"Uninstalling emulations in the metastore", bold=False)
        InstallationController.uninstall_all_emulations()
        click.secho(f"Uninstalling derived Docker images", bold=False)
        InstallationController.uninstall_derived_images()
        click.secho(f"Uninstalling base Docker images", bold=False)
        InstallationController.uninstall_base_images()
        click.secho(f"Uninstalling metastore", bold=False)
        InstallationController.uninstall_metastore()
    else:
        click.secho(f"Uninstalling {entity}", bold=False)
        InstallationController.uninstall_emulation(emulation_name=entity)
        InstallationController.uninstall_simulation(simulation_name=entity)
        InstallationController.uninstall_derived_image(image_name=entity)
        InstallationController.uninstall_base_image(image_name=entity)


def ls_shell_complete(ctx, param, incomplete):
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    emulations = list(map(lambda x: x.name, MetastoreFacade.list_emulations()))
    simulations = list(map(lambda x: x.name, MetastoreFacade.list_simulations()))
    running_containers = ContainerManager.list_all_running_containers()
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    containers = list(map(lambda x: x[0], containers))
    image_names=ContainerManager.list_all_images()
    image_names = list(map(lambda x: x[0], image_names))
    active_networks_names = ContainerManager.list_all_networks()
    return ["containers", "networks", "images", "emulations", "all", "environments", "prometheus", "node_exporter",
            "cadvisor", "monitor", "statsmanager", "--all", "--running", "--stopped"] + emulations + containers \
           + image_names + active_networks_names + simulations


@click.command("ls", help="containers | networks | images | emulations | all | environments | prometheus | node_exporter "
                    "| cadvisor | statsmanager | monitor | simulations")
@click.argument('entity', default='all', type=str, shell_complete=ls_shell_complete)
@click.option('--all', is_flag=True, help='list all')
@click.option('--running', is_flag=True, help='list running only (default)')
@click.option('--stopped', is_flag=True, help='list stopped only')
def ls(entity :str, all: bool, running: bool, stopped: bool) -> None:
    """
    Lists the set of containers, networks, images, or emulations, or all

    :param entity: either containers, networks, images, emulations, or all
    :param all: flag that indicates whether all containers/emulations should be listed
    :param running: flag that indicates whether running containers/emulations should be listed (default)
    :param stopped: flag that indicates whether stopped containers/emulations should be listed
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager

    if entity == "all":
        list_all(all=all, running=running, stopped=stopped)
    elif entity == "networks":
        list_networks()
    elif entity == "containers":
        if all:
            list_all_containers()
        elif stopped:
            list_stopped_containers()
        else:
            list_running_containers()
    elif entity == "images":
        list_images()
    elif entity == "emulations":
        list_emulations(all=all, stopped=stopped)
    elif entity == "environments":
        list_csle_gym_envs()
    elif entity == "prometheus":
        list_prometheus()
    elif entity == "node_exporter":
        list_node_exporter()
    elif entity == "cadvisor":
        list_cadvisor()
    elif entity == "grafana":
        list_grafana()
    elif entity == "monitor":
        list_monitor()
    elif entity == "statsmanager":
        list_statsmanager()
    elif entity == "simulations":
        list_simulations()
    else:
        container = get_running_container(name=entity)
        if container is not None:
            print_running_container(container=container)
        else:
            container = get_stopped_container(name=entity)
            if container is not None:
                print_stopped_container(container=container)
            else:
                emulation_env_config = MetastoreFacade.get_emulation(name=entity)
                if emulation_env_config is not None:
                    print_emulation_config(emulation_env_config=emulation_env_config)
                else:
                    net = get_network(name=entity)
                    if net is not None:
                        active_networks_names = ContainerManager.list_all_networks()
                        active = net.name in active_networks_names
                        print_network(net=net, active=active)
                    else:
                        img = get_image(name=entity)
                        if img is not None:
                            print_img(img=img)
                        else:
                            simulation_env_config = MetastoreFacade.get_simulation(name=entity)
                            if simulation_env_config is not None:
                                print_simulation_config(simulation_config=simulation_env_config)
                            else:
                                click.secho(f"entity: {entity} is not recognized", fg="red", bold=True)


def print_running_container(container) -> None:
    """
    Utility function for printing information about a running container

    :param container: the container to print
    :return: None
    """
    click.secho(container[0] + f" image:{container[1]}, ip: {container[2]} {click.style('[running]', fg='green')}",
                bold=False)


def print_stopped_container(container) -> None:
    """
    Utiltiy function for printing information about a stopped container

    :param container: the stopped container to print
    :return: None
    """
    click.secho(container[0] + f" image:{container[1]}, ip: {container[2]} {click.style('[stopped]', fg='red')}",
                bold=False)


def print_network(net: "ContainerNetwork", active: bool = False) -> None:
    """
    Utility function for printing a given network

    :param net: the network to print
    :param active: boolean flag whether the network is active or not
    :return: None
    """
    if active:
        click.secho(f"name:{net.name}, subnet_mask:{net.subnet_mask}, subnet_prefix:{net.subnet_prefix} "
                    f"{click.style('[active]', fg='green')}", bold=False)
    else:
        click.secho(f"name:{net.name}, subnet_mask:{net.subnet_mask}, subnet_prefix:{net.subnet_prefix} "
                    f"{click.style('[inactive]', fg='red')}", bold=False)


def print_img(img: Tuple[str, str, str, str, str]) -> None:
    """
    Utility function for printing a given Docker image

    :param img: the image to print
    :return: None
    """
    click.secho(f"name:{img[0]}, size:{img[4]}B", bold=False)


def list_all(all: bool = False, running : bool = True, stopped: bool = False) -> None:
    """
    Lists all containers, images, networks, and emulations

    :param all: boolean flag whether all containers/emulations should be listed
    :param running: boolean flag whether running containers/emulations should be listed (default)
    :param stopped: boolean flag whether stopped containers/emulations should be listed
    :return: None
    """
    list_networks()
    list_all_containers()
    list_images()
    list_emulations(all=all, stopped=stopped, running=running)
    list_simulations()
    list_csle_gym_envs()
    click.secho("CSLE Monitoring System:", fg="magenta", bold=True)
    list_prometheus()
    list_node_exporter()
    list_cadvisor()
    list_grafana()
    list_statsmanager()
    list_monitor()


def list_statsmanager() -> None:
    """
    List status of the docker host manager

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_statsmanager_running():
        emulations = MetastoreFacade.list_emulations()
        running_emulations, stopped_emulations = separate_running_and_stopped_emulations(emulations=emulations)
        docker_stats_monitor_status = None
        for em in emulations:
            if em.name in running_emulations:
                docker_stats_monitor_status = ContainerManager.get_docker_stats_manager_status(
                    log_sink_config=em.log_sink_config)
                break
        active_monitor_threads = 0
        active_emulations = []
        if docker_stats_monitor_status is not None:
            active_monitor_threads = docker_stats_monitor_status.num_monitors
            active_emulations = docker_stats_monitor_status.emulations
        click.secho("Docker statsmanager status: " + f" {click.style('[running], ', fg='green')} "
                                                     f"port:{50051}, num active monitor threads: "
                                                     f"{active_monitor_threads}, "
                                                     f"active emulations: {','.join(active_emulations)}", bold=False)
    else:
        click.secho("Docker statsmanager status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_grafana() -> None:
    """
    List status of grafana

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_grafana_running():
        click.secho("Grafana status: " + f" {click.style('[running]', fg='green')} "
                                         f"port:{constants.COMMANDS.GRAFANA_PORT}", bold=False)
    else:
        click.secho("Grafana status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_monitor() -> None:
    """
    List status of monitor

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_monitor_running():
        click.secho("Monitor status: " + f" {click.style('[running]', fg='green')} "
                                         f"port:{constants.COMMANDS.MONITOR_PORT}", bold=False)
    else:
        click.secho("Monitor status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_cadvisor() -> None:
    """
    Lists status of cadvisor

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_cadvisor_running():
        click.secho("Cadvisor status: " + f" {click.style('[running]', fg='green')} "
                                          f"port:{constants.COMMANDS.CADVISOR_PORT}", bold=False)
    else:
        click.secho("Cadvisor status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_node_exporter() -> None:
    """
    Lists status of node exporter

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_node_exporter_running():
        click.secho("Node exporter status: " + f" {click.style('[running]', fg='green')} "
                                               f"port:{constants.COMMANDS.NODE_EXPORTER_PORT}", bold=False)
    else:
        click.secho("Node exporter status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_prometheus() -> None:
    """
    Lists status of prometheus

    :return: None
    """
    import csle_common.constants.constants as constants
    from csle_common.controllers.monitor_tools_controller import MonitorToolsController

    if MonitorToolsController.is_prometheus_running():
        click.secho("Prometheus status: " + f" {click.style('[running]', fg='green')} "
                                            f"port:{constants.COMMANDS.PROMETHEUS_PORT}", bold=False)
    else:
        click.secho("Prometheus status: " + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_emulations(all: bool = False, stopped: bool = False, running: bool = True) -> None:
    """
    Lists emulations

    :param all: boolean flag whether all emulations should be listed
    :param stopped: boolean flag whether stopped emulations should be listed
    :param running: boolean flag whether running containers should be listed
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE emulations:", fg="magenta", bold=True)
    emulations = MetastoreFacade.list_emulations()
    running_emulations, stopped_emulations = separate_running_and_stopped_emulations(emulations=emulations)
    if all or not stopped:
        for em in running_emulations:
            click.secho(em + f" {click.style('[running]', fg='green')}", bold=False)
    if all or stopped:
        for em in stopped_emulations:
            click.secho(em + f" {click.style('[stopped]', fg='red')}", bold=False)


def list_simulations() -> None:
    """
    Lists simulations

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade

    click.secho("CSLE simulations:", fg="magenta", bold=True)
    simulations = MetastoreFacade.list_simulations()
    for sim in simulations:
        click.secho(sim.name)

def list_networks() -> None:
    """
    Lists networks

    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager

    click.secho("CSLE networks:", fg="magenta", bold=True)
    active_networks_names = ContainerManager.list_all_networks()
    emulations = MetastoreFacade.list_emulations()
    for em in emulations:
        for net in em.containers_config.networks:
            active = net.name in active_networks_names
            if active:
                print_network(net, active=active)


def get_network(name: str) -> Union[None, "ContainerNetwork"]:
    """
    Utility function for getting a given network

    :param name: the name of the network to get
    :return: None if the network was not found and otherwise returns the network
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager

    active_networks_names = ContainerManager.list_all_networks()
    emulations = MetastoreFacade.list_emulations()
    for em in emulations:
        for net in em.containers_config.networks:
            if net.name == name and net.name in active_networks_names:
                return net
    return None


def get_running_container(name: str) -> Union[None, Tuple[str, str, str]]:
    """
    Utility function for getting a running container with a given name

    :param name: the name of the container to get
    :return: None if the container was not found and otherwise returns the container
    """
    from csle_common.controllers.container_manager import ContainerManager

    running_containers = ContainerManager.list_all_running_containers()
    for c in running_containers:
        if name == c[0]:
            return c
    return None


def get_stopped_container(name: str) -> Union[None, Tuple[str, str, str]]:
    """
    Utility function for stopping a given container

    :param name: the name of the container to stop
    :return: None if the container was not found and true otherwise
    """
    from csle_common.controllers.container_manager import ContainerManager

    stopped_containers = ContainerManager.list_all_stopped_containers()
    for c in stopped_containers:
        if name == c[0]:
            return c
    return None


def list_all_containers() -> None:
    """
    Lists all containers, both running and stopped

    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    click.secho("CSLE Docker containers:", fg="magenta", bold=True)
    running_containers = ContainerManager.list_all_running_containers()
    stopped_containers = ContainerManager.list_all_stopped_containers()
    containers = running_containers + stopped_containers
    for c in containers:
        if c in running_containers:
            print_running_container(c)
        else:
            print_stopped_container(c)


def list_running_containers() -> None:
    """
    Lists only running containers

    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    click.secho("CSLE running Docker containers:", fg="magenta", bold=True)
    containers = ContainerManager.list_all_running_containers()
    for c in containers:
        print_running_container(c)


def list_stopped_containers() -> None:
    """
    Lists stopped containers

    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    click.secho("CSLE stopped Docker containers:", fg="magenta", bold=True)
    containers = ContainerManager.list_all_stopped_containers()
    for c in containers:
        print_stopped_container(c)


def list_images() -> None:
    """
    Lists images

    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    click.secho("CSLE Docker images:", fg="magenta", bold=True)
    image_names=ContainerManager.list_all_images()
    for img in image_names:
        print_img(img)


def get_image(name: str) -> Union[None, Tuple[str,str,str,str,str]]:
    """
    Utility function for getting metadata of a docker image
    :param name: the name of the image to get
    :return: None or the image if it was found
    """
    from csle_common.controllers.container_manager import ContainerManager

    image_names=ContainerManager.list_all_images()
    for img in image_names:
        if img == name:
            return img
    return None


def rm_name(name: str) -> None:
    """
    Removes a given container or image or network or emulation

    :param name: the name of the image, network, or container to remove
    :return: None
    """
    from csle_common.controllers.container_manager import ContainerManager

    container_removed = ContainerManager.rm_container(name)
    if not container_removed:
        network_removed = ContainerManager.rm_network(name)
        if not network_removed:
            image_removed = ContainerManager.rm_image(name)
            if not image_removed:
                emulation_removed = remove_emulation(name=name)
                if not emulation_removed:
                    click.secho(f"name: {name} not recognized", fg="red", bold=True)


def clean_name(name: str) -> None:
    """
    Cleans a given container or emulation

    :param name: the name of the container or emulation to clean
    :return: None
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.container_manager import ContainerManager

    container_stopped = ContainerManager.stop_container(name=name)
    if container_stopped:
        ContainerManager.rm_container(container_name=name)
    else:
        em = MetastoreFacade.get_emulation(name=name)
        if em is not None:
            clean_emulation(emulation_env_config=em)
        else:
            click.secho(f"name: {name} not recognized", fg="red", bold=True)


def remove_emulation(name: str) -> bool:
    """
    Utility function for removing (uninstalling) an emulation

    :param name: the name of the emulation to remove
    :return: True if the emulation was removed, false otherwise
    """
    from csle_common.metastore.metastore_facade import MetastoreFacade
    from csle_common.controllers.emulation_env_manager import EmulationEnvManager

    click.secho(f"Removing emulation {name}", bold=False)
    emulations = MetastoreFacade.list_emulations()
    for emulation in emulations:
        if emulation.name == name:
            clean_emulation(emulation)
            EmulationEnvManager.uninstall_emulation(config=emulation)
            return True
    return False


def print_emulation_config(emulation_env_config: "EmulationEnvConfig") -> None:
    """
    Prints the configuration of a given emulation

    :param emulation_env_config: the configuration to print
    :return: None
    """
    import csle_common.constants.constants as constants

    click.secho(f"Emulation name: {emulation_env_config.name}", fg="yellow", bold=True)
    click.secho(f"Containers:", fg="yellow", bold=True)
    for c in emulation_env_config.containers_config.containers:
        click.secho(f"{c.name} {','.join(c.get_ips())}", bold=False)
    click.secho(f"Admin login:", fg="yellow", bold=True)
    click.secho(f"Username:{constants.CSLE_ADMIN.USER}", bold=False)
    click.secho(f"Password:{constants.CSLE_ADMIN.PW}", bold=False)
    click.secho(f"Vulnerabilities:", fg="yellow", bold=True)
    for vuln in emulation_env_config.vuln_config.node_vulnerability_configs:
        click.secho(f"{vuln.vuln_type} {vuln.ip}", bold=False)
        click.secho(f"{type(vuln.vuln_type)}", bold=False)
    click.secho(f"Resource constraints:", fg="yellow", bold=True)
    if emulation_env_config.resources_config is not None:
        for rc in emulation_env_config.resources_config.node_resources_configurations:
            network_bandwidth = ""
            for i, ip_net in enumerate(rc.ips_and_network_configs):
                ip,net = ip_net
                interface = net.interface
                bandwidth=net.rate_limit_mbit
                if i > 0:
                    network_bandwidth = network_bandwidth + ", "
                network_bandwidth = network_bandwidth + f"{interface} {bandwidth}Mbit/s"
            click.secho(f"{rc.container_name}: CPUs:{rc.num_cpus}, memory: {rc.available_memory_gb}GB, "
                        f"network:{network_bandwidth}", bold=False)
    click.secho(f"Flags:", fg="yellow", bold=True)
    for flag in emulation_env_config.flags_config.node_flag_configs:
        click.secho(f"{flag.flags[0][0]} {flag.ip}", bold=False)
    click.secho(f"Users:", fg="yellow", bold=True)
    for user in emulation_env_config.users_config.users_configs:
        users = ",".join(list(map(lambda x: x[0], user.users)))
        click.secho(f"{users} {user.ip}", bold=False)
    click.secho(f"Log sink configuration:", fg="yellow", bold=True)
    click.secho(f"{emulation_env_config.log_sink_config.container.name} "
                f"{','.join(emulation_env_config.log_sink_config.container.get_ips())}", bold=False)
    click.secho(f"{emulation_env_config.log_sink_config.resources.container_name}: "
                f"CPUs:{emulation_env_config.log_sink_config.resources.num_cpus}, "
                f"memory: {emulation_env_config.log_sink_config.resources.available_memory_gb}GB", bold=False)


def print_simulation_config(simulation_config: SimulationEnvConfig) -> None:
    """
    Prints the configuration of a given emulation

    :param emulation_env_config: the configuration to print
    :return: None
    """

    click.secho(f"Simulation name: {simulation_config.name}", fg="yellow", bold=True)
    click.secho(f"Description:", fg="yellow", bold=True)
    click.secho(simulation_config.descr)
    click.secho(f"Gym env name: {simulation_config.gym_env_name}", fg="yellow", bold=True)
    click.secho(f"Num players: {len(simulation_config.players_config.player_configs)}", fg="yellow", bold=True)
    click.secho(f"Num states: {len(simulation_config.state_space_config.states)}", fg="yellow", bold=True)
    click.secho(f"Num observations: {len(simulation_config.observation_function_config.observation_tensor)}",
                fg="yellow", bold=True)


# Adds the commands to the group
commands.add_command(ls)
commands.add_command(rm)
commands.add_command(stop)
commands.add_command(start)
commands.add_command(materialize)
commands.add_command(shell)
commands.add_command(gen)
commands.add_command(clean)
commands.add_command(start_traffic)
commands.add_command(stop_traffic)
commands.add_command(statsmanager)
commands.add_command(em)
commands.add_command(attacker)
commands.add_command(trainingjob)
commands.add_command(systemidentificationjob)
commands.add_command(install)
commands.add_command(uninstall)


# # Script entrypoint
# if __name__ == '__main__':
#     commands()
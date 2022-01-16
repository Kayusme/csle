import os
from csle_common.dao.container_config.containers_config import ContainersConfig
from csle_common.dao.container_config.node_container_config import NodeContainerConfig
from csle_common.envs_model.config.generator.container_generator import ContainerGenerator
from csle_common.util.experiments_util import util

def default_containers_config() -> ContainersConfig:
    """
    :return: the ContainersConfig of the emulation
    """
    containers = [
        NodeContainerConfig(name="client_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.254"),
        NodeContainerConfig(name="ftp_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6", ip="172.18.6.79"),
        NodeContainerConfig(name="hacker_kali_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.191"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.21"),
        NodeContainerConfig(name="router_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.10"),
        NodeContainerConfig(name="ssh_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.2"),
        NodeContainerConfig(name="telnet_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.3"),
        NodeContainerConfig(name="ftp_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.7"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.101"),
        NodeContainerConfig(name="ssh_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.54"),
        NodeContainerConfig(name="ssh_3", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.74"),
        NodeContainerConfig(name="telnet_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.61"),
        NodeContainerConfig(name="telnet_3", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.62"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.4"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.5"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.6"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.8"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.9"),
        NodeContainerConfig(name="honeypot_1", network="csle_internal_net_3", minigame="ctf", version="0.0.1", level="3",
                            ip="172.18.6.178"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.11"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.13"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.14"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.15"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.16"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.17"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.18"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.19"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.22"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.23"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.24"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.25"),
        NodeContainerConfig(name="honeypot_2", network="csle_internal_net_6", minigame="ctf", version="0.0.1", level="6",
                            ip="172.18.6.28")
    ]
    containers_cfg = ContainersConfig(containers=containers, network="csle_internal_net_6", agent_ip="172.18.6.191",
                                      router_ip="172.18.6.10", subnet_mask="172.18.6.0/24", subnet_prefix="172.18.6.",
                                      ids_enabled=True)
    return containers_cfg

# Generates the containers.json configuration file
if __name__ == '__main__':
    if os.path.exists(util.default_containers_path(out_dir=util.default_output_dir())):
        os.remove(util.default_containers_path(out_dir=util.default_output_dir()))
    containers_cfg = default_containers_config()
    ContainerGenerator.write_containers_config(containers_cfg, path=util.default_output_dir())
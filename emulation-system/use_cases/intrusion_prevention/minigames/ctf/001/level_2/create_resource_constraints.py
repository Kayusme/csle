import os
from csle_common.dao.container_config.resources_config import ResourcesConfig
from csle_common.dao.container_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.container_config.node_network_config import NodeNetworkConfig
from csle_common.dao.container_config.packet_loss_type import PacketLossType
from csle_common.dao.container_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.resource_constraints_generator import ResourceConstraintsGenerator
import csle_common.constants.constants as constants


def default_resource_constraints(network_id: int = 2) -> ResourcesConfig:
    """
    :param network_id: the network id
    :return: generates the ResourcesConfig
    """
    node_resources_configurations = [
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.254",
                            container_name="csle-ctf-client_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=2,
                                packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                                loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=100, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                            container_name="csle-ctf-ftp_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                            container_name="csle-ctf-hacker_kali_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=2,
                                packet_delay_jitter_ms=0.5, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.02, loss_gemodel_r=0.97,
                                loss_gemodel_k=0.98, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.02,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=2,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=100, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),        
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.21",
                            container_name="csle-ctf-honeypot_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.10",
                            container_name="csle-ctf-router_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                            container_name="csle-ctf-ssh_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                            container_name="csle-ctf-telnet_1_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                            container_name="csle-ctf-ftp_2_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.101",
                            container_name="csle-ctf-honeypot_2_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                            container_name="csle-ctf-ssh_2_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.74",
                            container_name="csle-ctf-ssh_3_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                            container_name="csle-ctf-telnet_2_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            )),
        NodeResourcesConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.62",
                            container_name="csle-ctf-telnet_3_1-level2",
                            num_cpus = 1, available_memory_gb = 4,
                            network_config=NodeNetworkConfig(
                                interface=constants.NETWORKING.ETH0,
                                limit_packets_queue=30000, packet_delay_ms=0.1,
                                packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
                                packet_delay_distribution=PacketDelayDistributionType.PARETO,
                                packet_loss_type=PacketLossType.GEMODEL,
                                loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
                                loss_gemodel_k=0.9999, loss_gemodel_h=0.0001, packet_corrupt_percentage=0.00001,
                                packet_corrupt_correlation_percentage=25, packet_duplicate_percentage=0.00001,
                                packet_duplicate_correlation_percentage=25, packet_reorder_percentage=0.0025,
                                packet_reorder_correlation_percentage=25, packet_reorder_gap=5,
                                rate_limit_mbit=1000, packet_overhead_bytes=0,
                                cell_overhead_bytes=0
                            ))
    ]
    resources_config = ResourcesConfig(node_resources_configurations=node_resources_configurations)
    return resources_config


# Generates the resources.json configuration file
if __name__ == '__main__':
    network_id = 2
    if not os.path.exists(util.default_resources_path()):
        ResourceConstraintsGenerator.write_resources_config(
            resources_config=default_resource_constraints(network_id=network_id))
    resources_config = util.read_resources_config(util.default_resources_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.csle_ADMIN.USER,
                                       agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    ResourceConstraintsGenerator.apply_resource_constraints(resources_config=resources_config,
                                                            emulation_config=emulation_config)
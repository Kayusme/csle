import os
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
import csle_common.constants.constants as constants


def default_topology() -> Topology:
    """
    :return: the Topology of the emulation
    """
    node_1 = NodeFirewallConfig(ip="172.18.5.10", hostname="router_1_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                  "172.18.5.191", "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                    "172.18.5.191", "172.18.5.1", "172.18.5.254"]),
                                output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_2 = NodeFirewallConfig(ip="172.18.5.2", hostname="ssh_1_1",
                                output_accept=set(
                                    ["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254", "172.18.5.54"]),
                                input_accept=set(
                                    ["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254", "172.18.5.54"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set([("172.18.5.7", "172.18.5.3"), ("172.18.5.101", "172.18.5.3"),
                                            ("172.18.5.62", "172.18.5.3"), ("172.18.5.61", "172.18.5.3"),
                                            ("172.18.5.74", "172.18.5.3")]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT", default_gw=None)

    node_3 = NodeFirewallConfig(ip="172.18.5.3", hostname="telnet_1_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.74", "172.18.5.1", "172.18.5.254",
                                                   "172.18.5.61"]),
                                input_accept=set(
                                    ["172.18.5.74", "172.18.5.7", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254", "172.18.5.101", "172.18.5.61"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.5.54"]),
                                routes=set([("172.18.5.54", "172.18.5.2"), ("172.18.5.7", "172.18.5.74"),
                                            ("172.18.5.62", "172.18.5.74"), ("172.18.5.101", "172.18.5.74")]),
                                default_input="ACCEPT", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_4 = NodeFirewallConfig(ip="172.18.5.21", hostname="honeypot_1_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21",
                                                   "172.18.5.79", "172.18.5.191", "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(
                                    ["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.5.7", "172.18.5.3"), ("172.18.5.101", "172.18.5.3"),
                                     ("172.18.5.62", "172.18.5.3"),
                                     ("172.18.5.61", "172.18.5.3"), ("172.18.5.74", "172.18.5.3"),
                                     ("172.18.5.54", "172.18.5.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                                )

    node_5 = NodeFirewallConfig(ip="172.18.5.79", hostname="ftp_1_1",
                                output_accept=set(
                                    ["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(
                                    ["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79", "172.18.5.191",
                                     "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(
                                    [("172.18.5.7", "172.18.5.3"), ("172.18.5.101", "172.18.5.3"),
                                     ("172.18.5.62", "172.18.5.3"), ("172.18.5.61", "172.18.5.3"),
                                     ("172.18.5.74", "172.18.5.3"), ("172.18.5.54", "172.18.5.2")]
                                ),
                                default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)

    node_6 = NodeFirewallConfig(ip="172.18.5.191", hostname="hacker_kali_1_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21",
                                                   "172.18.5.79", "172.18.5.191", "172.18.5.10", "172.18.5.1"]),
                                input_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21",
                                                  "172.18.5.79", "172.18.5.191", "172.18.5.10", "172.18.5.1"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.5.10")

    node_7 = NodeFirewallConfig(ip="172.18.5.54", hostname="ssh_2_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.54", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(["172.18.5.2", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.5.2"
                                )

    node_8 = NodeFirewallConfig(ip="172.18.5.74", hostname="ssh_3_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                                   "172.18.5.101", "172.18.5.62", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(["172.18.5.3", "172.18.5.61", "172.18.5.62", "172.18.5.74",
                                                  "172.18.5.7", "172.18.5.101", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(["172.18.5.101", "172.18.5.62", "172.18.5.61"]),
                                output_drop=set(), input_drop=set(),
                                forward_drop=set(["172.18.5.7", "172.18.5.101", "172.18.5.62"]),
                                routes=set([
                                    ("172.18.5.2", "172.18.5.3"), ("172.18.5.21", "172.18.5.3"),
                                    ("172.18.5.54", "172.18.5.3"), ("172.18.5.79", "172.18.5.3"),
                                    ("172.18.5.10", "172.18.5.3"), ("172.18.5.191", "172.18.5.3"),
                                    ("172.18.5.61", "172.18.5.3"), ("172.18.5.7", "172.18.5.62")
                                ]),
                                default_input="DROP", default_output="DROP", default_forward="ACCEPT",
                                default_gw=None)

    node_9 = NodeFirewallConfig(ip="172.18.5.61", hostname="telnet_2_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                                   "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(["172.18.5.3", "172.18.5.61", "172.18.5.62", "172.18.5.74",
                                                  "172.18.5.7", "172.18.5.101", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.5.3")

    node_10 = NodeFirewallConfig(ip="172.18.5.62", hostname="telnet_3_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                   "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                                   "172.18.5.1", "172.18.5.254",
                                                   "172.18.5.101", "172.18.5.62", "172.18.5.7"]),
                                input_accept=set(["172.18.5.74", "172.18.5.7", "172.18.5.101", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(),
                                routes=set([("172.18.5.2", "172.18.5.74"), ("172.18.5.21", "172.18.5.74"),
                                            ("172.18.5.54", "172.18.5.74"), ("172.18.5.79", "172.18.5.74"),
                                            ("172.18.5.10", "172.18.5.74"), ("172.18.5.191", "172.18.5.74"),
                                            ("172.18.5.61", "172.18.5.74"), ("172.18.5.101", "172.18.5.74")]),
                                forward_drop=set(["172.18.5.7"]), default_input="DROP", default_output="DROP",
                                default_forward="ACCEPT", default_gw=None)

    node_11 = NodeFirewallConfig(ip="172.18.5.101", hostname="honeypot_2_1",
                                 output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                    "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                                    "172.18.5.101", "172.18.5.62", "172.18.5.1", "172.18.5.254"]),
                                 input_accept=set(["172.18.5.74", "172.18.5.7", "172.18.5.62", "172.18.5.1", "172.18.5.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.5.74")

    node_12 = NodeFirewallConfig(ip="172.18.5.7", hostname="ftp_2_1",
                                 output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21", "172.18.5.79",
                                                    "172.18.5.191", "172.18.5.10", "172.18.5.61", "172.18.5.74",
                                                    "172.18.5.101", "172.18.5.62", "172.18.5.7", "172.18.5.1", "172.18.5.254"]),
                                 input_accept=set(["172.18.5.62", "172.18.5.1", "172.18.5.254"]),
                                 forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                 routes=set(),
                                 default_input="DROP", default_output="DROP", default_forward="DROP",
                                 default_gw="172.18.5.62")
    node_13 = NodeFirewallConfig(ip="172.18.5.254", hostname="client_1_1",
                                output_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21",
                                                   "172.18.5.79", "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                input_accept=set(["172.18.5.2", "172.18.5.3", "172.18.5.21",
                                                  "172.18.5.79", "172.18.5.10", "172.18.5.1", "172.18.5.254"]),
                                forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(),
                                routes=set(),
                                default_input="DROP", default_output="DROP", default_forward="DROP",
                                default_gw="172.18.5.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10, node_11, node_12,
                    node_13]
    topology = Topology(node_configs=node_configs, subnetwork="172.18.5.0/24")
    return topology

# Generates the topology.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        TopologyGenerator.write_topology(default_topology())
    topology = util.read_topology(util.default_topology_path())
    emulation_config = EmulationConfig(agent_ip="172.18.5.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TopologyGenerator.create_topology(topology=topology, emulation_config=emulation_config)

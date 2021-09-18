from typing import List
import random
import numpy as np
from pycr_common.dao.container_config.topology import Topology
from pycr_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from pycr_common.envs_model.config.generator.generator_util import GeneratorUtil
from pycr_common.util.experiments_util import util


class TopologyGenerator:

    @staticmethod
    def generate(num_nodes: int, subnet_prefix : str) -> Topology:
        if num_nodes < 3:
            raise ValueError("At least three nodes are required to create a topology")
        agent_ip_suffix = TopologyGenerator.__generate_random_ip(blacklist=[])

        nodes_ip_suffixes = [agent_ip_suffix]
        for i in range(num_nodes-2):
            ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
            nodes_ip_suffixes.append(ip_suffix)

        node_id_d = {}
        node_id_d_inv = {}
        for i in range(len(nodes_ip_suffixes)):
            node_id_d[nodes_ip_suffixes[i]] = i
            node_id_d_inv[i] = nodes_ip_suffixes[i]

        adj_matrix = np.zeros((len(nodes_ip_suffixes)+1, len(nodes_ip_suffixes)+1))

        reachable = set()
        reachable.add(agent_ip_suffix)

        gateways = {}

        # Attach all nodes to the topology randomly
        for i in range(len(nodes_ip_suffixes)):
            if nodes_ip_suffixes[i] not in reachable:
                l = list(reachable)
                attach = random.randint(0, len(l)-1)
                adj_matrix[node_id_d[l[attach]]][node_id_d[nodes_ip_suffixes[i]]] = 1
                adj_matrix[node_id_d[nodes_ip_suffixes[i]]][node_id_d[l[attach]]] = 1
                reachable.add(nodes_ip_suffixes[i])
                gateways[nodes_ip_suffixes[i]] = l[attach]

        # Create some random links
        for i in range(adj_matrix.shape[0]-1):
            for j in range(adj_matrix.shape[1]-1):
                if j == i:
                    adj_matrix[i][j] = 1
                if np.random.rand() < 0.1:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1

        router_ip_suffix = TopologyGenerator.__generate_random_ip(nodes_ip_suffixes)
        adj_matrix[node_id_d[agent_ip_suffix]][-1] = 1
        adj_matrix[-1][node_id_d[agent_ip_suffix]] = 1

        # gw and agent same connections
        adj_matrix[-1] = adj_matrix[node_id_d[agent_ip_suffix]]
        for i in range(len(nodes_ip_suffixes)):
            if not nodes_ip_suffixes[i] == agent_ip_suffix:
                if adj_matrix[node_id_d[nodes_ip_suffixes[i]]][node_id_d[agent_ip_suffix]] == 1:
                    adj_matrix[node_id_d[nodes_ip_suffixes[i]]][-1] = 1

        gateways[agent_ip_suffix] = router_ip_suffix

        nodes_ip_suffixes.append(router_ip_suffix)
        node_id_d_inv[len(nodes_ip_suffixes) - 1] = router_ip_suffix
        node_id_d[router_ip_suffix] = len(nodes_ip_suffixes) - 1

        node_fw_configs = []
        for i in range(len(nodes_ip_suffixes)):
            ip = subnet_prefix + str(nodes_ip_suffixes[i])
            net_gw = subnet_prefix + "1"
            output_accept = set()
            input_accept = set()
            forward_accept = set()
            output_accept.add(net_gw)
            input_accept.add(net_gw)
            forward_accept.add(net_gw)
            output_drop = set()
            input_drop = set()
            forward_drop = set()
            routes = set()
            for j in range(adj_matrix.shape[1]):
                if adj_matrix[i][j] == 1:
                    input_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                    output_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                    forward_accept.add(subnet_prefix + str(node_id_d_inv[j]))
                else:
                    input_drop.add(subnet_prefix + str(node_id_d_inv[j]))
                    output_drop.add(subnet_prefix + str(node_id_d_inv[j]))
                    forward_drop.add(subnet_prefix + str(node_id_d_inv[j]))

            default_gw = None
            if nodes_ip_suffixes[i]==agent_ip_suffix:
                default_gw = subnet_prefix + str(router_ip_suffix)

            node_cfg = NodeFirewallConfig(ip=ip, output_accept=output_accept, input_accept=input_accept,
                               forward_accept=forward_accept, output_drop=set(), input_drop=set(), forward_drop=set(),
                               routes=set(), default_input="DROP", default_output="DROP", default_forward="DROP",
                               default_gw=default_gw)
            node_fw_configs.append(node_cfg)

        topology = Topology(node_configs=node_fw_configs, subnetwork=subnet_prefix + "0/24")
        agent_ip = subnet_prefix + str(agent_ip_suffix)
        router_ip = subnet_prefix + str(router_ip_suffix)

        return adj_matrix, gateways, topology, agent_ip, router_ip, node_id_d, node_id_d_inv

    @staticmethod
    def __generate_random_ip(blacklist: List) -> int:
        done = False
        ip_suffix = -1
        while not done:
            ip_suffix = random.randint(2, 254)
            if ip_suffix not in blacklist:
                done = True
        return ip_suffix

    @staticmethod
    def create_topology(topology: Topology, emulation_config: EmulationConfig):
        for node in topology.node_configs:
            print("node:{}".format(node.ip))
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=node.ip)
            print("connected")

            for route in node.routes:
                target, gw = route
                cmd = "sudo route add {} gw {}".format(target, gw)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            if node.default_gw is not None:
                cmd = "sudo route add -net {} netmask 255.255.255.0 gw {}".format(topology.subnetwork.replace("/24", ""),
                                                                                  node.default_gw)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            cmd="sudo iptables -F"
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)


            for output_node in node.output_accept:
                cmd = "sudo iptables -A OUTPUT -d {} -j ACCEPT".format(output_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "sudo arptables -A OUTPUT -d {} -j ACCEPT".format(output_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for input_node in node.input_accept:
                cmd = "sudo iptables -A INPUT -s {} -j ACCEPT".format(input_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "sudo arptables -A INPUT -s {} -j ACCEPT".format(input_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for forward_node in node.forward_accept:
                cmd = "sudo iptables -A FORWARD -d {} -j ACCEPT".format(forward_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for output_node in node.output_drop:
                cmd = "sudo iptables -A OUTPUT -d {} -j DROP".format(output_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "sudo arptables -A OUTPUT -d {} -j DROP".format(output_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for input_node in node.input_drop:
                cmd = "sudo iptables -A INPUT -s {} -j DROP".format(input_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                cmd = "sudo arptables -A INPUT -s {} -j DROP".format(input_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            for forward_node in node.forward_drop:
                cmd = "sudo iptables -A FORWARD -d {} -j DROP".format(forward_node)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            cmd = "sudo iptables -A OUTPUT -d {} -j {}".format(topology.subnetwork, node.default_output)
            o,e,_ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = "sudo arptables -A OUTPUT -d {} -j {}".format(topology.subnetwork, node.default_output)
            o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            cmd = "sudo iptables -A INPUT -d {} -j {}".format(topology.subnetwork, node.default_input)
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = "sudo arptables -A INPUT -d {} -j {}".format(topology.subnetwork, node.default_input)
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            cmd = "sudo iptables -A FORWARD -d {} -j {}".format(topology.subnetwork, node.default_forward)
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
            cmd = "sudo arptables -A FORWARD -d {} -j {}".format(topology.subnetwork, node.default_forward)
            EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            GeneratorUtil.disconnect_admin(emulation_config=emulation_config)


    @staticmethod
    def write_topology(topology: Topology, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_topology_path(out_dir=path)
        util.write_topology_file(topology, path)


if __name__ == '__main__':
    adj_matrix, gws, topology = TopologyGenerator.generate(num_nodes=10, subnet_prefix="172.18.2.")
    print(adj_matrix)
    print(gws)
    print(topology)
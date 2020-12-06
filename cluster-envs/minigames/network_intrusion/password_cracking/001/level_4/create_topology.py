import os
from gym_pycr_pwcrack.dao.container_config.topology import Topology
from gym_pycr_pwcrack.dao.container_config.node_firewall_config import NodeFirewallConfig
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig
from gym_pycr_pwcrack.envs.logic.cluster.cluster_util import ClusterUtil

def connect_admin(cluster_config: ClusterConfig, ip : str):
    cluster_config.agent_ip = ip
    cluster_config.connect_agent()

def disconnect_admin(cluster_config: ClusterConfig):
    cluster_config.close()

def default_topology() -> Topology:
    node_1 = NodeFirewallConfig(ip="172.18.4.10",
                           output_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79",
                                                "172.18.4.191", "172.18.4.10", "172.18.4.1"]),
                           input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79",
                                             "172.18.4.191", "172.18.4.10", "172.18.4.1"]),
                           forward_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79",
                                             "172.18.4.191", "172.18.4.1"]),
                           output_drop = set(), input_drop = set(), forward_drop = set(), routes=set(),
                           default_input = "DROP", default_output = "DROP", default_forward="DROP",
                           default_gw=None
                           )
    node_2 = NodeFirewallConfig(ip="172.18.4.2",
                       output_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                          "172.18.4.10", "172.18.4.1"]),
                       input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                         "172.18.4.10", "172.18.4.1"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), routes=set(), forward_drop=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                       )
    node_3 = NodeFirewallConfig(ip="172.18.4.3",
                           output_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                         "172.18.4.10", "172.18.4.1"]),
                           input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                             "172.18.4.10", "172.18.4.1"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                            default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_4 = NodeFirewallConfig(ip="172.18.4.21",
                           output_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21",
                                                "172.18.4.79", "172.18.4.191", "172.18.4.10", "172.18.4.1"]),
                           input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                             "172.18.4.10", "172.18.4.1"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None
                           )
    node_4 = NodeFirewallConfig(ip="172.18.4.79",
                           output_accept=set(
                               ["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                "172.18.4.10", "172.18.4.1"]),
                           input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21", "172.18.4.79", "172.18.4.191",
                                             "172.18.4.10", "172.18.4.1"]),
                           forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                           default_input="DROP", default_output="DROP", default_forward="DROP", default_gw=None)
    node_5 = NodeFirewallConfig(ip="172.18.4.191",
                       output_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21",
                                          "172.18.4.79", "172.18.4.191", "172.18.4.10", "172.18.4.1"]),
                       input_accept=set(["172.18.4.2", "172.18.4.3", "172.18.4.21",
                                         "172.18.4.79", "172.18.4.191", "172.18.4.10", "172.18.4.1"]),
                       forward_accept=set(), output_drop=set(), input_drop=set(), forward_drop=set(), routes=set(),
                       default_input="DROP", default_output="DROP", default_forward="DROP", default_gw="172.18.4.10")
    node_configs = [node_1, node_2, node_3, node_4, node_5]
    topology = Topology(node_configs=node_configs, subnetwork = "172.18.4.0/24")
    return topology

def write_default_topology(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_topology_path()
    topology = default_topology()
    util.write_topology_file(topology, path)

def create_topology(topology: Topology, cluster_config: ClusterConfig):
    for node in topology.node_configs:
        print("node:{}".format(node.ip))
        connect_admin(cluster_config=cluster_config, ip=node.ip)

        for route in node.routes:
            target, gw = route
            cmd = "sudo route add {} gw {}".format(target, gw)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        if node.default_gw is not None:
            cmd = "sudo route add -net {} netmask 255.255.255.0 gw {}".format(topology.subnetwork.replace("/24", ""),
                                                                              node.default_gw)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd="sudo iptables -F"
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)


        for output_node in node.output_accept:
            cmd = "sudo iptables -A OUTPUT -d {} -j ACCEPT".format(output_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for input_node in node.input_accept:
            cmd = "sudo iptables -A INPUT -s {} -j ACCEPT".format(input_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for forward_node in node.forward_accept:
            cmd = "sudo iptables -A FORWARD -d {} -j ACCEPT".format(forward_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for output_node in node.output_drop:
            cmd = "sudo iptables -A OUTPUT -d {} -j DROP".format(output_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for input_node in node.input_drop:
            cmd = "sudo iptables -A INPUT -s {} -j DROP".format(input_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        for forward_node in node.forward_drop:
            cmd = "sudo iptables -A FORWARD -d {} -j DROP".format(forward_node)
            ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A OUTPUT -d {} -j {}".format(topology.subnetwork, node.default_output)
        o,e,_ = ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A INPUT -d {} -j {}".format(topology.subnetwork, node.default_input)
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        cmd = "sudo iptables -A FORWARD -d {} -j {}".format(topology.subnetwork, node.default_forward)
        ClusterUtil.execute_ssh_cmd(cmd=cmd, conn=cluster_config.agent_conn)

        disconnect_admin(cluster_config=cluster_config)



if __name__ == '__main__':
    if not os.path.exists(util.default_topology_path()):
        write_default_topology()
    topology = util.read_topology(util.default_topology_path())
    cluster_config = ClusterConfig(agent_ip="172.18.4.191", agent_username="pycr_admin",
                                   agent_pw="pycr@admin-pw_191", server_connection=False)
    create_topology(topology=topology, cluster_config=cluster_config)
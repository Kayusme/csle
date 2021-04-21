from typing import List, Tuple
import pickle
from gym_pycr_ctf.dao.network.node import Node
from gym_pycr_ctf.dao.network.node_type import NodeType
from gym_pycr_ctf.dao.defender_dynamics.defender_dynamics_model import DefenderDynamicsModel
import numpy as np


class NetworkConfig:
    """
    DTO Representing a network configuration
    """

    def __init__(self, subnet_mask: str, nodes: List[Node], adj_matrix: np.ndarray, flags_lookup: dict,
                 agent_reachable: set, vulnerable_nodes = None):
        self.subnet_mask = subnet_mask
        self.nodes = nodes
        self.adj_matrix = adj_matrix
        node_d, hacker, router, levels_d = self.create_lookup_dicts()
        self.node_d = node_d
        self.hacker = hacker
        self.router = router
        self.levels_d = levels_d
        self.flags_lookup = flags_lookup
        self.agent_reachable = agent_reachable
        self.vulnerable_nodes = vulnerable_nodes
        self.defender_dynamics_model = DefenderDynamicsModel()

    def __str__(self) -> str:
        """
        :return: a string representation of the DTO
        """
        return "subnet_mask:{}, nodes:{}, adj_matrix:{}, hacker:{}, router: {}, flags_lookup: {}, agent_reachable: {}, " \
               "vulnerable_nodes: {}, defender_dynamics_model:{}".format(
            self.subnet_mask, list(map(lambda x: str(x), self.nodes)), self.adj_matrix, self.hacker, self.router, self.flags_lookup,
            self.agent_reachable, self.vulnerable_nodes, self.defender_dynamics_model)

    def create_lookup_dicts(self) -> Tuple[dict, Node, Node, dict]:
        """
        Utility function for creating lookup dictionaries, useful when rending the network

        :return: A lookup dictionary for nodes, the hacker node, the router node, and a lookup dictionary
                 for levels in the network
        """
        levels_d = {}
        node_d = {}
        hacker = None
        router = None
        for node in self.nodes:
            node_d[node.id] = node
            if node.type == NodeType.HACKER:
                if hacker is not None:
                    raise ValueError("Invalid Network Config: 2 Hackers")
                hacker = node
            elif node.type == NodeType.ROUTER:
                if router is not None:
                    raise ValueError("Invalid Network Config: 2 Routers")
                router = node
            if node.level in levels_d:
                levels_d[node.level].append(node)
                #levels_d[node.level] = n_level
            else:
                levels_d[node.level] = [node]

        return node_d, hacker, router, levels_d

    def copy(self):
        """
        :return: a copy of the network configuration
        """
        return NetworkConfig(
            subnet_mask=self.subnet_mask, nodes=self.nodes, adj_matrix=self.adj_matrix, flags_lookup=self.flags_lookup,
            agent_reachable=self.agent_reachable)

    def shortest_paths(self) -> List[Tuple[List[str], List[int]]]:
        """
        Utility function for finding the shortest paths to find all flags using brute-force search

        :return: a list of the shortest paths (list of ips and flags)
        """
        shortest_paths = self._find_nodes(reachable=self.agent_reachable, path=[], flags=[])
        return shortest_paths

    def _find_nodes(self, reachable, path, flags) -> List[Tuple[List[str], List[int]]]:
        """
        Utility function for finding the next node in a brute-force-search procedure for finding all flags
        in the network

        :param reachable: the set of reachable nodes from the current attacker state
        :param path: the current path
        :param flags: the set of flags
        :return: a list of the shortest paths (list of ips and flags)
        """
        paths = []
        min_path_len = len(self.nodes)
        for n in self.nodes:
            l_reachable = reachable.copy()
            l_path = path.copy()
            l_flags = flags.copy()
            if n.ip in l_reachable and n.ip in self.vulnerable_nodes and n.ip not in l_path:
                l_reachable.update(n.reachable_nodes)
                l_path.append(n.ip)
                l_flags = l_flags + n.flags
                if len(l_flags)== len(self.flags_lookup):
                    paths.append((l_path, l_flags.copy()))
                    if len(l_path) < min_path_len:
                        min_path_len = len(l_path)
                elif len(l_path) < min_path_len:
                    paths = paths + self._find_nodes(l_reachable, l_path, l_flags)
        return paths

    def save(self, path: str) -> None:
        """
        Utility function for saving the network config to disk

        :param path: the path to save it to
        :return: None
        """
        with open(path, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(path) -> "NetworkConfig":
        """
        Utility function for loading the network config from a pickled file on disk

        :param path: the path to load it from
        :return: the loaded network config
        """
        with open(path, 'rb') as file:
            obj = pickle.load(file)
            return obj



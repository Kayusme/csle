from typing import Set
from csle_common.dao.domain_randomization.csle_node_randomizer_config import CSLENodeRandomizerConfig
from csle_common.dao.container_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.container_config.node_users_config import NodeUsersConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from gym_csle_ctf.dao.domain_randomization.csle_ctf_randomization_space import CSLECTFRandomizationSpace


class CSLECTFNodeRandomizerConfig(CSLENodeRandomizerConfig):


    def __init__(self, ip: str, reachable: Set[str], id: int, users_config: NodeUsersConfig,
                  flags_config: NodeFlagsConfig, vulns_config: NodeVulnerabilityConfig,
                  r_space: CSLECTFRandomizationSpace,
                  router: bool = False, agent: bool = False, gateway: bool = False):
        """
        Creates a config DTO for randomizing a node in a csle-CTF env

        :param ip: the ip of the node
        :param reachable: the list of reachable nodes
        :param id: the id of the node
        :param users_config: the configuration of the users
        :param flags_config: the configuration of the flags
        :param vulns_config: the configuration of the vulnerabilities
        :param r_space: the randomization space
        :param router: the router
        :param agent: the agent
        :param gateway: the gateway
        :return: the randomized node
        """
        self.ip = ip
        self.reachable = reachable
        self.id = id
        self.users_config = users_config
        self.flags_config = flags_config
        self.vulns_config = vulns_config
        self.r_space = r_space
        self.router = router
        self.agent = agent
        self.gateway=gateway


    def __str__(self):
        return f"ip: {self.ip}, reachable: {self.reachable}, id: {self.id}, users_config: {self.users_config}, " \
               f"flags_config: {self.flags_config}, vulns_config: {self.vulns_config}, r_space: {str(self.r_space)}," \
               f"router: {self.router}, agent: {self.agent}, gateway: {self.gateway}"
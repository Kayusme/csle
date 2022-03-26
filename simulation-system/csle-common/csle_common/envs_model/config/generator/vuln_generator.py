from typing import List
import random
import numpy as np
from csle_common.dao.container_config.topology import Topology
from csle_common.dao.container_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.container_config.vulnerabilities_config import VulnerabilitiesConfig
from csle_common.dao.container_config.pw_vulnerability_config import PwVulnerabilityConfig
from csle_common.dao.container_config.rce_vulnerability_config import RceVulnerabilityConfig
from csle_common.dao.container_config.priv_esc_vulnerability_config import PrivEscVulnerabilityConfig
from csle_common.dao.container_config.sql_injection_vulnerability_config import SQLInjectionVulnerabilityConfig
from csle_common.dao.container_config.vulnerability_type import VulnType
from csle_common.envs_model.config.generator.topology_generator import TopologyGenerator
from csle_common.envs_model.config.generator.users_generator import UsersGenerator
from csle_common.envs_model.config.generator.generator_util import GeneratorUtil
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.logic.emulation.util.common.emulation_util import EmulationUtil
from csle_common.util.experiments_util import util
import csle_common.constants.constants as constants


class VulnerabilityGenerator:
    """
    A Utility Class for generating vulnerability configuration files
    """


    @staticmethod
    def shortlist() -> List[str]:
        """
        :return: a list of shortlist usernames for password vulnerabilities
        """
        return constants.VULNERABILITY_GENERATOR.NAMES_SHORTLIST


    @staticmethod
    def generate(topology: Topology, vulnerable_nodes : List[NodeFirewallConfig], agent_ip : str,
                 router_ip: str, subnet_prefix :str, num_flags,
                 access_vuln_types : List[VulnType]) -> VulnerabilitiesConfig:
        """
        Utility function for generating a vulnerability configuration for an emulation

        :param topology: the topology of the emulation
        :param vulnerable_nodes: the gateways of the emulation
        :param agent_ip: the ip of the agent container
        :param router_ip: the ip of the gateway container
        :param subnet_prefix: the prefix of of the subnet
        :param num_flags: the number of flags
        :param access_vuln_types: the vulnerability types that yield shell access
        :return: The created vulnerabilities config
        """
        vulnerabilities = []

        # Start by creating necessary vulns
        for vulnerable_node in vulnerable_nodes:
            ip = subnet_prefix + str(vulnerable_node)
            if ip != agent_ip and ip != router_ip:
                vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                vuln_type = access_vuln_types[vuln_idx]
                if vuln_type == VulnType.WEAK_PW:
                    vuln_cfg = VulnerabilityGenerator.pw_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.RCE:
                    vuln_cfg = VulnerabilityGenerator.rce_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.SQL_INJECTION:
                    vuln_cfg = VulnerabilityGenerator.sql_injection_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg)
                elif vuln_type == VulnType.PRIVILEGE_ESCALATION:
                    vuln_cfg_1 = VulnerabilityGenerator.pw_vuln(vulnerable_node)
                    vulnerabilities.append(vuln_cfg_1)
                    vuln_cfg_2 = VulnerabilityGenerator.priv_esc_vuln(vulnerable_node, username=vuln_cfg_1.username,
                                                                      pw=vuln_cfg_1.pw)
                    vulnerabilities.append(vuln_cfg_2)
                else:
                    raise ValueError("Unrecognized vulnerability type")

        for node in topology.node_configs:
            # Create vuln necessary for flags and some random vulns
            if len(vulnerable_nodes) < num_flags or np.random.rand() < 0.2:
                if agent_ip not in node.get_ips() and router_ip not in node.get_ips() and node not in vulnerable_nodes:
                    vuln_idx = random.randint(0, len(access_vuln_types) - 1)
                    vuln_type = access_vuln_types[vuln_idx]
                    if vuln_type == VulnType.WEAK_PW:
                        vuln_cfg = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.RCE:
                        vuln_cfg = VulnerabilityGenerator.rce_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.SQL_INJECTION:
                        vuln_cfg = VulnerabilityGenerator.sql_injection_vuln(node)
                        vulnerabilities.append(vuln_cfg)
                    elif vuln_type == VulnType.PRIVILEGE_ESCALATION:
                        vuln_cfg_1 = VulnerabilityGenerator.pw_vuln(node)
                        vulnerabilities.append(vuln_cfg_1)
                        vuln_cfg_2 = VulnerabilityGenerator.priv_esc_vuln(node, username=vuln_cfg_1.username,
                                                                          pw=vuln_cfg_1.pw)
                        vulnerabilities.append(vuln_cfg_2)
                    else:
                        raise ValueError("Unrecognized vulnerability type")

        vulns_cfg = VulnerabilitiesConfig(vulnerabilities=vulnerabilities)
        return vulns_cfg

    @staticmethod
    def pw_vuln(node: NodeFirewallConfig) -> PwVulnerabilityConfig:
        """
        Utility function for creating a password vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        pw_shortlist = VulnerabilityGenerator.shortlist()
        pw_idx = random.randint(0, len(pw_shortlist)-1)
        u = pw_shortlist[pw_idx]
        pw = pw_shortlist[pw_idx]
        vuln_config = PwVulnerabilityConfig(ip= node.get_ips()[0], vuln_type=VulnType.WEAK_PW, username=u, pw=pw, root=True)
        return vuln_config


    @staticmethod
    def rce_vuln(node: NodeFirewallConfig) -> RceVulnerabilityConfig:
        """
        Utility function for creating an RCE vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        vuln_config = RceVulnerabilityConfig(ip=node.get_ips()[0], vuln_type=VulnType.RCE)
        return vuln_config

    @staticmethod
    def priv_esc_vuln(node: NodeFirewallConfig, username: str, pw: str) -> PrivEscVulnerabilityConfig:
        """
        Utility function for creating a Priv-Esc vulnerability config object

        :param username: the username of to do the escalation
        :param pw: the password to do the escalation
        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        priv_esc_cve_idx = random.randint(0, len(constants.EXPLOIT_VULNERABILITES.PRIVILEGE_ESC_VULNS) - 1)
        root =False
        vuln_config = PrivEscVulnerabilityConfig(
            ip=node.get_ips()[0], vuln_type=VulnType.PRIVILEGE_ESCALATION, username=username, pw=pw, root=root,
            cve=constants.EXPLOIT_VULNERABILITES.PRIVILEGE_ESC_VULNS[priv_esc_cve_idx])
        return vuln_config


    @staticmethod
    def sql_injection_vuln(node: NodeFirewallConfig) -> SQLInjectionVulnerabilityConfig:
        """
        Utility function for creating a SQL-Injection vulnerability config object

        :param node: the node to create the vulnerability on
        :return: the created vulnerability
        """
        vuln_config = SQLInjectionVulnerabilityConfig(ip=node.get_ips()[0], vuln_type=VulnType.SQL_INJECTION,
                                             username=constants.DVWA_SQL_INJECTION.EXPLOIT_USER,
                                             pw=constants.DVWA_SQL_INJECTION.EXPLOIT_PW, root=True)
        return vuln_config


    @staticmethod
    def create_vulns(vuln_cfg: VulnerabilitiesConfig, emulation_config: EmulationConfig) -> None:
        """
        Utility function for connecting to a running emulation and creating vulnerabilities

        :param vuln_cfg: the vulnerability config
        :param emulation_config: the emulation config
        :return: None
        """
        vulnerabilities = vuln_cfg.vulnerabilities
        for vuln in vulnerabilities:
            GeneratorUtil.connect_admin(emulation_config=emulation_config, ip=vuln.ip)
            if vuln.vuln_type == VulnType.WEAK_PW or vuln.vuln_type == VulnType.SQL_INJECTION or \
                    vuln.vuln_type == VulnType.PRIVILEGE_ESCALATION:
                cmd = "ls /home"
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                users_w_home = o.decode().split("\n")
                users_w_home = list(filter(lambda x: x != '', users_w_home))

                for user in users_w_home:
                    if user != "csle_admin" and user == vuln.username:
                        cmd = "sudo deluser {}".format(user)
                        EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                        cmd = "sudo rm -rf /home/{}".format(user)
                        EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                cmd = "sudo deluser {}".format(vuln.username)
                EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                if vuln.root:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -g root -G sudo -p \"$(openssl passwd -1 '{}')\" {}".format(
                        vuln.username, vuln.pw, vuln.username)
                else:
                    cmd = "sudo useradd -rm -d /home/{} -s /bin/bash -p \"$(openssl passwd -1 '{}')\" {}".format(
                        vuln.username, vuln.pw, vuln.username)
                o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                # Update sudoers file
                if vuln.vuln_type == VulnType.PRIVILEGE_ESCALATION:

                    # Restore/Backup sudoers file
                    cmd = "sudo cp /etc/sudoers.bak /etc/sudoers"
                    EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

                    # Install sudoers vulnerability
                    if vuln.cve.lower() == constants.EXPLOIT_VULNERABILITES.CVE_2010_0426:
                        cmd = "sudo su root -c \"echo '{} ALL=NOPASSWD: sudoedit /etc/fstab' >> /etc/sudoers\""
                    elif vuln.cve.lower() == constants.EXPLOIT_VULNERABILITES.CVE_2015_5602:
                        cmd = "sudo su root -c \"echo '{} ALL=NOPASSWD: sudoedit /home/*/*/esc.txt' >> /etc/sudoers\""
                    else:
                        raise ValueError("CVE not recognized:{}".format(vuln.cve))
                    cmd = cmd.format(vuln.username)
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
                    cmd = "sudo chmod 440 /etc/sudoers"
                    o, e, _ = EmulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)

            elif vuln.vuln_type == VulnType.RCE:
                pass # Nothing to install
            else:
                raise ValueError("Vulnerability type not recognized")


    @staticmethod
    def write_vuln_config(vulns_cfg: VulnerabilitiesConfig, path: str = None) -> None:
        """
        Writes the default configuration to a json file

        :param vulns_cfg: the config to write
        :param path: the path to write the configuration to
        :return: None
        """
        path = util.default_vulnerabilities_path(out_dir=path)
        util.write_vulns_config_file(vulns_cfg, path)


if __name__ == '__main__':
    topology, agent_ip, router_ip, vulnerable_nodes = TopologyGenerator.generate(
        num_nodes=15, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2", subnet_id=2)
    vulnerabilities = VulnerabilityGenerator.generate(
        topology=topology, vulnerable_nodes=vulnerable_nodes,
        agent_ip=agent_ip, router_ip=router_ip, subnet_prefix=f"{constants.CSLE.CSLE_SUBNETMASK_PREFIX}2",
        num_flags = 3, access_vuln_types=[VulnType.WEAK_PW])
    print(vulnerabilities)




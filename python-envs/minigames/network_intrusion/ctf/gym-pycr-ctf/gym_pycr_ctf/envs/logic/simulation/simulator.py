from typing import Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.action import Action
from gym_pycr_ctf.dao.action.action_type import ActionType
from gym_pycr_ctf.dao.action.action_id import ActionId
from gym_pycr_ctf.envs.logic.simulation.recon_simulator import ReconSimulator
from gym_pycr_ctf.envs.logic.simulation.exploit_simulator import ExploitSimulator
from gym_pycr_ctf.envs.logic.simulation.post_exploit_simulator import PostExploitSimulator
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

class Simulator:
    """
    Simulator class. This class is used to simulate actions using a MDP or Markov Game model rather than taking
    real actions in the emulation environment.
    """
    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Simulates a state transition in the MDP or Markov Game

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if a.type == ActionType.RECON:
            EnvDynamicsUtil.cache_action(env_config=env_config,a=a, s=s)
            return Simulator.recon_action(s=s, a=a, env_config=env_config)
        elif a.type == ActionType.EXPLOIT or a.type == ActionType.PRIVILEGE_ESCALATION:
            if a.subnet:
                EnvDynamicsUtil.cache_action(env_config=env_config, a=a, s=s)
            return Simulator.exploit_action(s=s, a=a, env_config=env_config)
        elif a.type == ActionType.POST_EXPLOIT:
            return Simulator.post_exploit_action(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Action type:{} not recognized".format(a.type))

    @staticmethod
    def recon_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs a reconnaissance action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if a.id == ActionId.TCP_SYN_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == ActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == ActionId.PING_SCAN_SUBNET or a.id == ActionId.PING_SCAN_HOST\
                or a.id == ActionId.PING_SCAN_ALL:
            return ReconSimulator.simulate_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.UDP_PORT_SCAN_SUBNET or a.id == ActionId.UDP_PORT_SCAN_HOST\
                or a.id == ActionId.UDP_PORT_SCAN_ALL:
            return ReconSimulator.simulate_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_HOST\
                or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconSimulator.simulate_con_non_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_FIN_SCAN_SUBNET or a.id == ActionId.TCP_FIN_SCAN_HOST\
                or a.id == ActionId.TCP_FIN_SCAN_ALL:
            return ReconSimulator.simulate_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_NULL_SCAN_SUBNET or a.id == ActionId.TCP_NULL_SCAN_HOST\
                or a.id == ActionId.TCP_NULL_SCAN_ALL:
            return ReconSimulator.simulate_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == ActionId.TCP_XMAS_TREE_SCAN_SUBNET\
                or a.id == ActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconSimulator.simulate_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.OS_DETECTION_SCAN_HOST or a.id == ActionId.OS_DETECTION_SCAN_SUBNET\
                or a.id == ActionId.OS_DETECTION_SCAN_ALL:
            return ReconSimulator.simulate_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.VULSCAN_HOST or a.id == ActionId.VULSCAN_SUBNET\
                or a.id == ActionId.VULSCAN_ALL:
            return ReconSimulator.simulate_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NMAP_VULNERS_HOST or a.id == ActionId.NMAP_VULNERS_SUBNET\
                or a.id == ActionId.NMAP_VULNERS_ALL:
            return ReconSimulator.simulate_nmap_vulners(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NIKTO_WEB_HOST_SCAN:
            return ReconSimulator.simulate_nikto_web_host_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MASSCAN_HOST_SCAN or a.id == ActionId.MASSCAN_SUBNET_SCAN\
                or a.id == ActionId.MASSCAN_SUBNET_ALL:
            return ReconSimulator.simulate_masscan_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FIREWALK_HOST or a.id == ActionId.FIREWALK_SUBNET\
                or a.id == ActionId.FIREWALK_ALL:
            return ReconSimulator.simulate_firewalk_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.HTTP_ENUM_HOST or a.id == ActionId.HTTP_ENUM_SUBNET\
                or a.id == ActionId.HTTP_ENUM_ALL:
            return ReconSimulator.simulate_http_enum(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.HTTP_GREP_HOST or a.id == ActionId.HTTP_GREP_SUBNET\
                or a.id == ActionId.HTTP_GREP_ALL:
            return ReconSimulator.simulate_http_grep(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FINGER_HOST or a.id == ActionId.FINGER_SUBNET\
                or a.id == ActionId.FINGER_ALL:
            return ReconSimulator.simulate_finger(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def exploit_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Performs an exploit action

        :param s: the current state
        :param a: the action to take
        :param env_config: the environment configuration
        :return: s_prime, reward, done
        """
        if a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitSimulator.simulate_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SAMBACRY_EXPLOIT:
            raise NotImplementedError("Sambacry simulation not implemented")
        elif a.id == ActionId.SHELLSHOCK_EXPLOIT:
            raise NotImplementedError("Shellshock simulation not implemented")
        elif a.id == ActionId.DVWA_SQL_INJECTION:
            raise NotImplementedError("DVWA SQL Injection simulation not implemented")
        elif a.id == ActionId.CVE_2015_3306_EXPLOIT:
            raise NotImplementedError("CVE-2015-3306 simulation not implemented")
        elif a.id == ActionId.CVE_2015_1427_EXPLOIT:
            raise NotImplementedError("CVE-2015-1427 simulation not implemented")
        elif a.id == ActionId.CVE_2016_10033_EXPLOIT:
            raise NotImplementedError("CVE-2016-10033 simulation not implemented")
        elif a.id == ActionId.CVE_2010_0426_PRIV_ESC:
            raise NotImplementedError("CVE-2010-0426 simulation not implemented")
        elif a.id == ActionId.CVE_2015_5602_PRIV_ESC:
            raise NotImplementedError("CVE-2015-5602 simulation not implemented")
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def post_exploit_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Simulates a post-exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.NETWORK_SERVICE_LOGIN:
            s_1, r_1, _ = PostExploitSimulator.simulate_ssh_login(s=s, a=a, env_config=env_config)
            s_2, r_2, _ = PostExploitSimulator.simulate_ftp_login(s=s_1, a=a, env_config=env_config)
            s_3, r_3, done = PostExploitSimulator.simulate_telnet_login(s=s_2, a=a, env_config=env_config)
            rewards = list(filter(lambda x: x >= 0, [r_1, r_2, r_3]))
            if len(rewards) > 0:
                reward = sum(rewards)
            else:
                reward = r_3
            return s_3, reward, done
        if a.id == ActionId.FIND_FLAG:
            return PostExploitSimulator.simulate_bash_find_flag(s=s, a=a, env_config=env_config)
        if a.id == ActionId.INSTALL_TOOLS:
            return PostExploitSimulator.execute_install_tools(s=s, a=a, env_config=env_config)
        if a.id == ActionId.SSH_BACKDOOR:
            return PostExploitSimulator.execute_ssh_backdoor(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))



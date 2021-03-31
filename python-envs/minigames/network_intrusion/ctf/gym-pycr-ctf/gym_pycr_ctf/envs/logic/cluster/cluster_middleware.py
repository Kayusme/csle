from typing import Union, Tuple
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.action.action import Action
from gym_pycr_ctf.dao.action.action_type import ActionType
from gym_pycr_ctf.dao.action.action_id import ActionId
from gym_pycr_ctf.envs.logic.cluster.recon_middleware import ReconMiddleware
from gym_pycr_ctf.envs.logic.cluster.exploit_middleware import ExploitMiddleware
from gym_pycr_ctf.envs.logic.cluster.post_exploit_middleware import PostExploitMiddleware
from gym_pycr_ctf.envs.logic.common.env_dynamics_util import EnvDynamicsUtil

class ClusterMiddleware:
    """
    Class that provides a middleware between the OpenAI Gym Env and the Cluster
    """

    @staticmethod
    def transition(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition operator T: (s,a) -> (s',r)

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.type == ActionType.RECON:
            EnvDynamicsUtil.cache_action(env_config=env_config, a=a, s=s)
            return ClusterMiddleware.recon_action(s=s,a=a,env_config=env_config)
        elif a.type == ActionType.EXPLOIT or a.type == ActionType.PRIVILEGE_ESCALATION:
            if a.subnet:
                EnvDynamicsUtil.cache_action(env_config=env_config, a=a, s=s)
            return ClusterMiddleware.exploit_action(s=s, a=a, env_config=env_config)
        elif a.type == ActionType.POST_EXPLOIT:
            return ClusterMiddleware.post_exploit_action(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Action type not recognized")

    @staticmethod
    def recon_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition of a reconnaissance action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.TCP_SYN_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_SYN_STEALTH_SCAN_HOST \
                or a.id == ActionId.TCP_SYN_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_syn_stealth_scan(s=s,a=a,env_config=env_config)
        elif a.id == ActionId.PING_SCAN_SUBNET or a.id == ActionId.PING_SCAN_HOST or a.id == ActionId.PING_SCAN_ALL:
            return ReconMiddleware.execute_ping_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.UDP_PORT_SCAN_SUBNET or a.id == ActionId.UDP_PORT_SCAN_HOST \
                or a.id == ActionId.UDP_PORT_SCAN_ALL:
            return ReconMiddleware.execute_udp_port_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_SUBNET or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_HOST \
                or a.id == ActionId.TCP_CON_NON_STEALTH_SCAN_ALL:
            return ReconMiddleware.execute_tcp_con_stealth_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_FIN_SCAN_SUBNET or a.id == ActionId.TCP_FIN_SCAN_HOST \
                or a.id == ActionId.TCP_FIN_SCAN_ALL:
            return ReconMiddleware.execute_tcp_fin_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_NULL_SCAN_SUBNET or a.id == ActionId.TCP_NULL_SCAN_HOST \
                or a.id == ActionId.TCP_NULL_SCAN_ALL:
            return ReconMiddleware.execute_tcp_null_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.TCP_XMAS_TREE_SCAN_HOST or a.id == ActionId.TCP_XMAS_TREE_SCAN_SUBNET \
                or a.id == ActionId.TCP_XMAS_TREE_SCAN_ALL:
            return ReconMiddleware.execute_tcp_xmas_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.OS_DETECTION_SCAN_HOST or a.id == ActionId.OS_DETECTION_SCAN_SUBNET \
                or a.id == ActionId.OS_DETECTION_SCAN_ALL:
            return ReconMiddleware.execute_os_detection_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.VULSCAN_HOST or a.id == ActionId.VULSCAN_SUBNET or a.id == ActionId.VULSCAN_ALL:
            return ReconMiddleware.execute_vulscan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NMAP_VULNERS_HOST or a.id == ActionId.NMAP_VULNERS_SUBNET \
                or a.id == ActionId.NMAP_VULNERS_ALL:
            return ReconMiddleware.execute_nmap_vulners(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.NIKTO_WEB_HOST_SCAN:
            return ReconMiddleware.execute_nikto_web_host_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MASSCAN_HOST_SCAN or a.id == ActionId.MASSCAN_SUBNET_SCAN:
            return ReconMiddleware.execute_masscan_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FIREWALK_HOST or a.id == ActionId.FIREWALK_SUBNET or a.id == ActionId.FIREWALK_ALL:
            return ReconMiddleware.execute_firewalk_scan(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.HTTP_ENUM_HOST or a.id == ActionId.HTTP_ENUM_SUBNET or a.id == ActionId.HTTP_ENUM_ALL:
            return ReconMiddleware.execute_http_enum(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.HTTP_GREP_HOST or a.id == ActionId.HTTP_GREP_SUBNET or a.id == ActionId.HTTP_GREP_ALL:
            return ReconMiddleware.execute_http_grep(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FINGER_HOST or a.id == ActionId.FINGER_SUBNET or a.id == ActionId.FINGER_ALL:
            return ReconMiddleware.execute_finger(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Recon action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def exploit_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements transition of an exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == ActionId.TELNET_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_telnet_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == ActionId.SSH_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ssh_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == ActionId.FTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_ftp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.CASSANDRA_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_cassandra_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_SUBNET \
                or a.id == ActionId.IRC_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_irc_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.MONGO_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mongo_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.MYSQL_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_mysql_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.SMTP_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_smtp_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_HOST or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_SUBNET\
                or a.id == ActionId.POSTGRES_SAME_USER_PASS_DICTIONARY_ALL:
            return ExploitMiddleware.execute_postgres_same_user_dictionary(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SAMBACRY_EXPLOIT:
            return ExploitMiddleware.execute_sambacry(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.SHELLSHOCK_EXPLOIT:
            return ExploitMiddleware.execute_shellshock(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.DVWA_SQL_INJECTION:
            return ExploitMiddleware.execute_dvwa_sql_injection(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CVE_2015_3306_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_3306_exploit(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CVE_2015_1427_EXPLOIT:
            return ExploitMiddleware.execute_cve_2015_1427_exploit(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CVE_2016_10033_EXPLOIT:
            return ExploitMiddleware.execute_cve_2016_10033_exploit(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CVE_2010_0426_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2010_0426_exploit(s=s, a=a, env_config=env_config)
        elif a.id == ActionId.CVE_2015_5602_PRIV_ESC:
            return ExploitMiddleware.execute_cve_2015_5602_exploit(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Exploit action id:{},name:{} not recognized".format(a.id, a.name))

    @staticmethod
    def post_exploit_action(s: EnvState, a: Action, env_config: EnvConfig) -> Tuple[EnvState, int, bool]:
        """
        Implements the transition of a post-exploit action

        :param s: the current state
        :param a: the action
        :param env_config: the environment configuration
        :return: s', r, done
        """
        if a.id == ActionId.NETWORK_SERVICE_LOGIN:
            return PostExploitMiddleware.execute_service_login(s=s, a=a, env_config=env_config)
        if a.id == ActionId.FIND_FLAG:
            return PostExploitMiddleware.execute_bash_find_flag(s=s, a=a, env_config=env_config)
        if a.id == ActionId.INSTALL_TOOLS:
            return PostExploitMiddleware.execute_install_tools(s=s, a=a, env_config=env_config)
        if a.id == ActionId.SSH_BACKDOOR:
            return PostExploitMiddleware.execute_ssh_backdoor(s=s, a=a, env_config=env_config)
        else:
            raise ValueError("Post-expoit action id:{},name:{} not recognized".format(a.id, a.name))
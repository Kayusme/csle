from csle_common.envs_model.config.generator.env_config_generator import EnvConfigGenerator
from csle_common.util.experiments_util import util
from csle_common.dao.container_config.container_env_config import ContainerEnvConfig

def generate_config() -> None:
    """
    Creates the random environment configuration
    """
    container_pool = [("ftp_1", "0.0.1"), ("ftp_2", "0.0.1"), ("honeypot_1", "0.0.1"),
                      ("honeypot_2", "0.0.1"),
                      ("ssh_1", "0.0.1"), ("ssh_2", "0.0.1"),
                      ("ssh_3", "0.0.1"), ("telnet_1", "0.0.1"), ("telnet_2", "0.0.1"), ("telnet_3", "0.0.1"),
                      ("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"), ("cve_2016_10033_1", "0.0.1"),
                      ("samba_1", "0.0.1"), ("sql_injection_1", "0.0.1"), ("shellshock_1", "0.0.1"),
                      ("cve_2010_0426_1", "0.0.1"), ("cve_2015_5602_1", "0.0.1")
                      ]

    gw_vuln_compatible_containers = [("ssh_1", "0.0.1"), ("ssh_2", "0.0.1"), ("ssh_3", "0.0.1"), ("telnet_1", "0.0.1"),
                                     ("telnet_2", "0.0.1"), ("telnet_3", "0.0.1"),
                                     ("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"),
                                     ("cve_2016_10033_1", "0.0.1"),
                                     ("samba_1", "0.0.1"), ("sql_injection_1", "0.0.1"),
                                     ("shellshock_1", "0.0.1")
                                     ]

    pw_vuln_compatible_containers = [("ssh_1", "0.0.1"), ("ssh_2", "0.0.1"), ("ssh_3", "0.0.1"), ("telnet_1", "0.0.1"),
                                     ("telnet_2", "0.0.1"), ("telnet_3", "0.0.1"), ("ftp_1", "0.0.1"), ("ftp_2", "0.0.1")
                                     ]
    rce_vuln_compatible_containers = [("cve_2015_1427_1", "0.0.1"), ("cve_2015_3306_1", "0.0.1"),
                                    ("cve_2016_10033_1", "0.0.1"),
                                     ("samba_1", "0.0.1"), ("sql_injection_1", "0.0.1"),
                                     ("shellshock_1", "0.0.1")
                                     ]
    sql_injection_vuln_compatible_containers = [("sql_injection_1", "0.0.1")]
    priv_esc_vuln_compatible_containers = [("cve_2010_0426_1", "0.0.1"), ("cve_2015_5602_1", "0.0.1")]

    agent_containers = [(("hacker_kali_1", "0.0.1"))]
    router_containers = [("router_1", "0.0.1"), ("router_2", "0.0.1")]
    container_env_config = ContainerEnvConfig(
        min_num_users=1, max_num_users=5, min_num_flags=1, max_num_flags=5, min_num_nodes=4, max_num_nodes=10,
        container_pool=container_pool, gw_vuln_compatible_containers=gw_vuln_compatible_containers,
        pw_vuln_compatible_containers=pw_vuln_compatible_containers,
        rce_vuln_compatible_containers=rce_vuln_compatible_containers,
        sql_injection_vuln_compatible_containers=sql_injection_vuln_compatible_containers,
        priv_esc_vuln_compatible_containers=priv_esc_vuln_compatible_containers,
        agent_containers=agent_containers, router_containers=router_containers,
        path=util.default_output_dir(), subnet_id_blacklist=set(), subnet_prefix="172.18."
    )
    EnvConfigGenerator.create_env(container_env_config)

# Creates the environment configuration
if __name__ == '__main__':
    config_exists = EnvConfigGenerator.config_exists(path=util.default_output_dir())
    if not config_exists:
        generate_config()
    else:
        print("Reusing existing configuration")
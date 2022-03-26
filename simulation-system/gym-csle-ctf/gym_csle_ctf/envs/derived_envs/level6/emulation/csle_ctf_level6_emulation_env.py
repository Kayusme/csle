from csle_common.dao.network.env_mode import EnvMode
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.dao.network.env_config import CSLEEnvConfig
from gym_csle_ctf.envs.csle_ctf_env import CSLECTFEnv
from gym_csle_ctf.envs_model.config.level_6.csle_ctf_level_6_base import CSLECTFLevel6Base
from gym_csle_ctf.envs_model.config.level_6.csle_ctf_level_6_v1 import CSLECTFLevel6V1
from gym_csle_ctf.envs_model.config.level_6.csle_ctf_level_6_v2 import CSLECTFLevel6V2
from gym_csle_ctf.envs_model.config.level_6.csle_ctf_level_6_v3 import CSLECTFLevel6V3
from gym_csle_ctf.envs_model.config.level_6.csle_ctf_level_6_v4 import CSLECTFLevel6V4


# -------- Base Version (for testing) ------------
class CSLECTFLevel6EmulationBaseEnv(CSLECTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6Base.attacker_all_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                      subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                      hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6Base.defender_all_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6Base.env_config(network_conf=network_conf,
                                                      attacker_action_conf=attacker_action_conf,
                                                      defender_action_conf=defender_action_conf,
                                                      emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super(CSLECTFLevel6EmulationBaseEnv, self).__init__(env_config=env_config)


# -------- Version 1 ------------

class CSLECTFLevel6Emulation1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V1.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V1.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
            env_config.attacker_filter_illegal_actions = False
            env_config.max_episode_length = 100
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class CSLECTFLevel6EmulationWithCosts1Env(CSLECTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V1.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V1.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V1.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class CSLECTFLevel6Emulation2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V2.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V2.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class CSLECTFLevel6EmulationWithCosts2Env(CSLECTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V2.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V2.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V2.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class CSLECTFLevel6Emulation3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V3.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V3.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class CSLECTFLevel6EmulationWithCosts3Env(CSLECTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V3.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V3.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V3.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class CSLECTFLevel6Emulation4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V4.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V4.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 0
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class CSLECTFLevel6EmulationWithCosts4Env(CSLECTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: CSLEEnvConfig, emulation_config: EmulationConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = CSLECTFLevel6Base.render_conf()
            if emulation_config is None:
                emulation_config = CSLECTFLevel6Base.emulation_config()
            emulation_config.ids_router = True
            emulation_config.ids_router_ip = CSLECTFLevel6Base.router_ip()
            network_conf = CSLECTFLevel6Base.network_conf()
            attacker_action_conf = CSLECTFLevel6V4.attacker_actions_conf(num_nodes=CSLECTFLevel6Base.num_nodes(),
                                                                subnet_mask=CSLECTFLevel6Base.subnet_mask(),
                                                                hacker_ip=CSLECTFLevel6Base.hacker_ip())
            defender_action_conf = CSLECTFLevel6V4.defender_actions_conf(
                num_nodes=CSLECTFLevel6Base.num_nodes(), subnet_mask=CSLECTFLevel6Base.subnet_mask())
            env_config = CSLECTFLevel6V4.env_config(network_conf=network_conf,
                                                    attacker_action_conf=attacker_action_conf,
                                                    defender_action_conf=defender_action_conf,
                                                    emulation_config=emulation_config, render_conf=render_config)
            env_config.attacker_alerts_coefficient = 1
            env_config.attacker_cost_coefficient = 1
            env_config.env_mode = EnvMode.EMULATION
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)
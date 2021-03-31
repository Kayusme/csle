from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.network.cluster_config import ClusterConfig
from gym_pycr_ctf.envs.pycr_ctf_env import PyCRCTFEnv
from gym_pycr_ctf.envs.config.level_5.pycr_ctf_level_5_base import PyCrCTFLevel5Base
from gym_pycr_ctf.envs.config.level_5.pycr_ctf_level_5_v1 import PyCrCTFLevel5V1
from gym_pycr_ctf.envs.config.level_5.pycr_ctf_level_5_v2 import PyCrCTFLevel5V2
from gym_pycr_ctf.envs.config.level_5.pycr_ctf_level_5_v3 import PyCrCTFLevel5V3
from gym_pycr_ctf.envs.config.level_5.pycr_ctf_level_5_v4 import PyCrCTFLevel5V4


# -------- Base Version (for testing) ------------
class PyCRCTFLevel5ClusterBaseEnv(PyCRCTFEnv):
    """
    Base version with all set of actions
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5Base.all_actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                                 subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                                 hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5Base.env_config(network_conf=network_conf, action_conf=action_conf,
                                                          cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 ------------

class PyCRCTFLevel5Cluster1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V1.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 1 with costs------------

class PyCRCTFLevel5ClusterWithCosts1Env(PyCRCTFEnv):
    """
    The simplest possible configuration, minimal set of actions. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V1.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V1.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 ------------

class PyCRCTFLevel5Cluster2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V2.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 2 with costs------------

class PyCRCTFLevel5ClusterWithCosts2Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V1. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V2.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V2.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 ------------

class PyCRCTFLevel5Cluster3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V3.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 3 with costs------------

class PyCRCTFLevel5ClusterWithCosts3Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V2. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V3.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V3.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 ------------

class PyCRCTFLevel5Cluster4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does not take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V4.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 0
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)


# -------- Version 4 with costs------------

class PyCRCTFLevel5ClusterWithCosts4Env(PyCRCTFEnv):
    """
    Slightly more set of actions than V3. Does take action costs into account.
    """
    def __init__(self, env_config: EnvConfig, cluster_config: ClusterConfig, checkpoint_dir : str):
        if env_config is None:
            render_config = PyCrCTFLevel5Base.render_conf()
            if cluster_config is None:
                cluster_config = PyCrCTFLevel5Base.cluster_conf()
            cluster_config.ids_router = True
            cluster_config.ids_router_ip = PyCrCTFLevel5Base.router_ip()
            network_conf = PyCrCTFLevel5Base.network_conf()
            action_conf = PyCrCTFLevel5V4.actions_conf(num_nodes=PyCrCTFLevel5Base.num_nodes(),
                                                           subnet_mask=PyCrCTFLevel5Base.subnet_mask(),
                                                           hacker_ip=PyCrCTFLevel5Base.hacker_ip())
            env_config = PyCrCTFLevel5V4.env_config(network_conf=network_conf, action_conf=action_conf,
                                                        cluster_conf=cluster_config, render_conf=render_config)
            env_config.alerts_coefficient = 1
            env_config.cost_coefficient = 1
            env_config.env_mode = EnvMode.CLUSTER
            env_config.save_trajectories = False
            env_config.checkpoint_dir = checkpoint_dir
            env_config.checkpoint_freq = 1000
        super().__init__(env_config=env_config)
import os
from gym_pycr_pwcrack.agents.config.pg_agent_config import PolicyGradientAgentConfig
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.dao.agent.agent_type import AgentType
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.network.cluster_config import ClusterConfig

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    pg_agent_config = PolicyGradientAgentConfig(gamma=0.99, alpha=0.00005, epsilon=1, render=False, eval_sleep=0.0,
                                                min_epsilon=0.01, eval_episodes=1, train_log_frequency=1,
                                                epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                                                video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                                                num_iterations=1000000000,
                                                eval_render=False, gifs=True,
                                                gif_dir=util.default_output_dir() + "/results/gifs",
                                                eval_frequency=100, video_frequency=11,
                                                save_dir=util.default_output_dir() + "/results/data",
                                                checkpoint_freq=100, input_dim=6 * 30,
                                                output_dim=124,
                                                pi_hidden_dim=128, pi_hidden_layers=1,
                                                vf_hidden_dim=128, vf_hidden_layers=1,
                                                shared_hidden_layers=1, shared_hidden_dim=128,
                                                batch_size=8000,
                                                gpu=False, tensorboard=True,
                                                tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                                                optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                                                state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                                                lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.001,
                                                vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                                                eps_clip=0.2, optimization_iterations=10, mini_batch_size=64,
                                                render_steps=20, illegal_action_logit=-100
                                                )
    env_name = "pycr-pwcrack-simple-cluster-v1"
    cluster_config = ClusterConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                   server_connection=False)
    client_config = ClientConfig(env_name=env_name, pg_agent_config=pg_agent_config,
                                 agent_type=AgentType.PPO_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="PPO-Baseline v0",
                                 run_many=False, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, cluster_config=cluster_config)
    return client_config


def write_default_config(path:str = None) -> None:
    """
    Writes the default configuration to a json file

    :param path: the path to write the configuration to
    :return: None
    """
    if path is None:
        path = util.default_config_path()
    config = default_config()
    util.write_config_file(config, path)


# Program entrypoint
if __name__ == '__main__':

    args = util.parse_args(util.default_config_path())
    experiment_title = "PPO simple v1 cluster"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()
    if not config.run_many:
        util.run_experiment(config, config.random_seed)
    else:
        train_csv_paths = []
        eval_csv_paths = []
        for seed in config.random_seeds:
            if args.configpath is not None and not args.noconfig:
                if not os.path.exists(args.configpath):
                    write_default_config()
                config = util.read_config(args.configpath)
            else:
                config = default_config()
            train_csv_path, eval_csv_path = util.run_experiment(config, seed)
            train_csv_paths.append(train_csv_path)
            eval_csv_paths.append(eval_csv_path)

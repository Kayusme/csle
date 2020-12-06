import os
from gym_pycr_pwcrack.agents.config.agent_config import AgentConfig
from gym_pycr_pwcrack.dao.experiment.client_config import ClientConfig
from gym_pycr_pwcrack.dao.agent.agent_type import AgentType
from gym_pycr_pwcrack.util.experiments_util import util
from gym_pycr_pwcrack.dao.experiment.runner_mode import RunnerMode

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=0.999, alpha=0.001, epsilon=1, render=False, eval_sleep=0.9,
                                                min_epsilon=0.01, eval_episodes=10, train_log_frequency=1,
                                                epsilon_decay=0.9999, video=True, eval_log_frequency=1,
                                                video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                                                num_episodes=1000000,
                                                eval_render=False, gifs=True,
                                                gif_dir=util.default_output_dir() + "/results/gifs",
                                                eval_frequency=10000, video_frequency=11,
                                                save_dir=util.default_output_dir() + "/results/data",
                                                checkpoint_freq=1000, input_dim=180,
                                                output_dim=23,
                                                pi_hidden_dim=32,
                                                pi_hidden_layers=1, batch_size=8,
                                                gpu=True, tensorboard=True,
                                                tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                                                optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                                                state_length=1, gpu_id=0)
    env_name = "pycr-pwcrack-level-1-sim-v1"
    client_config = ClientConfig(env_name=env_name, agent_config=agent_config,
                                 agent_type=AgentType.REINFORCE.value,
                                 output_dir=util.default_output_dir(),
                                 title="REINFORCE level_1 v1",
                                 run_many=False, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, mode=RunnerMode.TRAIN_ATTACKER.value)
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
    experiment_title = "REINFORCE level_1 v1"
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

import os
import glob
from pycr_common.agents.config.agent_config import AgentConfig
from pycr_common.dao.experiment.client_config import ClientConfig
from pycr_common.dao.agent.agent_type import AgentType
from pycr_common.util.experiments_util import util
import pycr_common.util.plots as plotting_util
from pycr_common.dao.network.emulation_config import EmulationConfig
from pycr_common.dao.experiment.runner_mode import RunnerMode
from pycr_common.dao.agent.train_mode import TrainMode

def default_config() -> ClientConfig:
    """
    :return: Default configuration for the experiment
    """
    agent_config = AgentConfig(gamma=0.0, alpha=0.001, epsilon=1, render=False, eval_sleep=0.0,
                               min_epsilon=0.01, eval_episodes=2, train_log_frequency=500,
                               epsilon_decay=0.9999, video=False, eval_log_frequency=1,
                               video_fps=5, video_dir=util.default_output_dir() + "/results/videos",
                               num_iterations=100000,
                               eval_render=True, gifs=True,
                               gif_dir=util.default_output_dir() + "/results/gifs",
                               eval_frequency=200, video_frequency=10,
                               save_dir=util.default_output_dir() + "/results/data",
                               checkpoint_freq=500, input_dim=5 * 8,
                               output_dim=22,
                               pi_hidden_dim=64, pi_hidden_layers=1,
                               vf_hidden_dim=64, vf_hidden_layers=1,
                               shared_hidden_layers=2, shared_hidden_dim=64,
                               batch_size=200,
                               gpu=False, tensorboard=True,
                               tensorboard_dir=util.default_output_dir() + "/results/tensorboard",
                               optimizer="Adam", lr_exp_decay=False, lr_decay_rate=0.999,
                               state_length=1, gpu_id=0, sde_sample_freq=4, use_sde=False,
                               lr_progress_decay=False, lr_progress_power_decay=4, ent_coef=0.001,
                               vf_coef=0.5, features_dim=512, gae_lambda=0.95, max_gradient_norm=0.5,
                               eps_clip=0.2, optimization_iterations=10,
                               render_steps=100, illegal_action_logit=-100,
                               buffer_size=1000000,
                               tau=1.0, learning_starts=5000, train_freq=4, gradient_steps=1,
                               target_update_interval=5000, exploration_fraction=0.99,
                               exploration_initial_eps=1.0, exploration_final_eps=0.05,
                               filter_illegal_actions=True, train_progress_deterministic_eval=True,
                               n_deterministic_eval_iter=10
                               )
    # env_name = "pycr-ctf-level-1-emulation-v1"
    env_name = "pycr-ctf-level-1-emulation-costs-v1"
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False, warmup=True, warmup_iterations=500,
                                     port_forward_next_port=3000)
    client_config = ClientConfig(env_name=env_name, attacker_agent_config=agent_config,
                                 agent_type=AgentType.DQN_BASELINE.value,
                                 output_dir=util.default_output_dir(),
                                 title="DQN-Baseline v1",
                                 run_many=False, random_seeds=[0, 999, 299, 399, 499],
                                 random_seed=399, emulation_config=emulation_config,
                                 mode=RunnerMode.TRAIN_ATTACKER.value, train_mode=TrainMode.TRAIN_ATTACKER)
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

    # Setup
    args = util.parse_args(util.default_config_path())
    experiment_title = "DQN level_1 v1 emulation"
    if args.configpath is not None and not args.noconfig:
        if not os.path.exists(args.configpath):
            write_default_config()
        config = util.read_config(args.configpath)
    else:
        config = default_config()

    # Plot
    if args.plotonly:
        if args.csvfile is not None:
            plotting_util.plot_csv_files([args.csvfile],
                                        config.output_dir + "/results/plots/" + str(config.random_seed) + "/")
        elif config.run_many:
            csv_files = []
            for seed in config.random_seeds:
                p = glob.glob(config.output_dir + "/results/data/" + str(seed) + "/*_train.csv")[0]
                csv_files.append(p)
            plotting_util.plot_csv_files(csv_files, config.output_dir + "/results/plots/")
        else:
            p = glob.glob(config.output_dir + "/results/data/" + str(config.random_seed) + "/*_train.csv")[0]
            plotting_util.plot_csv_files([p], config.output_dir + "/results/plots/" + str(config.random_seed) + "/")

    # Run experiment
    else:
        if not config.run_many:
            train_csv_path, eval_csv_path = util.run_experiment(config, config.random_seed)
            if train_csv_path is not None and not train_csv_path == "":
                plotting_util.plot_csv_files([train_csv_path], config.output_dir + "/results/plots/"
                                             + str(config.random_seed)+ "/")
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

            plotting_util.plot_csv_files(train_csv_paths, config.output_dir + "/results/plots/")
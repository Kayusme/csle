from csle_common.dao.network.emulation_config import EmulationConfig
import gym
import numpy as np
from csle_common.util.experiments_util import util


def test_env(env_name : str, num_steps : int):
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/csle_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/")
    # eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/")
    # eval_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/")

    # containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/backup/random_many/")
    # flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_2/backup/random_many/")
    # eval_containers_configs = EnvConfigGenerator.get_all_envs_containers_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/backup/random_many_2/")
    # eval_env_flags_configs = EnvConfigGenerator.get_all_envs_flags_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many/backup/random_many_2/")


    # containers_config = util.read_containers_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random/containers.json")
    # flags_config = util.read_flags_config(
    #     "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random/flags.json")
    containers_config = util.read_containers_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/env_16_172.18.20./containers.json")
    flags_config = util.read_flags_config(
        "/home/kim/storage/workspace/csle/emulation-system/minigames/network_intrusion/ctf/001/random_many_train/env_16_172.18.20./flags.json")
    # max_num_nodes_train = max(list(map(lambda x: len(x.containers), containers_config)))
    # max_num_nodes_eval = max(list(map(lambda x: len(x.containers), flags_config)))
    # max_num_nodes = max(max_num_nodes_train, max_num_nodes_eval)
    max_num_nodes = len(containers_config.containers)
    #
    # emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
    #                                  port_forward_next_port=9650,
    #                                  server_connection=False, warmup=True, warmup_iterations=500
    #                                  )

    emulation_config = EmulationConfig(agent_ip=containers_config.agent_ip, agent_username="agent", agent_pw="agent",
                                   port_forward_next_port=9600,
                                   server_connection=True, server_private_key_file="/home/kim/.ssh/id_rsa",
                                   server_username="kim", server_ip="172.31.212.92",
                                   warmup=True, warmup_iterations=500
                                   )

    env = gym.make(env_name, env_config=None, emulation_config=emulation_config,
                   containers_config=containers_config, flags_config=flags_config, num_nodes=max_num_nodes)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()

    num_actions = env.env_config.attacker_action_conf.num_actions
    actions = np.array(list(range(num_actions)))
    print("num actions:{}".format(num_actions))
    tot_rew = 0
    for i in range(num_steps):
        print(i)
        legal_actions = list(filter(lambda x: env.is_attack_action_legal(x, env.env_config, env.env_state), actions))
        action = np.random.choice(legal_actions)
        obs, reward, done, info = env.step(action)
        tot_rew += reward
        #env.render()
        if done:
            print("done")
            tot_rew = 0
            env.reset()
        #time.sleep(0.001)
        #time.sleep(0.5)
    env.reset()
    env.close()


def test_all():
    #test_env("csle-ctf-random-emulation-v1", num_steps=1000000000)
    test_env("csle-ctf-random-emulation-v1", num_steps=1000000000)
    #csle-ctf-random-generated-sim-v1

if __name__ == '__main__':
    test_all()
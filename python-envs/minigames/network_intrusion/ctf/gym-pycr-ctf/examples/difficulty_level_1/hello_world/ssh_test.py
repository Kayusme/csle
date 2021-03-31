from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.envs.logic.emulation.util.emulation_util import EmulationUtil
import gym
import time
import numpy as np

def test_env(env_name : str, num_steps : int):
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.1.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username="agent", agent_pw="agent",
                                     server_connection=False)
    env = gym.make(env_name, env_config=None, emulation_config=emulation_config)
    env.env_config.max_episode_length = 1000000000
    env.env_config.manual_play = True

    env.reset()
    sftp_client = emulation_config.agent_conn.open_sftp()
    remote_file = sftp_client.file("/home/agent/test", mode="a")
    remote_file.write("test!\n")
    remote_file.write("test2!\n")
    remote_file.close()

    # cmd = "sudo find / -name 'flag*.txt'  2>&1 | grep -v 'Permission denied'"
    # for i in range(100):
    #     outdata, errdata, total_time = emulationUtil.execute_ssh_cmd(cmd=cmd, conn=emulation_config.agent_conn)
    #     flags = outdata.decode().split("\n")
    #     print("outdata:{}".format(flags))
        # if "flag191.txt" not in outdata:
        #     print("error: {}".format(outdata))

    # num_actions = env.env_config.action_conf.num_actions
    # actions = np.array(list(range(num_actions)))
    # print("num actions:{}".format(num_actions))
    # for i in range(num_steps):
    #     legal_actions = list(filter(lambda x: env.is_action_legal(x, env.env_config, env.env_state), actions))
    #     action = np.random.choice(legal_actions)
    #     obs, reward, done, info = env.step(action)
    #     env.render()
    #     if done:
    #         env.reset()
    #     #time.sleep(0.001)
    #     #time.sleep(0.5)
    # env.reset()
    # env.close()


def test_all():
    #test_env("pycr-ctf-level-1-sim-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-1-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-1-emulation-v2", num_steps=1000000000)
    #test_env("pycr-ctf-level-1-emulation-base-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-1-emulation-v3", num_steps=1000000000)
    test_env("pycr-ctf-level-1-emulation-v1", num_steps=1000000000)
    #test_env("pycr-ctf-level-1-generated-sim-v1", num_steps=1000000000)

if __name__ == '__main__':
    test_all()
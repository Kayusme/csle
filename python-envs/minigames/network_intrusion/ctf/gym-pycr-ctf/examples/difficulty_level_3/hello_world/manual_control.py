from gym_pycr_ctf.envs.derived_envs.level1.simulation.pycr_ctf_level1_sim_env import PyCRCTFLevel1Sim1Env
from gym_pycr_ctf.envs.derived_envs.level1.emulation.pycr_ctf_level1_emulation_env import PyCRCTFLevel1Emulation1Env
from gym_pycr_ctf.dao.network.emulation_config import EmulationConfig
from gym_pycr_ctf.agents.manual.manual_attacker_agent import ManualAttackerAgent
import gym

def manual_control():
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(server_ip="172.31.212.91", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    # emulation_config = emulationConfig(agent_ip="172.18.3.191", agent_username="agent", agent_pw="agent",
    #                                server_connection=False)
    # emulation_config = emulationConfig(server_ip="172.31.212.92", agent_ip="172.18.3.191",
    #                                agent_username="agent", agent_pw="agent", server_connection=True,
    #                                server_private_key_file="/home/kim/.ssh/id_rsa",
    #                                server_username="kim")
    emulation_config = EmulationConfig(server_ip="172.31.212.92", agent_ip="172.18.3.191",
                                     agent_username="agent", agent_pw="agent", server_connection=True,
                                     server_private_key_file="/Users/kimham/.ssh/pycr_id_rsa",
                                     server_username="kim")

    #env = gym.make("pycr-ctf-level-2-emulation-base-v1", env_config=None, emulation_config=emulation_config)
    env = gym.make("pycr-ctf-level-3-emulation-v4", env_config=None, emulation_config=emulation_config)
    #env = gym.make("pycr-ctf-level-2-sim-v1", env_config=None, emulation_config=emulation_config)

    #env = gym.make("pycr-ctf-level-2-sim-base-v1", env_config=None)
    ManualAttackerAgent(env=env, env_config=env.env_config)




if __name__ == '__main__':
    manual_control()
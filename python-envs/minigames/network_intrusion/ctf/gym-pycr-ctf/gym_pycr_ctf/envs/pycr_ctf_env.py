from typing import Tuple
import gym
import pickle
from abc import ABC
import numpy as np
import os
import sys
from gym_pycr_ctf.dao.network.env_config import EnvConfig
from gym_pycr_ctf.dao.agent.attacker_agent_state import AttackerAgentState
from gym_pycr_ctf.dao.network.env_state import EnvState
from gym_pycr_ctf.dao.agent.agent_log import AgentLog
import gym_pycr_ctf.constants.constants as constants
from gym_pycr_ctf.envs_model.logic.transition_operator import TransitionOperator
from gym_pycr_ctf.dao.network.env_mode import EnvMode
from gym_pycr_ctf.dao.action.attacker.attacker_action import AttackerAction
from gym_pycr_ctf.dao.action.attacker.attacker_action_type import AttackerActionType
from gym_pycr_ctf.dao.action.attacker.attacker_action_id import AttackerActionId
from gym_pycr_ctf.envs_model.logic.common.env_dynamics_util import EnvDynamicsUtil
import gym_pycr_ctf.envs_model.logic.common.util as util
from gym_pycr_ctf.envs_model.logic.emulation.system_id.simulation_generator import SimulationGenerator
from gym_pycr_ctf.envs_model.logic.exploration.random_exploration_policy import RandomExplorationPolicy
from gym_pycr_ctf.envs_model.logic.emulation.warmup.emulation_warmup import EmulationWarmup
from gym_pycr_ctf.envs_model.logic.common.domain_randomizer import DomainRandomizer
from gym_pycr_ctf.envs_model.logic.simulation.find_pi_star import FindPiStar

class PyCRCTFEnv(gym.Env, ABC):
    """
    Abstract OpenAI Gym Env for the PyCr CTF minigame
    """

    def __init__(self, env_config : EnvConfig, rs = None):
        self.env_config = env_config
        if util.is_network_conf_incomplete(env_config) and self.env_config.env_mode == EnvMode.SIMULATION:
            raise ValueError("Must provide a simulation model to run in simulation mode")

        # Initialize environment state
        self.env_state = EnvState(env_config=self.env_config, num_ports=self.env_config.attacker_num_ports_obs,
                                  num_vuln=self.env_config.attacker_num_vuln_obs, num_sh=self.env_config.attacker_num_sh_obs,
                                  num_nodes=env_config.num_nodes,
                                  service_lookup=constants.SERVICES.service_lookup,
                                  vuln_lookup=constants.VULNERABILITIES.vuln_lookup,
                                  os_lookup=constants.OS.os_lookup, num_flags=self.env_config.num_flags,
                                  state_type=self.env_config.state_type,
                                  ids=env_config.ids_router)

        # Setup Attacker Spaces
        self.attacker_observation_space = self.env_state.attacker_observation_space
        self.attacker_m_selection_observation_space = self.env_state.attacker_m_selection_observation_space
        self.attacker_m_action_observation_space = self.env_state.attacker_m_action_observation_space
        self.attacker_action_space = self.env_config.attacker_action_conf.action_space
        self.attacker_m_selection_action_space = gym.spaces.Discrete(self.env_state.attacker_obs_state.num_machines + 1)
        self.attacker_m_action_space = self.env_config.attacker_action_conf.m_action_space
        self.attacker_num_actions = self.env_config.attacker_action_conf.num_actions
        self.attacker_network_orig_shape = self.env_state.attacker_network_orig_shape
        self.attacker_machine_orig_shape = self.env_state.attacker_machine_orig_shape

        # Setup Defender Spaces
        self.defender_observation_space = self.env_state.defender_observation_space

        # Setup Config
        self.env_config.pi_star_rew_list_attacker = []
        self.reward_range = (float(0), float(1))
        self.num_states = 100
        self.idx = self.env_config.idx
        self.viewer = None
        self.randomization_space = rs
        self.steps_beyond_done = None
        self.metadata = {
            'render.modes': ['human', 'rgb_array'],
            'video.frames_per_second': 50  # Video rendering speed
        }
        self.step_outcome = None

        # System Identification
        if self.env_config.env_mode == EnvMode.emulation or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION:

            # Connect to emulation
            self.env_config.emulation_config.connect_agent()

            if self.env_config.defender_update_state:
                # Initialize Defender's state
                self.env_state.initialize_defender_state()

            if self.env_config.load_services_from_server:
                self.env_config.emulation_config.download_emulation_services()
            self.env_state.merge_services_with_emulation(self.env_config.emulation_config.emulation_services)
            if self.env_config.load_cves_from_server:
                self.env_config.emulation_config.download_cves()
            self.env_state.merge_cves_with_emulation(self.env_config.emulation_config.emulation_cves)
            self.env_config.attacker_action_costs = self.env_config.emulation_config.load_action_costs(
                actions=self.env_config.attacker_action_conf.actions, dir=self.env_config.nmap_cache_dir,
                nmap_ids=self.env_config.attacker_action_conf.nmap_action_ids,
                network_service_ids=self.env_config.attacker_action_conf.network_service_action_ids,
                shell_ids=self.env_config.attacker_action_conf.shell_action_ids,
                nikto_ids=self.env_config.attacker_action_conf.nikto_action_ids,
                masscan_ids=self.env_config.attacker_action_conf.masscan_action_ids,
                action_lookup_d_val = self.env_config.attacker_action_conf.action_lookup_d_val)
            self.env_config.attacker_action_alerts = self.env_config.emulation_config.load_action_alerts(
                actions=self.env_config.attacker_action_conf.actions, dir=self.env_config.nmap_cache_dir,
                action_ids=self.env_config.attacker_action_conf.action_ids,
                action_lookup_d_val=self.env_config.attacker_action_conf.action_lookup_d_val,
                shell_ids=self.env_config.attacker_action_conf.shell_action_ids)

        self.env_config.scale_rewards_prep_attacker()
        self.env_config.scale_rewards_prep_defender()
        self.attacker_agent_state = AttackerAgentState(attacker_obs_state=self.env_state.attacker_obs_state, env_log=AgentLog(),
                                                       service_lookup=self.env_state.service_lookup,
                                                       vuln_lookup=self.env_state.vuln_lookup,
                                                       os_lookup=self.env_state.os_lookup)

        # Setup Attacker Trajectories
        self.attacker_last_obs = self.env_state.get_attacker_observation()
        self.attacker_trajectory = []
        self.attacker_trajectories = []

        # Setup Defender Trajectories
        self.defender_last_obs = self.env_state.get_attacker_observation()
        self.defender_trajectory = []
        self.defender_trajectories = []
        self.defender_time_step = 0

        # Warmup in the emulation
        if self.env_config.emulation_config is not None and self.env_config.emulation_config.warmup \
                and (self.env_config.env_mode == EnvMode.GENERATED_SIMULATION or self.env_config.env_mode == EnvMode.emulation):
            EmulationWarmup.warmup(exp_policy=RandomExplorationPolicy(num_actions=env_config.attacker_action_conf.num_actions),
                                   num_warmup_steps=env_config.emulation_config.warmup_iterations,
                                   env=self, render = False)
            print("[Warmup complete], nmap_cache_size:{}, fs_cache_size:{}, user_command_cache:{}, nikto_scan_cache:{},"
                  "cache_misses:{}".format(
                len(self.env_config.attacker_nmap_scan_cache.cache),
                len(self.env_config.attacker_filesystem_scan_cache.cache),
                len(self.env_config.attacker_user_command_cache.cache),
                len(self.env_config.attacker_nikto_scan_cache.cache),
                self.env_config.cache_misses))
        if self.env_config.env_mode == EnvMode.GENERATED_SIMULATION \
                and not self.env_config.emulation_config.skip_exploration:
            self.env_config.network_conf, obs_state = SimulationGenerator.build_model(
                exp_policy=env_config.attacker_exploration_policy, env_config=self.env_config, env=self)
            self.env_state.attacker_obs_state = obs_state
            self.env_config.env_mode = EnvMode.SIMULATION
            self.randomization_space = DomainRandomizer.generate_randomization_space([self.env_config.network_conf])
            self.env_config.emulation_config.connect_agent()
            self.reset()

        # Reset and setup action spaces
        self.reset()
        actions = list(range(self.attacker_num_actions))
        self.attacker_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
                    action, env_config=self.env_config, env_state=self.env_state), actions))
        self.defender_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_defense_action_legal(
            action, env_config=self.env_config, env_state=self.env_state), actions))

        if (self.env_config.env_mode == EnvMode.SIMULATION
            or self.env_config.env_mode == EnvMode.GENERATED_SIMULATION) \
                and self.env_config.compute_pi_star_attacker:

            if not self.env_config.use_upper_bound_pi_star_attacker:
                pi_star_tau_attacker, pi_star_rew_attacker = FindPiStar.brute_force(self.env_config, self)
                self.env_config.pi_star_tau_attacker = pi_star_tau_attacker
                self.env_config.pi_star_rew_attacker = pi_star_rew_attacker
                self.env_config.pi_star_rew_list_attacker.append(pi_star_rew_attacker)

        if self.env_config.use_upper_bound_pi_star_attacker:
            self.env_config.pi_star_rew_attacker = FindPiStar.upper_bound_pi(self.env_config)
            self.env_config.pi_star_tau_attacker = None
            self.env_config.pi_star_rew_list_attacker.append(self.env_config.pi_star_rew_attacker)

    # -------- API ------------
    def step(self, action_id : Tuple[int, int]) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment by executing the given action

        :param action_id: the action to take
        :return: (obs, reward, done, info)
        """

        # Initialization
        attack_action_id, defense_action_id = action_id
        attacker_reward = 0
        defender_reward = 0
        attacker_obs = None
        defender_obs = None
        done = False

        # First step attacker
        if attack_action_id is not None:
            attacker_m_obs, attacker_reward, done, info = self.step_attacker(attacker_action_id=attack_action_id)

        # Second step defender
        if defense_action_id is not None:
            defender_obs, attacker_m_obs_2, defender_reward, attacker_reward_2, done, info = \
                self.step_defender(defender_action_id=defense_action_id, done_attacker=done)
            attacker_reward = attacker_reward + attacker_reward_2
            attacker_m_obs = attacker_m_obs_2

        return (attacker_m_obs, defender_obs), (attacker_reward, defender_reward), done, info

    def step_attacker(self, attacker_action_id) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment as the attacker by executing the given action

        :param attacker_action_id: the action to take
        :return: (obs, reward, done, info)
        """

        # Update trajecotry
        self.attacker_trajectory = []
        self.attacker_trajectory.append(self.attacker_last_obs)
        self.attacker_trajectory.append(attacker_action_id)
        info = {"idx": self.idx}

        # Check if action is illegal
        if not self.is_attack_action_legal(attacker_action_id, env_config=self.env_config, env_state=self.env_state):
            print("illegal attack action:{}, idx:{}".format(attacker_action_id, self.idx))
            actions = list(range(len(self.env_config.attacker_action_conf.actions)))
            attacker_non_legal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
                action, env_config=self.env_config, env_state=self.env_state), actions))
            print("true illegal attack actions:{}, idx:{}".format(attacker_non_legal_actions, self.idx))
            attacker_legal_actions = list(filter(lambda action: PyCRCTFEnv.is_attack_action_legal(
                action, env_config=self.env_config, env_state=self.env_state), actions))
            print("true legal attack actions:{}, idx:{}".format(attacker_legal_actions, self.idx))
            print("flags found:{}, idx:{}".format(self.env_state.num_flags, self.idx))
            print("flags found:{}, idx:{}".format(
                list(map(lambda x: x.flags_found, self.env_state.attacker_obs_state.machines)), self.idx))
            print("flags found:{}, idx:{}".format(self.env_state.attacker_obs_state.catched_flags, self.idx))
            print("total flags:{}, idx:{}".format(self.env_config.network_conf.flags_lookup, self.idx))
            print(self.env_config.network_conf)
            print("Idx:{}".format(self.idx))
            # self.env_config.network_conf.save("./netconf" + str(self.idx) + ".pkl")
            raise ValueError("Test")
            sys.exit(0)
            done = False
            info["flags"] = self.env_state.attacker_obs_state.catched_flags
            self.agent_state.time_step += 1
            if self.agent_state.time_step > self.env_config.max_episode_length:
                done = True
            return self.attacker_last_obs, self.env_config.illegal_reward_action, done, info
        if attacker_action_id > len(self.env_config.attacker_action_conf.actions) - 1:
            raise ValueError("Action ID: {} not recognized".format(attacker_action_id))

        # Prepare action for execution
        attack_action = self.env_config.attacker_action_conf.actions[attacker_action_id]
        attack_action.ip = self.env_state.attacker_obs_state.get_action_ip(attack_action)

        # Step in the environment
        s_prime, attacker_reward, done = TransitionOperator.attacker_transition(
            s=self.env_state, attacker_action=attack_action, env_config=self.env_config)

        # Parse result of action
        if done:
            attacker_reward = attacker_reward - self.env_config.attacker_final_steps_reward_coefficient * self.attacker_agent_state.time_step
        if self.attacker_agent_state.time_step > self.env_config.max_episode_length:
            done = True
        self.env_state = s_prime
        if self.env_state.attacker_obs_state.detected:
            attacker_reward = attacker_reward - self.env_config.attacker_detection_reward
        attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()
        self.attacker_last_obs = attacker_m_obs
        self.attacker_agent_state.time_step += 1
        self.attacker_agent_state.episode_reward += attacker_reward
        self.__update_log(attack_action)
        self.attacker_trajectory.append(attacker_m_obs)
        self.attacker_trajectory.append(attacker_reward)
        info["flags"] = self.env_state.attacker_obs_state.catched_flags
        if self.env_config.save_trajectories:
            self.attacker_trajectories.append(self.attacker_trajectory)

        return attacker_m_obs, attacker_reward, done, info

    def step_defender(self, defender_action_id, done_attacker : bool = False) -> Tuple[np.ndarray, int, bool, dict]:
        """
        Takes a step in the environment as the defender by executing the given action

        :param defender_action_id: the action to take
        :param done_attacker: whether the environment completed after attacker action
        :return: (obs, reward, done, info)
        """

        if done_attacker:
            defender_m_obs, defender_network_obs = self.env_state.get_defender_observation()
            attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()
            defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
            return defender_obs, attacker_m_obs, self.env_config.defender_intrusion_reward, 0, True, {}

        # Update trajectory
        self.defender_trajectory = []
        self.defender_trajectory.append(self.defender_last_obs)
        self.defender_trajectory.append(defender_action_id)
        info = {"idx": self.idx}
        if not self.is_defense_action_legal(defender_action_id, env_config=self.env_config, env_state=self.env_state):
            print("illegal defense action:{}, idx:{}".format(defender_action_id, self.idx))
            sys.exit(0)
            done = False
            return self.defender_last_obs, self.env_config.illegal_reward_action, done, info

        # Prepare action for execution in the environment
        if defender_action_id > len(self.env_config.defender_action_conf.actions) - 1:
            raise ValueError("Action ID: {} not recognized".format(defender_action_id))
        defense_action = self.env_config.defender_action_conf.actions[defender_action_id]
        defense_action.ip = self.env_state.defender_obs_state.get_action_ip(defense_action)

        # Step in the environment
        s_prime, defender_reward, done = TransitionOperator.defender_transition(
            s=self.env_state, defender_action=defense_action, env_config=self.env_config)

        # Parse result
        attacker_reward = 0
        if done:
            defender_reward = defender_reward - \
                              self.env_config.defender_final_steps_reward_coefficient * \
                              self.defender_time_step
        if self.defender_time_step > self.env_config.max_episode_length:
            done = True

        self.env_state = s_prime

        if self.env_state.defender_obs_state.caught_attacker:
            defender_reward = defender_reward + self.env_config.defender_caught_attacker_reward
            attacker_reward = self.env_config.attacker_detection_reward
        elif self.env_state.defender_obs_state.stopped:
            defender_reward = defender_reward + self.env_config.defender_early_stopping

        defender_m_obs, defender_network_obs = self.env_state.get_defender_observation()
        attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()

        defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
        self.defender_last_obs = defender_obs
        self.defender_time_step += 1
        self.defender_trajectory.append(defender_obs)
        self.defender_trajectory.append(defender_reward)
        if self.env_config.save_trajectories:
            self.defender_trajectories.append(self.defender_trajectory)

        return defender_obs, attacker_m_obs, defender_reward, attacker_reward, done, info

    def reset(self, soft : bool = False) -> np.ndarray:
        """
        Resets the environment state, this should be called whenever step() returns <done>

        :return: initial observation
        """
        if not soft and self.env_config.env_mode == EnvMode.SIMULATION \
                and self.env_config.domain_randomization and self.randomization_space is not None:
            randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                             network_ids=list(range(1, 254)),
                                                                             r_space=self.randomization_space,
                                                                             env_config=self.env_config)
            self.env_config = env_config
            if self.env_config.compute_pi_star:
                if not self.env_config.use_upper_bound_pi_star:
                    attacker_pi_star_tau, attacker_pi_star_rew = FindPiStar.brute_force(self.env_config, self)
                else:
                    attacker_pi_star_rew = FindPiStar.upper_bound_pi(self.env_config)
                    attacker_pi_star_tau = None
                self.env_config.pi_star_tau = attacker_pi_star_tau
                self.env_config.pi_star_rew = attacker_pi_star_rew
                self.env_config.pi_star_rew_list.append(attacker_pi_star_rew)
            total_attacker_actions = list(range(self.attacker_num_actions))
            self.attacker_initial_illegal_actions = list(filter(lambda attack_action: not PyCRCTFEnv.is_attack_action_legal(
                attack_action, env_config=self.env_config,
                env_state=self.env_state), total_attacker_actions))

        self.__checkpoint_log()
        self.__checkpoint_trajectories()
        if self.env_state.attacker_obs_state.detected:
            self.attacker_agent_state.num_detections += 1
        elif self.env_state.attacker_obs_state.all_flags:
            self.attacker_agent_state.num_all_flags += 1
        self.env_state.reset_state()
        attacker_m_obs, attacker_p_obs = self.env_state.get_attacker_observation()
        defender_m_obs, defender_network_obs = self.env_state.get_defender_observation()
        defender_obs = np.append(defender_network_obs, defender_m_obs.flatten())
        self.attacker_last_obs = attacker_m_obs
        self.attacker_agent_state.num_episodes += 1
        self.attacker_agent_state.cumulative_reward += self.attacker_agent_state.episode_reward
        self.attacker_agent_state.time_step = 0
        self.attacker_agent_state.episode_reward = 0
        self.defender_time_step = 0
        self.attacker_agent_state.env_log.reset()
        self.attacker_agent_state.attacker_obs_state = self.env_state.attacker_obs_state
        #self.viewer.mainframe.set_state(self.agent_state)
        if self.viewer is not None and self.viewer.mainframe is not None:
            self.viewer.mainframe.reset_state()
        if self.env_config.env_mode == EnvMode.SIMULATION:
            self.env_state.attacker_obs_state.agent_reachable = self.env_config.network_conf.agent_reachable
        self.env_config.cache_misses = 0
        sys.stdout.flush()
        return attacker_m_obs, defender_obs

    def render(self, mode: str = 'human'):
        """
        Renders the environment
        Supported rendering modes:
        - human: render to the current display or terminal and
          return nothing. Usually for human consumption.
        - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
          representing RGB values for an x-by-y pixel image, suitable
          for turning into a video.
        :param mode: the rendering mode
        :return: True (if human mode) otherwise an rgb array
        """
        #self.agent_state.attacker_obs_state = self.env_state.attacker_obs_state.copy()
        self.attacker_agent_state.attacker_obs_state = self.env_state.attacker_obs_state
        if mode not in self.metadata["render.modes"]:
            raise NotImplemented("mode: {} is not supported".format(mode))
        if self.viewer is None:
            self.__setup_viewer()
        self.viewer.mainframe.set_state(self.attacker_agent_state)
        arr = self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return arr

    def randomize(self):
        randomized_network_conf, env_config = DomainRandomizer.randomize(subnet_prefix="172.18.",
                                                                         network_ids=list(range(1, 254)),
                                                                         r_space=self.randomization_space,
                                                                         env_config=self.env_config)
        self.env_config = env_config
        attacker_total_actions = list(range(self.attacker_num_actions))
        self.attacker_initial_illegal_actions = list(filter(lambda action: not PyCRCTFEnv.is_attack_action_legal(
            action, env_config=self.env_config, env_state=self.env_state), attacker_total_actions))

    @staticmethod
    def is_defense_action_legal(defense_action_id: int, env_config: EnvConfig, env_state: EnvState) -> bool:
        """
        Checks if a given defense action is legal in the current state of the environment

        :param defense_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal, else false
        """
        return True

    @staticmethod
    def is_attack_action_legal(attack_action_id : int, env_config: EnvConfig, env_state: EnvState, m_selection: bool = False,
                               m_action: bool = False, m_index : int = None) -> bool:
        """
        Checks if a given attack action is legal in the current state of the environment

        :param attack_action_id: the id of the action to check
        :param env_config: the environment config
        :param env_state: the environment state
        :param m_selection: boolean flag whether using AR policy m_selection or not
        :param m_action: boolean flag whether using AR policy m_action or not
        :param m_index: index of machine in case using AR policy
        :return: True if legal, else false
        """
        # If using AR policy
        if m_selection:
            return PyCRCTFEnv._is_attack_action_legal_m_selection(action_id=attack_action_id, env_config=env_config,
                                                                  env_state=env_state)
        elif m_action:
            return PyCRCTFEnv._is_attack_action_legal_m_action(action_id=attack_action_id, env_config=env_config,
                                                               env_state=env_state, machine_index=m_index)

        if not env_config.attacker_filter_illegal_actions:
            return True
        if attack_action_id > len(env_config.attacker_action_conf.actions) - 1:
            return False

        action = env_config.attacker_action_conf.actions[attack_action_id]
        ip = env_state.attacker_obs_state.get_action_ip(action)

        logged_in_ips_str = EnvDynamicsUtil.logged_in_ips_str(env_config=env_config, a=action, s=env_state)
        if (action.id, action.index, logged_in_ips_str) in env_state.attacker_obs_state.actions_tried:
            return False

        # Recon on subnet is always possible
        if action.type == AttackerActionType.RECON and action.subnet:
            return True

        # Recon on set of all found machines is always possible if there exists such machiens
        if action.type == AttackerActionType.RECON and action.index == -1 and len(env_state.attacker_obs_state.machines) > 0:
            return True

        # Optimal Stopping actions are always possible
        if action.type == AttackerActionType.STOP or action.type == AttackerActionType.CONTINUE:
            return True

        machine_discovered = False
        target_machine = None
        target_machines = []
        logged_in = False
        unscanned_filesystems = False
        untried_credentials = False
        root_login = False
        machine_root_login = False
        machine_logged_in = False
        uninstalled_tools = False
        machine_w_tools = False
        uninstalled_backdoor = False

        for m in env_state.attacker_obs_state.machines:
            if m_index == -1:
                target_machines.append(m)
                machine_discovered = True

            if m.logged_in:
                logged_in = True
                if not m.filesystem_searched:
                    unscanned_filesystems = True
                if m.root:
                    root_login = True
                    if not m.tools_installed and not m.install_tools_tried:
                        uninstalled_tools = True
                    else:
                        machine_w_tools = True
                    if m.tools_installed and not m.backdoor_installed and not m.backdoor_tried:
                        uninstalled_backdoor = True
            if m.ip == ip:
                machine_discovered = True
                target_machine = m
                if m.logged_in:
                    machine_logged_in = True
                    if m.root:
                        machine_root_login = True
            # if m.shell_access and not m.logged_in:
            #     untried_credentials = True
            if m.untried_credentials:
                untried_credentials = m.untried_credentials

        if action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN:
            machine_discovered = True

        # Privilege escalation only legal if machine discovered and logged in and not root
        if action.type == AttackerActionType.PRIVILEGE_ESCALATION and (not machine_discovered or not machine_logged_in
                                                                       or machine_root_login):
            return False

        # If IP is discovered, then IP specific action without other prerequisites is legal
        if machine_discovered and (action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT
                                   or action.type == AttackerActionType.PRIVILEGE_ESCALATION):
            if action.subnet and target_machine is None:
                return True
            if m_index is not None and m_index == -1:
                exploit_tried = all(list(map(lambda x: env_state.attacker_obs_state.exploit_tried(a=action, m=x), target_machines)))
            else:
                exploit_tried = env_state.attacker_obs_state.exploit_tried(a=action, m=target_machine)
            if exploit_tried:
                return False
            return True

        # If nothing new to scan, find-flag is illegal
        if action.id == AttackerActionId.FIND_FLAG and not unscanned_filesystems:
            return False

        # If nothing new to backdoor, install backdoor is illegal
        if action.id == AttackerActionId.SSH_BACKDOOR and not uninstalled_backdoor:
            return False

        # If no new credentials, login to service is illegal
        if action.id == AttackerActionId.NETWORK_SERVICE_LOGIN and not untried_credentials:
            return False

        # Pivot recon possible if logged in on pivot machine with tools installed
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT and logged_in and machine_w_tools:
            return True

        # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
        if machine_discovered and action.type == AttackerActionType.POST_EXPLOIT \
                and ((target_machine is not None and target_machine.shell_access
                      and len(target_machine.shell_access_credentials) > 0)
                     or action.subnet or action.id == AttackerActionId.NETWORK_SERVICE_LOGIN):
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in
        if action.id == AttackerActionId.FIND_FLAG and logged_in and unscanned_filesystems:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.INSTALL_TOOLS and logged_in and root_login and uninstalled_tools:
            return True

        # Bash action not tied to specific IP only possible when having shell access and being logged in and root
        if action.id == AttackerActionId.SSH_BACKDOOR and logged_in and root_login and machine_w_tools and uninstalled_backdoor:
            return True

        return False

    def close(self) -> None:
        """
        Closes the viewer (cleanup)
        :return: None
        """
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def cleanup(self) -> None:
        """
        Cleans up environment state. This method is particularly useful in emulation mode where there are
        SSH/Telnet/FTP... connections that should be cleaned up, as well as background threads.

        :return: None
        """
        self.env_state.cleanup()
        if self.env_config.emulation_config is not None:
            self.env_config.emulation_config.close()


    def attacker_convert_ar_action(self, machine_idx, action_idx):
        """
        Converts an AR action id into a global action id

        :param machine_idx: the machine id
        :param action_idx: the action id
        :return: the global action id
        """
        key = (machine_idx, action_idx)
        print(self.env_config.attacker_action_conf.ar_action_converter)
        return self.env_config.attacker_action_conf.ar_action_converter[key]

    # -------- Private methods ------------

    def __update_log(self, action : AttackerAction) -> None:
        """
        Updates the log for rendering with a new action

        :param action: the new action to add to the log
        :return: None
        """
        tag = "-"
        if not action.subnet:
            if action.ip is not None:
                tag = str(action.ip.rsplit(".", 1)[-1])
        else:
            tag = "*"
        self.attacker_agent_state.env_log.add_entry(action.name + "[." + tag + "]" + " c:" + str(action.cost))

    def __setup_viewer(self):
        """
        Setup for the viewer to use for rendering

        :return: None
        """
        from gym_pycr_ctf.rendering import Viewer
        script_dir = os.path.dirname(__file__)
        resource_path = os.path.join(script_dir, './rendering/frames/', constants.RENDERING.RESOURCES_DIR)
        self.env_config.render_config.resources_dir = resource_path
        self.viewer = Viewer(env_config=self.env_config, init_state=self.attacker_agent_state)
        self.viewer.start()

    def __checkpoint_log(self) -> None:
        """
        Checkpoints the agent log for an episode

        :return: None
        """
        if not self.env_config.checkpoint_dir == None \
                and self.attacker_agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.attacker_agent_state.num_episodes) + "_agent.log"
            with open(file_path, "w") as outfile:
                outfile.write("\n".join(self.attacker_agent_state.env_log.log))

    def __checkpoint_trajectories(self) -> None:
        """
        Checkpoints agent trajectories

        :return: None
        """
        if self.env_config.save_trajectories and not self.env_config.checkpoint_dir == None \
                and self.attacker_agent_state.num_episodes % self.env_config.checkpoint_freq == 0:
            file_path = self.env_config.checkpoint_dir + "/ep_" + str(self.attacker_agent_state.num_episodes) + "_trajectories.pickle"
            with open(file_path, "wb") as outfile:
                pickle.dump(self.attacker_trajectories, outfile, protocol=pickle.HIGHEST_PROTOCOL)
                self.attacker_trajectories = []

    @staticmethod
    def _is_attack_action_legal_m_selection(action_id: int, env_config: EnvConfig, env_state: EnvState) -> bool:
        """
        Utility method to check if a m_selection action is legal for AR policies

        :param action_id: the action id of the m_selection to  check
        :param env_config: the environment config
        :param env_state: the environment state
        :return: True if legal else False
        """
        # Subnet actions are always legal
        if action_id == env_config.num_nodes:
            return True

        # If machine is discovered then it is a legal action
        if action_id < len(env_state.attacker_obs_state.machines):
            m = env_state.attacker_obs_state.machines[action_id]
            if m is not None:
                return True

        return False

    @staticmethod
    def _is_attack_action_legal_m_action(action_id: int, env_config: EnvConfig, env_state: EnvState, machine_index : int) \
            -> bool:
        """
        Utility method to check if a machine-specific action is legal or not for AR-policies

        :param action_id: the machine-specific-action-id
        :param env_config: the environment config
        :param env_state: the environment state
        :param machine_index: index of the machine to apply the action to
        :return: True if legal else False
        """
        action_id_id = env_config.attacker_action_conf.action_ids[action_id]
        key = (action_id_id, machine_index)
        if key not in env_config.attacker_action_conf.action_lookup_d:
            return False
        action = env_config.attacker_action_conf.action_lookup_d[(action_id_id, machine_index)]
        logged_in = False
        for m in env_state.attacker_obs_state.machines:
            if m.logged_in:
                logged_in = True

        if machine_index == env_config.num_nodes:
            if action.subnet or action.index == env_config.num_nodes:
                # Recon an exploits are always legal
                if action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT:
                    return True
                # Bash action not tied to specific IP only possible when having shell access and being logged in
                if action.id == AttackerActionId.FIND_FLAG and logged_in:
                    return True
                return False
            else:
                return False
        else:
            if action.subnet or action.index == env_config.num_nodes:
                return False
            else:
                # Recon an exploits are always legal
                if action.type == AttackerActionType.RECON or action.type == AttackerActionType.EXPLOIT:
                    return True

                if machine_index < len(env_state.attacker_obs_state.machines):
                    env_state.attacker_obs_state.sort_machines()
                    target_machine = env_state.attacker_obs_state.machines[machine_index]

                    # If IP is discovered, and credentials are found and shell access, then post-exploit actions are legal
                    if action.type == AttackerActionType.POST_EXPLOIT and target_machine.shell_access \
                            and len(target_machine.shell_access_credentials) > 0:
                        return True

                    # Bash action not tied to specific IP only possible when having shell access and being logged in
                    if action.id == AttackerActionId.FIND_FLAG and logged_in:
                        return True
        return False
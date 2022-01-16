import os
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.traffic_generator import TrafficGenerator
import csle_common.constants.constants as constants

# Stops the traffic generators in the emulation
if __name__ == '__main__':
    if not os.path.exists(util.default_traffic_path()):
        raise ValueError("You must first generate the traffic.json file")
    traffic_config = util.read_traffic_config(util.default_traffic_path())
    emulation_config = EmulationConfig(agent_ip="172.18.4.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    TrafficGenerator.stop_traffic_generators(traffic_config=traffic_config, emulation_config=emulation_config)
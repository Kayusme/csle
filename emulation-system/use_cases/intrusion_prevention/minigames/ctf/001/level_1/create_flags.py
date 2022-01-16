import os
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
import csle_common.constants.constants as constants


def default_flags() -> FlagsConfig:
    """
    :return: The flags confguration
    """
    flags = [
        NodeFlagsConfig(ip="172.18.1.79", flags = [("/tmp/flag3.txt", "flag3", "/tmp/", 3, True, 1)]),
        NodeFlagsConfig(ip="172.18.1.2", flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, True, 1)]),
        NodeFlagsConfig(ip="172.18.1.3", flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config

# Generates the flags.json configuration file
if __name__ == '__main__':
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags())
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip="172.18.1.191", agent_username=constants.csle_ADMIN.USER,
                                     agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)
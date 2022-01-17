import os
from csle_common.dao.container_config.flags_config import FlagsConfig
from csle_common.dao.container_config.node_flags_config import NodeFlagsConfig
from csle_common.util.experiments_util import util
from csle_common.dao.network.emulation_config import EmulationConfig
from csle_common.envs_model.config.generator.flags_generator import FlagsGenerator
import csle_common.constants.constants as constants


def default_flags(network_id: int = 9) -> FlagsConfig:
    """
    :param network_id: the network id
    :return: the FlagsConfig of the emulation
    """
    flags = [
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.79",
                        flags=[("/tmp/flag3.txt", "flag3", "/tmp/", 3, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.2",
                        flags=[("/tmp/flag2.txt", "flag2", "/tmp/", 2, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.3",
                        flags=[("/root/flag1.txt", "flag1", "/root/", 1, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.54",
                        flags=[("/tmp/flag4.txt", "flag4", "/tmp/", 4, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.61",
                        flags=[("/root/flag5.txt", "flag5", "/root/", 5, True, 1)]),
        NodeFlagsConfig(ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.7",
                        flags=[("/tmp/flag6.txt", "flag6", "/tmp/", 6, True, 1)])
    ]
    flags_config = FlagsConfig(flags=flags)
    return flags_config


# Generates the flags.json configuration file
if __name__ == '__main__':
    network_id = 9
    if not os.path.exists(util.default_flags_path()):
        FlagsGenerator.write_flags_config(default_flags(network_id=network_id))
    flags_config = util.read_flags_config(util.default_flags_path())
    emulation_config = EmulationConfig(agent_ip=f"{constants.CSLE.CSLE_INTERNAL_SUBNETMASK_PREFIX}{network_id}.191",
                                       agent_username=constants.csle_ADMIN.USER,
                                       agent_pw=constants.csle_ADMIN.PW, server_connection=False)
    FlagsGenerator.create_flags(flags_config=flags_config, emulation_config=emulation_config)

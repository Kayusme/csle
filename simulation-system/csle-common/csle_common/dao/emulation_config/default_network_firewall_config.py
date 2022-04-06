from typing import Union, Dict, Any
from csle_common.dao.emulation_config.container_network import ContainerNetwork


class DefaultNetworkFirewallConfig:
    """
    DTO representing a default firewall configuration
    """

    def __init__(self, ip: Union[str, None], default_gw: Union[str, None], default_input: str, default_output: str,
                 default_forward: str, network: ContainerNetwork):
        """
        Initialzies the DTO

        :param ip: the ip associated to the network
        :param default_gw: the default gateway for the network
        :param default_input: the default input policy for the network
        :param default_output: the default output policy for the network
        :param default_forward: the default forward policy for the network
        :param network: the network configuraiton
        """
        self.ip = ip
        self.default_gw = default_gw
        self.default_input = default_input
        self.default_output = default_output
        self.default_forward = default_forward
        self.network = network

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "DefaultNetworkFirewallConfig":
        """
        Converts a dict representation to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = DefaultNetworkFirewallConfig(
            ip = d["ip"], default_gw=d["default_gw"], default_input=d["default_input"],
            default_output=d["default_output"], default_forward=d["default_forward"],
            network=ContainerNetwork.from_dict(d["network"])
        )
        return obj

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["ip"] = self.ip
        d["default_gw"] = self.default_gw
        d["default_input"] = self.default_input
        d["default_output"] = self.default_output
        d["default_forward"] = self.default_forward
        d["network"] = self.network.to_dict()
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"ip:{self.ip}, default_gw:{self.default_gw}, default_input:{self.default_input}, " \
               f"default_output:{self.default_output}, default_forward:{self.default_forward}, network:{self.network}"

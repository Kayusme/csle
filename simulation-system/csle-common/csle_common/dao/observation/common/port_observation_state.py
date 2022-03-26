from csle_common.dao.network.transport_protocol import TransportProtocol
from csle_common.dao.network.network_service import NetworkService


class PortObservationState:
    """
    DTO Representation a Port observation
    """

    def __init__(self, port : int, open : bool, service : int, protocol : TransportProtocol, http_enum: str = "",
                 http_grep: str = "", vulscan: str = "", version : str = "", fingerprint: str = ""):
        """
        Initializes the DTO

        :param port: the port
        :param open: whether the port is open or not (boolean)
        :param service: the service of the port
        :param protocol: the protocol of the port
        :param http_enum: the HTTP enum result on the port
        :param http_grep: the HTTP grep result on the port
        :param vulscan: the vulscan result of the port
        :param version: the version of the port
        :param fingerprint: the fingerprint output of the port
        """
        self.port = port
        self.open = open
        self.service = service
        self.protocol = protocol
        self.http_enum = http_enum
        self.http_grep = http_grep
        self.vulscan = vulscan
        self.version = version
        self.fingerprint = fingerprint

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return "port:{}, open:{}, service:{}, protocol:{}, http_enum:{}, http_grep:{}, vulscan:{}, version:{}, " \
               "fingerprint:{}".format(
            self.port, self.open,  self.service, self.protocol, self.http_enum, self.http_grep, self.vulscan,
            self.version, self.fingerprint)

    def to_network_service(self) -> NetworkService:
        """
        Converts the object into a network service representation

        :return: the network service representation
        """
        service = NetworkService(protocol=self.protocol, port=self.port, name=self.service, credentials=[])
        return service

    @staticmethod
    def from_network_service(network_service: NetworkService, service_lookup: dict) -> "PortObservationState":
        """
        Converts a network service into a port observation state

        :param network_service: the network service to convert
        :param service_lookup: a lookup table for converting between service names and service ids
        :return:
        """
        if network_service.name in service_lookup:
            s = service_lookup[network_service.name]
        else:
            s = service_lookup["unknown"]
        port = PortObservationState(port=network_service.port, open=True,
                                    service=s,
                                    protocol=network_service.protocol)
        return port
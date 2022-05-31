from typing import Dict, Any
from csle_common.dao.emulation_config.credential import Credential


class EmulationConnectionObservationState:
    """
    A DTO representing a connection observation in the emulation
    """

    def __init__(self, conn, credential: Credential, root: bool, service: str, port: int, tunnel_thread = None,
                 tunnel_port : int = None, interactive_shell = None,
                 proxy : "EmulationConnectionObservationState" = None, ip = None):
        """
        Intializes the DTO

        :param conn: the connection object
        :param credential: the credential of the connection
        :param root: whether the connection is root or not
        :param service: the service of the connection
        :param port: the port of the connection
        :param tunnel_thread: the tunnel thread for the connection
        :param tunnel_port: the tunnel port of the connection
        :param interactive_shell: an interactive shell of the connection
        :param proxy: a proxy for the connection
        :param ip: the ip of the connection
        """
        if proxy is not None:
            assert ip != proxy.ip
        self.conn = conn
        self.credential = credential
        self.root = root
        self.port = port
        self.service = service
        self.tunnel_thread = tunnel_thread
        self.tunnel_port = tunnel_port
        self.interactive_shell = interactive_shell
        self.proxy = proxy
        self.ip = ip

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmulationConnectionObservationState":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EmulationConnectionObservationState(
            conn=None, credential=Credential.from_dict(d["credential"]), root=d["root"], port=d["port"], service=d["service"],
            tunnel_port=d["tunnel_port"], tunnel_thread=None, interactive_shell=None, ip=d["ip"], proxy=None
        )
        return obj

    def to_dict(self)-> Dict[str, Any]:
        """
        :return: a dict represnetation of the object
        """
        d = {}
        d["credential"] = self.credential.to_dict()
        d["root"] = self.root
        d["port"] = self.port
        d["service"] = self.service
        d["ip"] = self.ip
        d["tunnel_port"] = self.tunnel_port
        return d

    def __str__(self) -> str:
        """
        :return: a string representation of the connection observation
        """
        return "credential:{},root:{},service:{},port:{}".format(self.credential, self.root, self.service, self.port)

    def __eq__(self, other) -> bool:
        """
        Checks for equality with another connection

        :param other: the other connection to compare with
        :return: True if equal, otherwise False
        """
        if not isinstance(other, EmulationConnectionObservationState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.credential.username == other.credential.username and self.root == other.root \
               and self.service == other.service \
               and self.port == other.port and self.ip == other.ip

    def __hash__(self):
        """
        :return: a hash representation of the object
        """
        return hash(self.credential.username) + 31 * hash(self.root) \
               + 31 * hash(self.service) + 31 * hash(self.port) \
               + 31 * hash(self.ip)

    def cleanup(self) -> None:
        """
        Utility function for cleaning up the connection.

        :return: None
        """

        if self.tunnel_thread is not None:
            try:
                self.tunnel_thread.shutdown()
            except Exception:
                pass
            self.tunnel_thread = None
        if self.interactive_shell is not None:
            try:
                self.interactive_shell.close()
            except Exception:
                pass
            self.interactive_shell = None
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None
        if self.proxy is not None:
            try:
                self.proxy.cleanup()
            except Exception:
                pass
            self.proxy = None


    def to_json_str(self) -> str:
        """
        Converts the DTO into a json string

        :return: the json string representation of the DTO
        """
        import json
        json_str = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        return json_str

    def to_json_file(self, json_file_path: str) -> None:
        """
        Saves the DTO to a json file

        :param json_file_path: the json file path to save  the DTO to
        :return: None
        """
        import io
        json_str = self.to_json_str()
        with io.open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json_str)
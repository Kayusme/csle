from typing import Dict, Any, List
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType


class EPTMPArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a homogenous poisson arrival process with an
    Exponential-Polynomial-Trigonometric rate function having Multiple Periodicities
    """

    def __init__(self, thetas: List[float], gammas: List[float], phis: List[float], omegas: List[float], mu: float):
        """
        Initializes the object

        :param mu: expected service time
        :param thetas: represent the overall trend in frequency of events over a long time frame
        :param gammas: amplitudes
        :param phis: period shifts
        :param omegas: frequencies
        """
        self.mu = mu
        self.thetas = thetas
        self.gammas = gammas
        self.phis = phis
        self.omegas = omegas
        super(EPTMPArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.EPTMP)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"thetas: {self.thetas}, gammas: {self.gammas}, phis: {self.phis}, omegas: {self.omegas}, " \
               f"client_arrival_type: {self.client_arrival_type}, mu: {self.mu}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["thetas"] = self.thetas
        d["gammas"] = self.gammas
        d["phis"] = self.phis
        d["omegas"] = self.omegas
        d["mu"] = self.mu
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EPTMPArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = EPTMPArrivalConfig(thetas=d["thetas"], gammas=d["gammas"], phis=d["phis"], omegas=d["omegas"], mu=d["mu"])
        return obj
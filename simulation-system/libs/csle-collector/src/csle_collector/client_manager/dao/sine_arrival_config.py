from typing import Dict, Any
from csle_collector.client_manager.dao.arrival_config import ArrivalConfig
from csle_collector.client_manager.dao.client_arrival_type import ClientArrivalType


class SineArrivalConfig(ArrivalConfig):
    """
    DTO representing the configuration of a sine-modulated poisson arrival process withb exponential service times
    """

    def __init__(self, lamb: float, mu: float, time_scaling_factor: float, period_scaling_factor: float):
        """
        Initializes the object

        :param lamb: the static arrival rate
        :param mu: the mean service time
        :param time_scaling_factor: the time-scaling factor for sine-modulated arrival processes
        :param period_scaling_factor: the period-scaling factor for sine-modulated arrival processes
        """
        self.lamb = lamb
        self.mu = mu
        self.time_scaling_factor = time_scaling_factor
        self.period_scaling_factor = period_scaling_factor
        super(SineArrivalConfig, self).__init__(client_arrival_type=ClientArrivalType.SINE_MODULATED)

    def __str__(self) -> str:
        """
        :return: a string representation of the object
        """
        return f"lamb: {self.lamb}, mu: {self.mu}, time_scaling_factor: {self.time_scaling_factor}, " \
               f"period_scaling_factor: {self.period_scaling_factor}, client_arrival_type: {self.client_arrival_type}"

    def to_dict(self) -> Dict[str, Any]:
        """
        :return: a dict representation of the object
        """
        d = {}
        d["lamb"] = self.lamb
        d["mu"] = self.mu
        d["time_scaling_factor"] = self.time_scaling_factor
        d["period_scaling_factor"] = self.period_scaling_factor
        d["client_arrival_type"] = self.client_arrival_type
        return d

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "SineArrivalConfig":
        """
        Converts a dict representation of the object to an instance

        :param d: the dict to convert
        :return: the created instance
        """
        obj = SineArrivalConfig(lamb=d["lamb"], mu=d["mu"], time_scaling_factor=d["time_scaling_factor"],
                                period_scaling_factor=d["period_scaling_factor"])
        return obj
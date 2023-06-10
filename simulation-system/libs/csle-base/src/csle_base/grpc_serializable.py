from abc import ABC, abstractmethod


class GRPCSerializable(ABC):
    """
    Abstract class representing objects that are GRPC serializable
    """

    @abstractmethod
    def to_grpc_object(self):
        """
        :return: a grpc serializable version of the object
        """
        pass

    @staticmethod
    @abstractmethod
    def from_grpc_object(obj):
        """
        Instantiate the object from a GRPC object

        :param obj: the objet to instantiate from
        :return: the instantiated grpc object
        """
        pass
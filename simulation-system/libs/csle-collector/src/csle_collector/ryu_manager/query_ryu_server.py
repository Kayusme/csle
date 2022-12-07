import csle_collector.ryu_manager.ryu_manager_pb2_grpc
import csle_collector.ryu_manager.ryu_manager_pb2
import csle_collector.constants.constants as constants


def get_ryu_status(stub: csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub,
                     timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
    """
    Queries the server for the ryu server status

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a RyuDTO describing the status of the ryu controller
    """
    get_ryu_status_msg = csle_collector.ryu_manager.ryu_manager_pb2.GetRyuStatusMsg()
    ryu_dto = stub.getRyuStatus(get_ryu_status_msg, timeout=timeout)
    return ryu_dto


def stop_ryu(stub: csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub,
             timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
    """
    Sends a request to the Ryu controller to stop the Ryu controller

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :return: a RyuDTO describing the status of the ryu controller
    """
    stop_ryu_msg = csle_collector.ryu_manager.ryu_manager_pb2.StopRyuMsg()
    ryu_dto = stub.stopRyu(stop_ryu_msg, timeout=timeout)
    return ryu_dto


def start_ryu(stub: csle_collector.ryu_manager.ryu_manager_pb2_grpc.RyuManagerStub,
              port: int, web_port: int, controller: str, timeout=constants.GRPC.TIMEOUT_SECONDS) \
        -> csle_collector.ryu_manager.ryu_manager_pb2.RyuDTO:
    """
    Sends a request to the Ryu manager to start the Ryu controller

    :param stub: the stub to send the remote gRPC to the server
    :param timeout: the GRPC timeout (seconds)
    :param port: the port that Ryu will listen to
    :param web_port: the port that the Ryu web interface will listen to
    :param controller: the controller that Ryu will start
    :return: a RyuDTO describing the status of the ryu controller
    """
    start_ryu_msg = csle_collector.ryu_manager.ryu_manager_pb2.StartRyuMsg(
        port=port, web_port=web_port, controller=controller)
    ryu_dto = stub.startRyu(start_ryu_msg, timeout=timeout)
    return ryu_dto

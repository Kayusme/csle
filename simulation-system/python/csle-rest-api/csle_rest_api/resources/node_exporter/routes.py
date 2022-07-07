"""
Routes and sub-resources for the /node_exporter resource
"""

from flask import Blueprint, jsonify
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants


# Creates a blueprint "sub application" of the main REST app
node_exporter_bp = Blueprint(api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE, __name__,
                             url_prefix=f"{constants.COMMANDS.SLASH_DELIM}"
                                     f"{api_constants.MGMT_WEBAPP.NODE_EXPORTER_RESOURCE}")


@node_exporter_bp.route("",
                        methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET, api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def node_exporter():
    """
    :return: static resources for the /node-exporter url
    """
    running = MonitorToolsController.is_node_exporter_running()
    port = constants.COMMANDS.NODE_EXPORTER_PORT
    node_exporter_dict = {
        api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: running,
        api_constants.MGMT_WEBAPP.PORT_PROPERTY: port,
        api_constants.MGMT_WEBAPP.URL_PROPERTY: f"http://localhost:{port}/"
    }
    response = jsonify(node_exporter_dict)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response
"""
Routes and sub-resources for the /training-jobs resource
"""
import time
from flask import Blueprint, jsonify, request
import csle_common.constants.constants as constants
import csle_rest_api.constants.constants as api_constants
from csle_common.metastore.metastore_facade import MetastoreFacade
from csle_common.util.emulation_util import EmulationUtil
from csle_common.controllers.monitor_tools_controller import MonitorToolsController
from csle_agents.job_controllers.training_job_manager import TrainingJobManager


# Creates a blueprint "sub application" of the main REST app
training_jobs_bp = Blueprint(
    api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE, __name__,
    url_prefix=f"{constants.COMMANDS.SLASH_DELIM}{api_constants.MGMT_WEBAPP.TRAINING_JOBS_RESOURCE}")


@training_jobs_bp.route("", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                        api_constants.MGMT_WEBAPP.HTTP_REST_DELETE])
def training_jobs():
    """
    The /training-jobs resource.

    :return: A list of training-jobs or a list of ids of the jobs or deletes the jobs
    """

    if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
        # Check if ids query parameter is True, then only return the ids and not the whole dataset
        ids = request.args.get(api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM)
        if ids is not None and ids:
            return training_jobs_ids()

        training_jobs = MetastoreFacade.list_training_jobs()
        alive_jobs = []
        for job in training_jobs:
            if EmulationUtil.check_pid(job.pid):
                job.running = True
            alive_jobs.append(job)
        training_jobs_dicts = list(map(lambda x: x.to_dict(), alive_jobs))
        response = jsonify(training_jobs_dicts)
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response
    elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
        jobs = MetastoreFacade.list_training_jobs()
        for job in jobs:
            MonitorToolsController.stop_pid(job.pid)
            MetastoreFacade.remove_training_job(training_job=job)
        time.sleep(2)
        response = jsonify({})
        response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
        return response


def training_jobs_ids():
    """
    :return: An HTTP response with all training jobs ids
    """
    training_jobs_ids = MetastoreFacade.list_training_jobs_ids()
    response_dicts = []
    for tup in training_jobs_ids:
        response_dicts.append({
            api_constants.MGMT_WEBAPP.ID_PROPERTY: tup[0],
            api_constants.MGMT_WEBAPP.SIMULATION_PROPERTY: tup[1],
            api_constants.MGMT_WEBAPP.EMULATION_PROPERTY: tup[2],
            api_constants.MGMT_WEBAPP.RUNNING_PROPERTY: EmulationUtil.check_pid(tup[3])
        })
    response = jsonify(response_dicts)
    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response


@training_jobs_bp.route("/<job_id>", methods=[api_constants.MGMT_WEBAPP.HTTP_REST_GET,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_DELETE,
                                              api_constants.MGMT_WEBAPP.HTTP_REST_POST])
def training_policy(job_id: int):
    """
    The /training-jobs/id resource.

    :param job_id: the id of the policy

    :return: The given policy or deletes the policy
    """
    job = MetastoreFacade.get_training_job_config(id=job_id)
    response = jsonify({})
    if job is not None:
        if request.method == api_constants.MGMT_WEBAPP.HTTP_REST_GET:
            if EmulationUtil.check_pid(job.pid):
                job.running = True
            response = jsonify(job.to_dict())
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_DELETE:
            MonitorToolsController.stop_pid(job.pid)
            MetastoreFacade.remove_training_job(training_job=job)
            time.sleep(2)
        elif request.method == api_constants.MGMT_WEBAPP.HTTP_REST_POST:
            start = True
            stop = request.args.get(api_constants.MGMT_WEBAPP.STOP_QUERY_PARAM)
            if stop is not None and stop:
                start = False
            if start:
                TrainingJobManager.start_training_job_in_background(training_job=job)
                time.sleep(2)
            else:
                MonitorToolsController.stop_pid(pid=job.pid)
                time.sleep(2)

    response.headers.add(api_constants.MGMT_WEBAPP.ACCESS_CONTROL_ALLOW_ORIGIN_HEADER, "*")
    return response
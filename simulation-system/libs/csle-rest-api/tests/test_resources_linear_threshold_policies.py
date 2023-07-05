import json
import logging

import csle_common.constants.constants as constants
import pytest
from csle_common.dao.simulation_config.action import Action
from csle_common.dao.simulation_config.state import State
from csle_common.dao.simulation_config.state_type import StateType
from csle_common.dao.training.agent_type import AgentType
from csle_common.dao.training.experiment_config import ExperimentConfig
from csle_common.dao.training.hparam import HParam
from csle_common.dao.training.linear_threshold_stopping_policy import (
    LinearThresholdStoppingPolicy,
)
from csle_common.dao.training.player_type import PlayerType

import csle_rest_api.constants.constants as api_constants
from csle_rest_api.rest_api import create_app


class TestRecourcesLinearThresholdSuite(object):
    """
    Test suite for /linaer-threshold resource
    """

    pytest.logger = logging.getLogger("resources_users_tests")

    @pytest.fixture
    def flask_app(self):
        """
        :return: the flask app fixture representing the webserver
        """
        return create_app(
            static_folder="../../../../../management-system/csle-mgmt-webapp/build"
        )

    @pytest.fixture
    def list_linear_threshold_ids(self, mocker):
        """
        pytest fixture for list_linear_threshold_ids policies
        """
        def list_linear_threshold_stopping_policies_ids():
            policy_id = (111, "some_simulation")
            return [policy_id]
        list_ppo_plicies_ids_mocker = mocker.MagicMock(side_effect=list_linear_threshold_stopping_policies_ids)
        return list_ppo_plicies_ids_mocker

    @pytest.fixture
    def list_linear_theshold(self, mocker):
        """
        pytest fixture for listing linear_threshold policies
        """
        def list_linear_threshold_stopping_policies():
            policy = TestRecourcesLinearThresholdSuite.get_example_policy()
            return [policy]
        list_linear_threshold_stopping_policies_mocker = mocker.MagicMock(side_effect=
                                                                          list_linear_threshold_stopping_policies)
        return list_linear_threshold_stopping_policies_mocker

    @pytest.fixture
    def remove(self, mocker):
        """
        pytest fixture for removal of linear_threshold policies
        """
        def remove_linear_threshold_stopping_policy(linear_threshold_stopping_policy):
            return None
        remove_linear_threshold_stopping_policy_mocker = mocker.MagicMock(side_effect=
                                                                          remove_linear_threshold_stopping_policy)
        return remove_linear_threshold_stopping_policy_mocker

    @pytest.fixture
    def get_policy(self, mocker):
        """
        pytest fixture for the get linear_threshold policy
        """
        def get_linear_threshold_stopping_policy(id):
            policy = TestRecourcesLinearThresholdSuite.get_example_policy()
            return policy
        get_linear_threshold_stopping_policy_mocker = mocker.MagicMock(side_effect=get_linear_threshold_stopping_policy)
        return get_linear_threshold_stopping_policy_mocker

    @staticmethod
    def get_example_policy():
        """
        :return: an example class full of dummy values
        """
        state_list = [State(id=1, name="JohnDoe", descr="description", state_type=StateType(0))]
        e_config_class = ExperimentConfig(output_dir="output_directory", title="title", random_seeds=[1, 2, 3],
                                          agent_type=AgentType(1),
                                          hparams={'element': HParam(10, name="John", descr="Doe")},
                                          log_every=10, player_type=PlayerType(1),
                                          player_idx=10, br_log_every=10)
        obj = LinearThresholdStoppingPolicy(theta=[1, 2, 3], simulation_name="JohnDoeSimulation",
                                            L=20, states=state_list, player_type=PlayerType(1),
                                            actions=[Action(id=10, descr="null")],
                                            experiment_config=e_config_class, avg_R=1.1,
                                            agent_type=AgentType(1),
                                            opponent_strategy=None)
        return obj

    def test_linear_threshold_policies_get(
            self,
            flask_app,
            mocker,
            list_linear_theshold,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            list_linear_threshold_ids,
    ) -> None:
        """
        testing the GET HTTPS method  for the /linear-threshold-policies resource
        """
        test_policy = TestRecourcesLinearThresholdSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "list_linear_threshold_stopping_policies",
                     side_effect=list_linear_theshold)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "list_linear_threshold_stopping_policies_ids",
                     side_effect=list_linear_threshold_ids)
        mocker.patch("csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
                     side_effect=not_logged_in,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"
                                               f"?{api_constants.MGMT_WEBAPP.IDS_QUERY_PARAM}=true")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        lin_thresh_dict = response_data_list[0]
        assert lin_thresh_dict["id"] == 111
        assert lin_thresh_dict["simulation"] == "some_simulation"
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        l_thresh = LinearThresholdStoppingPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert l_thresh.L == test_policy.L
        assert l_thresh.actions[0].descr == test_policy.actions[0].descr
        assert l_thresh.actions[0].id == test_policy.actions[0].id
        assert l_thresh.agent_type == test_policy.agent_type
        assert l_thresh.avg_R == test_policy.avg_R
        assert l_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert l_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert l_thresh.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert l_thresh.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert l_thresh.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert l_thresh.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert l_thresh.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert l_thresh.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert l_thresh.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert l_thresh.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert l_thresh.experiment_config.title == test_policy.experiment_config.title
        assert l_thresh.id == test_policy.id
        assert l_thresh.player_type == test_policy.player_type
        assert l_thresh.policy_type == test_policy.policy_type
        assert l_thresh.simulation_name == l_thresh.simulation_name
        assert l_thresh.states[0].descr == test_policy.states[0].descr
        assert l_thresh.states[0].id == test_policy.states[0].id
        assert l_thresh.states[0].name == test_policy.states[0].name
        assert l_thresh.states[0].state_type == test_policy.states[0].state_type
        assert l_thresh.theta == test_policy.theta
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        l_thresh = LinearThresholdStoppingPolicy.from_dict(response_data_list[0])
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert l_thresh.L == test_policy.L
        assert l_thresh.actions[0].descr == test_policy.actions[0].descr
        assert l_thresh.actions[0].id == test_policy.actions[0].id
        assert l_thresh.agent_type == test_policy.agent_type
        assert l_thresh.avg_R == test_policy.avg_R
        assert l_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert l_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert l_thresh.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert l_thresh.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert l_thresh.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert l_thresh.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert l_thresh.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert l_thresh.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert l_thresh.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert l_thresh.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert l_thresh.experiment_config.title == test_policy.experiment_config.title
        assert l_thresh.id == test_policy.id
        assert l_thresh.player_type == test_policy.player_type
        assert l_thresh.policy_type == test_policy.policy_type
        assert l_thresh.simulation_name == l_thresh.simulation_name
        assert l_thresh.states[0].descr == test_policy.states[0].descr
        assert l_thresh.states[0].id == test_policy.states[0].id
        assert l_thresh.states[0].name == test_policy.states[0].name
        assert l_thresh.states[0].state_type == test_policy.states[0].state_type
        assert l_thresh.theta == test_policy.theta

    def test_linear_threshold_policies_delete(
            self,
            flask_app,
            mocker,
            list_linear_theshold,
            logged_in,
            not_logged_in,
            logged_in_as_admin,
            remove,
    ) -> None:
        """
        testing  the DELETE HTTPS method for the /linear-threshold-policies resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "remove_linear_threshold_stopping_policy",
                     side_effect=remove)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "list_linear_threshold_stopping_policies",
                     side_effect=list_linear_theshold)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE)
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert response_data_list == {}

    def test_linear_threshold_policies_id_get(self, flask_app, mocker, logged_in,
                                              not_logged_in, logged_in_as_admin,
                                              get_policy,) -> None:
        """
        testing the HTTPS GET method for the /linear-threshold-policies/id resource
        """
        test_policy = TestRecourcesLinearThresholdSuite.get_example_policy()
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "get_linear_threshold_stopping_policy",
                     side_effect=get_policy)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,
        )
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        l_thresh = LinearThresholdStoppingPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert l_thresh.L == test_policy.L
        assert l_thresh.actions[0].descr == test_policy.actions[0].descr
        assert l_thresh.actions[0].id == test_policy.actions[0].id
        assert l_thresh.agent_type == test_policy.agent_type
        assert l_thresh.avg_R == test_policy.avg_R
        assert l_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert l_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert l_thresh.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert l_thresh.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert l_thresh.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert l_thresh.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert l_thresh.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert l_thresh.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert l_thresh.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert l_thresh.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert l_thresh.experiment_config.title == test_policy.experiment_config.title
        assert l_thresh.id == test_policy.id
        assert l_thresh.player_type == test_policy.player_type
        assert l_thresh.policy_type == test_policy.policy_type
        assert l_thresh.simulation_name == l_thresh.simulation_name
        assert l_thresh.states[0].descr == test_policy.states[0].descr
        assert l_thresh.states[0].id == test_policy.states[0].id
        assert l_thresh.states[0].name == test_policy.states[0].name
        assert l_thresh.states[0].state_type == test_policy.states[0].state_type
        assert l_thresh.theta == test_policy.theta
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,)
        response = flask_app.test_client().get(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        l_thresh = LinearThresholdStoppingPolicy.from_dict(response_data_list)
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE
        assert l_thresh.L == test_policy.L
        assert l_thresh.actions[0].descr == test_policy.actions[0].descr
        assert l_thresh.actions[0].id == test_policy.actions[0].id
        assert l_thresh.agent_type == test_policy.agent_type
        assert l_thresh.avg_R == test_policy.avg_R
        assert l_thresh.experiment_config.agent_type == test_policy.experiment_config.agent_type
        assert l_thresh.experiment_config.br_log_every == test_policy.experiment_config.br_log_every
        assert l_thresh.experiment_config.hparams["element"].descr == \
            test_policy.experiment_config.hparams["element"].descr
        assert l_thresh.experiment_config.hparams["element"].name == \
            test_policy.experiment_config.hparams["element"].name
        assert l_thresh.experiment_config.hparams["element"].value == \
            test_policy.experiment_config.hparams["element"].value
        assert l_thresh.experiment_config.log_every == \
            test_policy.experiment_config.log_every
        assert l_thresh.experiment_config.output_dir == \
            test_policy.experiment_config.output_dir
        assert l_thresh.experiment_config.player_idx == \
            test_policy.experiment_config.player_idx
        assert l_thresh.experiment_config.player_type == \
            test_policy.experiment_config.player_type
        assert l_thresh.experiment_config.random_seeds == \
            test_policy.experiment_config.random_seeds
        assert l_thresh.experiment_config.title == test_policy.experiment_config.title
        assert l_thresh.id == test_policy.id
        assert l_thresh.player_type == test_policy.player_type
        assert l_thresh.policy_type == test_policy.policy_type
        assert l_thresh.simulation_name == l_thresh.simulation_name
        assert l_thresh.states[0].descr == test_policy.states[0].descr
        assert l_thresh.states[0].id == test_policy.states[0].id
        assert l_thresh.states[0].name == test_policy.states[0].name
        assert l_thresh.states[0].state_type == test_policy.states[0].state_type
        assert l_thresh.theta == test_policy.theta

    def test_linear_threshold_policies_id_delete(self, flask_app, mocker, logged_in,
                                                 not_logged_in, logged_in_as_admin,
                                                 get_policy, remove) -> None:

        """
        testing the HTTPS DELETE method for the /linear-threshold-policies/id resource
        """
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "get_linear_threshold_stopping_policy",
                     side_effect=get_policy)
        mocker.patch("csle_common.metastore.metastore_facade.MetastoreFacade." +
                     "remove_linear_threshold_stopping_policy",
                     side_effect=remove)
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=not_logged_in,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"
                                                  f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in,)
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"
                                                  f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response.status_code == constants.HTTPS.UNAUTHORIZED_STATUS_CODE
        assert response_data_list == {}
        mocker.patch(
            "csle_rest_api.util.rest_api_util.check_if_user_is_authorized",
            side_effect=logged_in_as_admin,
        )
        response = flask_app.test_client().delete(f"{api_constants.MGMT_WEBAPP.LINEAR_THRESHOLD_POLICIES_RESOURCE}"
                                                  f"/10")
        response_data = response.data.decode("utf-8")
        response_data_list = json.loads(response_data)
        assert response_data_list == {}
        assert response.status_code == constants.HTTPS.OK_STATUS_CODE

from csle_common.dao.emulation_config.node_beats_config import NodeBeatsConfig
from csle_common.dao.emulation_config.beats_config import BeatsConfig
from csle_common.dao.emulation_config.client_managers_info import ClientManagersInfo
from csle_common.dao.emulation_config.container_network import ContainerNetwork
from csle_common.dao.emulation_config.cluster_node import ClusterNode
from csle_common.dao.emulation_config.cluster_config import ClusterConfig
from csle_common.dao.emulation_config.config import Config
from csle_common.dao.emulation_config.credential import Credential
from csle_common.dao.emulation_config.default_network_firewall_config import DefaultNetworkFirewallConfig
from csle_common.dao.emulation_config.node_firewall_config import NodeFirewallConfig
from csle_common.dao.emulation_config.transport_protocol import TransportProtocol
from csle_common.dao.emulation_config.docker_stats_manager_config import DockerStatsManagerConfig
from csle_common.dao.emulation_config.docker_stats_managers_info import DockerStatsManagersInfo
from csle_common.dao.emulation_config.node_network_config import NodeNetworkConfig
from csle_common.dao.emulation_config.packet_loss_type import PacketLossType
from csle_common.dao.emulation_config.packet_delay_distribution_type import PacketDelayDistributionType
from csle_common.dao.emulation_config.node_resources_config import NodeResourcesConfig
from csle_common.dao.emulation_config.resources_config import ResourcesConfig
from csle_common.dao.emulation_config.node_container_config import NodeContainerConfig
from csle_common.dao.emulation_config.node_services_config import NodeServicesConfig
from csle_common.dao.emulation_config.node_traffic_config import NodeTrafficConfig
from csle_common.dao.emulation_config.user import User
from csle_common.dao.emulation_config.node_users_config import NodeUsersConfig
from csle_common.dao.emulation_config.node_vulnerability_config import NodeVulnerabilityConfig
from csle_common.dao.emulation_config.flag import Flag
from csle_common.dao.emulation_config.node_flags_config import NodeFlagsConfig
from csle_common.dao.emulation_config.elk_config import ElkConfig
from csle_common.dao.emulation_config.elk_managers_info import ELKManagersInfo
from csle_common.dao.emulation_config.snort_managers_info import SnortIdsManagersInfo
from csle_common.dao.emulation_config.ossec_managers_info import OSSECIDSManagersInfo
from csle_common.dao.emulation_config.ryu_managers_info import RyuManagersInfo
from csle_common.dao.emulation_config.host_managers_info import HostManagersInfo
from csle_common.dao.emulation_config.kafka_managers_info import KafkaManagersInfo
from csle_common.dao.emulation_config.ossec_ids_manager_config import OSSECIDSManagerConfig
from csle_common.dao.emulation_config.ovs_config import OVSConfig
from csle_common.dao.emulation_config.ovs_switch_config import OvsSwitchConfig
from csle_common.dao.emulation_config.kafka_config import KafkaConfig
from csle_common.dao.emulation_config.kafka_topic import KafkaTopic
from csle_common.dao.emulation_config.vulnerability_type import VulnType
from csle_common.dao.emulation_config.network_service import NetworkService
from csle_collector.client_manager.client_manager_pb2 import ClientsDTO
from csle_collector.docker_stats_manager.docker_stats_manager_pb2 import DockerStatsMonitorDTO
from csle_collector.elk_manager.elk_manager_pb2 import ElkDTO
from csle_collector.host_manager.host_manager_pb2 import HostStatusDTO
from csle_collector.snort_ids_manager.snort_ids_manager_pb2 import SnortIdsMonitorDTO
from csle_collector.ossec_ids_manager.ossec_ids_manager_pb2 import OSSECIdsMonitorDTO
from csle_collector.ryu_manager.ryu_manager_pb2 import RyuDTO
from csle_collector.kafka_manager.kafka_manager_pb2 import KafkaDTO


class TestEmulationConfigDaoSuite:
    """
    Test suite for datasets data access objects (DAOs)
    """

    def test_node_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeBeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        assert isinstance(node_beats_config.to_dict(), dict)
        assert isinstance(NodeBeatsConfig.from_dict(node_beats_config.to_dict()), NodeBeatsConfig)
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()).to_dict() == node_beats_config.to_dict()
        assert NodeBeatsConfig.from_dict(node_beats_config.to_dict()) == node_beats_config

    def test_beats_config(self) -> None:
        """
        Tests creation and dict conversion of the BeatsConfig DAO

        :return: None
        """
        node_beats_config = NodeBeatsConfig(
            ip="192.168.5.1", log_files_paths=["log1"], filebeat_modules=["mod1"], metricbeat_modules=["mod2"],
            heartbeat_hosts_to_monitor=["192.168.5.7"], kafka_input=False, start_heartbeat_automatically=True,
            start_packetbeat_automatically=True, start_metricbeat_automatically=True, start_filebeat_automatically=True
        )
        beats_config = BeatsConfig(
            node_beats_configs=[node_beats_config], num_elastic_shards=19, reload_enabled=False
        )
        assert isinstance(beats_config.to_dict(), dict)
        assert isinstance(BeatsConfig.from_dict(beats_config.to_dict()), BeatsConfig)
        assert BeatsConfig.from_dict(beats_config.to_dict()).to_dict() == beats_config.to_dict()
        assert BeatsConfig.from_dict(beats_config.to_dict()) == beats_config

    def test_client_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the client_managers_info_dto

        :return: None
        """
        client_manager_status = ClientsDTO(
            num_clients=19, client_process_active=True, producer_active=False, clients_time_step_len_seconds=30,
            producer_time_step_len_seconds=30)
        client_managers_info = ClientManagersInfo(
            ips=["192.168.25.12"], ports=[2333], emulation_name="test_em", execution_id=19,
            client_managers_running=[True], client_managers_statuses=[client_manager_status])
        assert isinstance(client_managers_info.to_dict(), dict)
        assert isinstance(ClientManagersInfo.from_dict(client_managers_info.to_dict()), ClientManagersInfo)
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()).to_dict() == client_managers_info.to_dict()
        assert ClientManagersInfo.from_dict(client_managers_info.to_dict()) == client_managers_info

    def test_container_network(self) -> None:
        """
        Tests creation and dict conversion of the ContainerNetwork DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        assert isinstance(container_network.to_dict(), dict)
        assert isinstance(ContainerNetwork.from_dict(container_network.to_dict()), ContainerNetwork)
        assert ContainerNetwork.from_dict(container_network.to_dict()).to_dict() == container_network.to_dict()
        assert ContainerNetwork.from_dict(container_network.to_dict()) == container_network

    def test_cluster_node(self) -> None:
        """
        Tests creation and dict conversion of the ClusterNode DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        assert isinstance(cluster_node.to_dict(), dict)
        assert isinstance(ClusterNode.from_dict(cluster_node.to_dict()), ClusterNode)
        assert ClusterNode.from_dict(cluster_node.to_dict()).to_dict() == cluster_node.to_dict()
        assert ClusterNode.from_dict(cluster_node.to_dict()) == cluster_node

    def test_cluster_config(self) -> None:
        """
        Tests creation and dict conversion of the ClusterConfig DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        cluster_config = ClusterConfig(cluster_nodes=[cluster_node])
        assert isinstance(cluster_config.to_dict(), dict)
        assert isinstance(ClusterConfig.from_dict(cluster_config.to_dict()), ClusterConfig)
        assert ClusterConfig.from_dict(cluster_config.to_dict()).to_dict() == cluster_config.to_dict()
        assert ClusterConfig.from_dict(cluster_config.to_dict()) == cluster_config

    def test_config(self) -> None:
        """
        Tests creation and dict conversion of the Config DTO

        :return: None
        """
        cluster_node = ClusterNode(ip="192.168.5.1", leader=False, cpus=123, gpus=5, RAM=128)
        cluster_config = ClusterConfig(cluster_nodes=[cluster_node])
        config = Config(
            management_admin_email_default="admin",
            management_admin_username_default="admin",
            management_admin_password_default="admin",
            management_admin_first_name_default="admin",
            management_admin_last_name_default="admin",
            management_admin_organization_default="admin",
            management_guest_username_default="admin",
            management_guest_password_default="admin",
            management_guest_first_name_default="admin",
            management_guest_last_name_default="admin",
            management_guest_email_default="admin",
            management_guest_organization_default="admin",
            ssh_admin_username="admin",
            ssh_admin_password="admin",
            ssh_agent_username="admin",
            ssh_agent_password="admin",
            metastore_user="admin",
            metastore_password="admin",
            metastore_database_name="admin",
            metastore_ip="admin",
            node_exporter_port=23,
            grafana_port=23,
            management_system_port=23,
            cadvisor_port=23,
            prometheus_port=23,
            node_exporter_pid_file="admin",
            pgadmin_port=23,
            csle_mgmt_webapp_pid_file="admin",
            docker_stats_manager_log_file="admin",
            docker_stats_manager_log_dir="admin",
            docker_stats_manager_port=23,
            docker_stats_manager_max_workers=23,
            docker_stats_manager_outfile="admin",
            docker_stats_manager_pidfile="admin",
            prometheus_pid_file="admin",
            prometheus_log_file="admin",
            prometheus_config_file="admin",
            default_log_dir="admin",
            cluster_config=cluster_config,
            node_exporter_log_file="admin",
            allow_registration=True,
            grafana_username="admin",
            grafana_password="admin",
            pgadmin_username="admin",
            pgadmin_password="admin",
            postgresql_log_dir="admin",
            nginx_log_dir="admin",
            flask_log_file="admin",
            cluster_manager_log_file="admin"
        )
        assert isinstance(config.to_dict(), dict)
        assert isinstance(Config.from_dict(config.to_dict()), Config)
        assert Config.from_dict(config.to_dict()).to_dict() == config.to_dict()
        assert Config.from_dict(config.to_dict()) == config

    def test_credential(self) -> None:
        """
        Tests creation and dict conversion of the Credential DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        assert isinstance(credential.to_dict(), dict)
        assert isinstance(Credential.from_dict(credential.to_dict()), Credential)
        assert Credential.from_dict(credential.to_dict()).to_dict() == credential.to_dict()
        assert Credential.from_dict(credential.to_dict()) == credential

    def test_default_network_firewall_config(self) -> None:
        """
        Tests creation and dict conversion of the DefaultNetworkFirewallConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        assert isinstance(default_net_fw_config.to_dict(), dict)
        assert isinstance(DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()),
                          DefaultNetworkFirewallConfig)
        assert DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()).to_dict() == \
               default_net_fw_config.to_dict()
        assert DefaultNetworkFirewallConfig.from_dict(default_net_fw_config.to_dict()) == default_net_fw_config

    def test_docker_stats_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagerConfig DTO

        :return: None
        """
        docker_statsmanager_config = DockerStatsManagerConfig(
            docker_stats_manager_log_file="testlog", docker_stats_manager_log_dir="logdir",
            docker_stats_manager_max_workers=10, time_step_len_seconds=30, docker_stats_manager_port=19, version="0.0.1"
        )
        assert isinstance(docker_statsmanager_config.to_dict(), dict)
        assert isinstance(DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()),
                          DockerStatsManagerConfig)
        assert DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()).to_dict() == \
               docker_statsmanager_config.to_dict()
        assert DockerStatsManagerConfig.from_dict(docker_statsmanager_config.to_dict()) == docker_statsmanager_config

    def test_docker_stats_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the DockerStatsManagersInfo DTO

        :return: None
        """
        docker_stats_monitor_dto = DockerStatsMonitorDTO(num_monitors=1, emulations=["testem"],
                                                         emulation_executions=[15])
        docker_statsmanagers_info = DockerStatsManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            docker_stats_managers_statuses=[docker_stats_monitor_dto], docker_stats_managers_running=[True])
        assert isinstance(docker_statsmanagers_info.to_dict(), dict)
        assert isinstance(DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()),
                          DockerStatsManagersInfo)
        assert DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()).to_dict() == \
               docker_statsmanagers_info.to_dict()
        assert DockerStatsManagersInfo.from_dict(docker_statsmanagers_info.to_dict()) == docker_statsmanagers_info

    def test_node_network_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeNetworkConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        assert isinstance(node_network_config.to_dict(), dict)
        assert isinstance(NodeNetworkConfig.from_dict(node_network_config.to_dict()), NodeNetworkConfig)
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()).to_dict() == node_network_config.to_dict()
        assert NodeNetworkConfig.from_dict(node_network_config.to_dict()) == node_network_config

    def test_node_resources_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeResourcesConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        assert isinstance(node_resources_config.to_dict(), dict)
        assert isinstance(NodeResourcesConfig.from_dict(node_resources_config.to_dict()), NodeResourcesConfig)
        assert NodeResourcesConfig.from_dict(node_resources_config.to_dict()).to_dict() == \
               node_resources_config.to_dict()
        assert NodeResourcesConfig.from_dict(node_resources_config.to_dict()) == node_resources_config

    def test_node_container_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeContainerConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        assert isinstance(node_container_config.to_dict(), dict)
        assert isinstance(NodeContainerConfig.from_dict(node_container_config.to_dict()), NodeContainerConfig)
        assert NodeContainerConfig.from_dict(node_container_config.to_dict()).to_dict() == \
               node_container_config.to_dict()
        assert NodeContainerConfig.from_dict(node_container_config.to_dict()) == node_container_config

    def test_node_firewall_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeFirewallConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        assert isinstance(node_firewall_config.to_dict(), dict)
        assert isinstance(NodeFirewallConfig.from_dict(node_firewall_config.to_dict()), NodeFirewallConfig)
        assert NodeFirewallConfig.from_dict(node_firewall_config.to_dict()).to_dict() == node_firewall_config.to_dict()
        assert NodeFirewallConfig.from_dict(node_firewall_config.to_dict()) == node_firewall_config

    def test_elk_config(self) -> None:
        """
        Tests creation and dict conversion of the ElkConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        elk_config = ElkConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            elk_manager_log_file="elk_manager.log", elk_manager_log_dir="/", elk_manager_max_workers=10,
            elastic_port=9200, kibana_port=5601, logstash_port=5044, time_step_len_seconds=15, elk_manager_port=50045,
            version="0.0.1")
        assert isinstance(elk_config.to_dict(), dict)
        assert isinstance(ElkConfig.from_dict(elk_config.to_dict()), ElkConfig)
        assert ElkConfig.from_dict(elk_config.to_dict()).to_dict() == elk_config.to_dict()
        assert ElkConfig.from_dict(elk_config.to_dict()) == elk_config

    def test_elk_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the ElkManagersInfo DTO

        :return: None
        """
        elk_dto = ElkDTO(elasticRunning=False, kibanaRunning=True, logstashRunning=True)
        elk_managers_info_info = ELKManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            elk_managers_statuses=[elk_dto], elk_managers_running=[True], local_kibana_port=5050,
            physical_server_ip="8.8.8.8")
        assert isinstance(elk_managers_info_info.to_dict(), dict)
        assert isinstance(ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()),
                          ELKManagersInfo)
        assert ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()).to_dict() == \
               elk_managers_info_info.to_dict()
        assert ELKManagersInfo.from_dict(elk_managers_info_info.to_dict()) == elk_managers_info_info

    def test_snort_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the SnortManagersInfo DTO

        :return: None
        """
        snort_dto = SnortIdsMonitorDTO(monitor_running=True, snort_ids_running=True)
        snort_managers_info = SnortIdsManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            snort_ids_managers_statuses=[snort_dto], snort_ids_managers_running=[True])
        assert isinstance(snort_managers_info.to_dict(), dict)
        assert isinstance(SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()),
                          SnortIdsManagersInfo)
        assert SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()).to_dict() == \
               snort_managers_info.to_dict()
        assert SnortIdsManagersInfo.from_dict(snort_managers_info.to_dict()) == snort_managers_info

    def test_ossec_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagersInfo DTO

        :return: None
        """
        ossec_dto = OSSECIdsMonitorDTO(monitor_running=True, ossec_ids_running=True)
        ossec_managers_info = OSSECIDSManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            ossec_ids_managers_statuses=[ossec_dto], ossec_ids_managers_running=[True])
        assert isinstance(ossec_managers_info.to_dict(), dict)
        assert isinstance(OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()),
                          OSSECIDSManagersInfo)
        assert OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()).to_dict() == \
               ossec_managers_info.to_dict()
        assert OSSECIDSManagersInfo.from_dict(ossec_managers_info.to_dict()) == ossec_managers_info

    def test_ryu_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the RyuManagersInfo DTO

        :return: None
        """
        ryu_dto = RyuDTO(ryu_running=True, monitor_running=False, port=3000, web_port=8080, controller="8.8.8.8",
                         kafka_ip="7.7.7.7", kafka_port=9090, time_step_len=30)
        ryu_managers_info = RyuManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            ryu_managers_statuses=[ryu_dto], ryu_managers_running=[True])
        assert isinstance(ryu_managers_info.to_dict(), dict)
        assert isinstance(RyuManagersInfo.from_dict(ryu_managers_info.to_dict()),
                          RyuManagersInfo)
        assert RyuManagersInfo.from_dict(ryu_managers_info.to_dict()).to_dict() == \
               ryu_managers_info.to_dict()
        assert RyuManagersInfo.from_dict(ryu_managers_info.to_dict()) == ryu_managers_info

    def test_host_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the HostManagersInfo DTO

        :return: None
        """
        host_dto = HostStatusDTO(
            monitor_running=True, filebeat_running=False, packetbeat_running=True, metricbeat_running=True,
            heartbeat_running=False)
        host_managers_info = HostManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            host_managers_statuses=[host_dto], host_managers_running=[True])
        assert isinstance(host_managers_info.to_dict(), dict)
        assert isinstance(HostManagersInfo.from_dict(host_managers_info.to_dict()),
                          HostManagersInfo)
        assert HostManagersInfo.from_dict(host_managers_info.to_dict()).to_dict() == \
               host_managers_info.to_dict()
        assert HostManagersInfo.from_dict(host_managers_info.to_dict()) == host_managers_info

    def test_kafka_managers_info(self) -> None:
        """
        Tests creation and dict conversion of the KafkaManagersInfo DTO

        :return: None
        """
        kafka_dto = KafkaDTO(running=True, topics=["topic1"])
        kafka_managers_info = KafkaManagersInfo(
            ips=["192.168.1.1"], ports=[3333], emulation_name="testem", execution_id=15,
            kafka_managers_statuses=[kafka_dto], kafka_managers_running=[True])
        assert isinstance(kafka_managers_info.to_dict(), dict)
        assert isinstance(KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()),
                          KafkaManagersInfo)
        assert KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()).to_dict() == \
               kafka_managers_info.to_dict()
        assert KafkaManagersInfo.from_dict(kafka_managers_info.to_dict()) == kafka_managers_info

    def test_kafka_topic(self) -> None:
        """
        Tests creation and dict conversion of the KafkaTopic DTO

        :return: None
        """
        kafka_topic = KafkaTopic(name="testname", num_replicas=10, num_partitions=15, attributes=["attr1"],
                                 retention_time_hours=10)
        assert isinstance(kafka_topic.to_dict(), dict)
        assert isinstance(KafkaTopic.from_dict(kafka_topic.to_dict()), KafkaTopic)
        assert KafkaTopic.from_dict(kafka_topic.to_dict()).to_dict() == kafka_topic.to_dict()
        assert KafkaTopic.from_dict(kafka_topic.to_dict()) == kafka_topic

    def test_kafka_config(self) -> None:
        """
        Tests creation and dict conversion of the KafkaConfig DTO

        :return: None
        """
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        node_container_config = NodeContainerConfig(
            name="node_name", ips_and_networks=[("net_1", container_network)], version="1.0.0", level="4",
            restart_policy="always", suffix="_2", os="Ubuntu", execution_ip_first_octet=15,
            docker_gw_bridge_ip="7.7.7.7", physical_host_ip="8.8.8.8"
        )
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        container_network = ContainerNetwork(
            name="testnet", subnet_mask="/24", bitmask="255.255.255.0", subnet_prefix="192.168.5", interface="eth1")
        default_net_fw_config = DefaultNetworkFirewallConfig(
            ip="192.168.5.1", default_gw="192.168.5.29", default_output="ACCEPT", default_input="DROP",
            default_forward="ACCEPT", network=container_network
        )
        route = ("8.8.8.8", "7.7.7.7")
        routes = set()
        routes.add(route)
        node_firewall_config = NodeFirewallConfig(
            hostname="my_hostname", output_accept=set("8.8.8.8"), input_accept=set("8.8.8.8"),
            forward_accept=set("8.8.8.8"), output_drop=set("8.8.8.8"), input_drop=set("8.8.8.8"),
            forward_drop=set("8.8.8.8"), routes=routes, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="192.172.1.1", ips_gw_default_policy_networks=[default_net_fw_config]
        )
        kafka_topic = KafkaTopic(name="testname", num_replicas=10, num_partitions=15, attributes=["attr1"],
                                 retention_time_hours=10)
        kafka_config = KafkaConfig(
            container=node_container_config, resources=node_resources_config, firewall_config=node_firewall_config,
            kafka_manager_log_file="elk_manager.log", kafka_manager_log_dir="/", kafka_manager_max_workers=10,
            time_step_len_seconds=15, kafka_manager_port=50045, version="0.0.1", topics=[kafka_topic])
        assert isinstance(kafka_config.to_dict(), dict)
        assert isinstance(KafkaConfig.from_dict(kafka_config.to_dict()), KafkaConfig)
        assert KafkaConfig.from_dict(kafka_config.to_dict()).to_dict() == kafka_config.to_dict()
        assert KafkaConfig.from_dict(kafka_config.to_dict()) == kafka_config

    def test_network_service(self) -> None:
        """
        Tests creation and dict conversion of the NetworkService DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        assert isinstance(network_service.to_dict(), dict)
        assert isinstance(NetworkService.from_dict(network_service.to_dict()), NetworkService)
        assert NetworkService.from_dict(network_service.to_dict()).to_dict() == network_service.to_dict()
        assert NetworkService.from_dict(network_service.to_dict()) == network_service

    def test_flag(self) -> None:
        """
        Tests creation and dict conversion of the Flag DTO

        :return: None
        """
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        assert isinstance(flag.to_dict(), dict)
        assert isinstance(Flag.from_dict(flag.to_dict()), Flag)
        assert Flag.from_dict(flag.to_dict()).to_dict() == flag.to_dict()
        assert Flag.from_dict(flag.to_dict()) == flag

    def test_node_flags_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeFlagsConfig DTO

        :return: None
        """
        flag = Flag(name="testflag", dir="/", id=10, path="/test.txt", requires_root=False, score=10)
        node_flags_config = NodeFlagsConfig(
            ip="8.8.8.8", flags=[flag], docker_gw_bridge_ip="9.9.9.9", physical_host_ip="168.22.11.2")
        assert isinstance(node_flags_config.to_dict(), dict)
        assert isinstance(NodeFlagsConfig.from_dict(node_flags_config.to_dict()), NodeFlagsConfig)
        assert NodeFlagsConfig.from_dict(node_flags_config.to_dict()).to_dict() == node_flags_config.to_dict()
        assert NodeFlagsConfig.from_dict(node_flags_config.to_dict()) == node_flags_config

    def test_node_services_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeServicesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        network_service = NetworkService(protocol=TransportProtocol.UDP, port=3000, name="testservice",
                                         credentials=[credential])
        node_services_config = NodeServicesConfig(ip="8.8.8.8", services=[network_service])
        assert isinstance(node_services_config.to_dict(), dict)
        assert isinstance(NodeServicesConfig.from_dict(node_services_config.to_dict()), NodeServicesConfig)
        assert NodeServicesConfig.from_dict(node_services_config.to_dict()).to_dict() == node_services_config.to_dict()
        assert NodeServicesConfig.from_dict(node_services_config.to_dict()) == node_services_config

    def test_node_traffic_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeTrafficConfig DTO

        :return: None
        """
        node_traffic_config = NodeTrafficConfig(
            ip="8.8.8.8", commands=["ls"], traffic_manager_log_file="traffic_manager.log", traffic_manager_log_dir="/",
            traffic_manager_port=3000, traffic_manager_max_workers=10, docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="7.7.7.7")
        assert isinstance(node_traffic_config.to_dict(), dict)
        assert isinstance(NodeTrafficConfig.from_dict(node_traffic_config.to_dict()), NodeTrafficConfig)
        assert NodeTrafficConfig.from_dict(node_traffic_config.to_dict()).to_dict() == node_traffic_config.to_dict()
        assert NodeTrafficConfig.from_dict(node_traffic_config.to_dict()) == node_traffic_config

    def test_user(self) -> None:
        """
        Tests creation and dict conversion of the User DTO

        :return: None
        """
        user = User(username="testuser", pw="mypw", root=True)
        assert isinstance(user.to_dict(), dict)
        assert isinstance(User.from_dict(user.to_dict()), User)
        assert User.from_dict(user.to_dict()).to_dict() == user.to_dict()
        assert User.from_dict(user.to_dict()) == user

    def test_node_users_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeUsersConfig DTO

        :return: None
        """
        user = User(username="testuser", pw="mypw", root=True)
        node_users_config = NodeUsersConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7", users=[user])
        assert isinstance(node_users_config.to_dict(), dict)
        assert isinstance(NodeUsersConfig.from_dict(node_users_config.to_dict()), NodeUsersConfig)
        assert NodeUsersConfig.from_dict(node_users_config.to_dict()).to_dict() == node_users_config.to_dict()
        assert NodeUsersConfig.from_dict(node_users_config.to_dict()) == node_users_config

    def test_node_vulnerability_config(self) -> None:
        """
        Tests creation and dict conversion of the NodeVulnerabilitiesConfig DTO

        :return: None
        """
        credential = Credential(username="testuser", pw="testpw", port=9311, protocol=TransportProtocol.UDP,
                                service="test", root=True)
        node_vuln_config = NodeVulnerabilityConfig(
            ip="8.8.8.8", docker_gw_bridge_ip="8.8.8.8", physical_host_ip="7.7.7.7",
            vuln_type=VulnType.RCE, protocol=TransportProtocol.TCP, credentials=[credential], cvss=2.0, cve="test_cve",
            service="myserv", root=True, name="testname", port=2510)
        assert isinstance(node_vuln_config.to_dict(), dict)
        assert isinstance(NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()), NodeVulnerabilityConfig)
        assert NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()).to_dict() == node_vuln_config.to_dict()
        assert NodeVulnerabilityConfig.from_dict(node_vuln_config.to_dict()) == node_vuln_config

    def test_ossec_ids_manager_config(self) -> None:
        """
        Tests creation and dict conversion of the OSSECIDSManagerConfig DTO

        :return: None
        """
        ossec_ids_manager_config = OSSECIDSManagerConfig(
            ossec_ids_manager_log_file="ossec.log", ossec_ids_manager_log_dir="/", ossec_ids_manager_max_workers=10,
            time_step_len_seconds=30,  ossec_ids_manager_port=1515, version="0.0.1")
        assert isinstance(ossec_ids_manager_config.to_dict(), dict)
        assert isinstance(OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()), OSSECIDSManagerConfig)
        assert OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()).to_dict() == \
               ossec_ids_manager_config.to_dict()
        assert OSSECIDSManagerConfig.from_dict(ossec_ids_manager_config.to_dict()) == ossec_ids_manager_config

    def test_ovs_switch_config(self) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :return: None
        """
        ovs_switch_config = OvsSwitchConfig(
            container_name="testcontainer", ip="8.8.8.8", openflow_protocols=["v1.0.0"], controller_ip="8.8.8.8",
            controller_port=3000, controller_transport_protocol="UDP", docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="168.156.2.2")
        assert isinstance(ovs_switch_config.to_dict(), dict)
        assert isinstance(OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()), OvsSwitchConfig)
        assert OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()).to_dict() == ovs_switch_config.to_dict()
        assert OvsSwitchConfig.from_dict(ovs_switch_config.to_dict()) == ovs_switch_config

    def test_ovs_config(self) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :return: None
        """
        ovs_switch_config = OvsSwitchConfig(
            container_name="testcontainer", ip="8.8.8.8", openflow_protocols=["v1.0.0"], controller_ip="8.8.8.8",
            controller_port=3000, controller_transport_protocol="UDP", docker_gw_bridge_ip="8.8.8.8",
            physical_host_ip="168.156.2.2")
        ovs_config = OVSConfig(switch_configs=[ovs_switch_config])
        assert isinstance(ovs_config.to_dict(), dict)
        assert isinstance(OVSConfig.from_dict(ovs_config.to_dict()), OVSConfig)
        assert OVSConfig.from_dict(ovs_config.to_dict()).to_dict() == ovs_config.to_dict()
        assert OVSConfig.from_dict(ovs_config.to_dict()) == ovs_config

    def test_resources_config(self) -> None:
        """
        Tests creation and dict conversion of the OVSConfig DTO

        :return: None
        """
        node_network_config = NodeNetworkConfig(
            interface="eth0", limit_packets_queue=3000, packet_delay_ms=0.1,
            packet_delay_jitter_ms=0.025, packet_delay_correlation_percentage=25,
            packet_delay_distribution=PacketDelayDistributionType.PARETO,
            packet_loss_type=PacketLossType.GEMODEL, packet_loss_rate_random_percentage=2,
            packet_loss_random_correlation_percentage=25, loss_state_markov_chain_p13=0.1,
            loss_state_markov_chain_p31=0.1, loss_state_markov_chain_p32=0.1, loss_state_markov_chain_p23=0.1,
            loss_state_markov_chain_p14=0.1, loss_gemodel_p=0.0001, loss_gemodel_r=0.999,
            loss_gemodel_h=0.0001, loss_gemodel_k=0.9999)
        node_resources_config = NodeResourcesConfig(
            container_name="my_container", num_cpus=10, available_memory_gb=100,
            ips_and_network_configs=[("net_1", node_network_config)], docker_gw_bridge_ip="docker_gw",
            physical_host_ip="192.168.1.1")
        resources_config = ResourcesConfig(node_resources_configurations=[node_resources_config])
        assert isinstance(resources_config.to_dict(), dict)
        assert isinstance(ResourcesConfig.from_dict(resources_config.to_dict()), ResourcesConfig)
        assert ResourcesConfig.from_dict(resources_config.to_dict()).to_dict() == resources_config.to_dict()
        assert ResourcesConfig.from_dict(resources_config.to_dict()) == resources_config
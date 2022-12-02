# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: host_manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12host_manager.proto\"\x14\n\x12StopHostMonitorMsg\"Z\n\x13StartHostMonitorMsg\x12\x10\n\x08kafka_ip\x18\x01 \x01(\t\x12\x12\n\nkafka_port\x18\x02 \x01(\x05\x12\x1d\n\x15time_step_len_seconds\x18\x04 \x01(\x05\"\x11\n\x0fStopFilebeatMsg\"\x12\n\x10StartFilebeatMsg\"\x97\x02\n\x11\x43onfigFilebeatMsg\x12\x11\n\tkibana_ip\x18\x01 \x01(\t\x12\x13\n\x0bkibana_port\x18\x02 \x01(\x05\x12\x12\n\nelastic_ip\x18\x03 \x01(\t\x12\x14\n\x0c\x65lastic_port\x18\x04 \x01(\x05\x12\x1a\n\x12num_elastic_shards\x18\x05 \x01(\x05\x12\x16\n\x0ereload_enabled\x18\x06 \x01(\x08\x12\x10\n\x08kafka_ip\x18\x07 \x01(\t\x12\x12\n\nkafka_port\x18\x08 \x01(\x05\x12\r\n\x05kafka\x18\t \x01(\x08\x12\x14\n\x0ckafka_topics\x18\n \x03(\t\x12\x18\n\x10\x66ilebeat_modules\x18\x0b \x03(\t\x12\x17\n\x0flog_files_paths\x18\x0c \x03(\t\"\x13\n\x11StopPacketbeatMsg\"\x14\n\x12StartPacketbeatMsg\"\x83\x01\n\x13\x43onfigPacketbeatMsg\x12\x11\n\tkibana_ip\x18\x01 \x01(\t\x12\x13\n\x0bkibana_port\x18\x02 \x01(\x05\x12\x12\n\nelastic_ip\x18\x03 \x01(\t\x12\x14\n\x0c\x65lastic_port\x18\x04 \x01(\x05\x12\x1a\n\x12num_elastic_shards\x18\x05 \x01(\x05\"\x13\n\x11StopMetricbeatMsg\"\x14\n\x12StartMetricbeatMsg\"\xdd\x01\n\x13\x43onfigMetricbeatMsg\x12\x11\n\tkibana_ip\x18\x01 \x01(\t\x12\x13\n\x0bkibana_port\x18\x02 \x01(\x05\x12\x12\n\nelastic_ip\x18\x03 \x01(\t\x12\x14\n\x0c\x65lastic_port\x18\x04 \x01(\x05\x12\x1a\n\x12num_elastic_shards\x18\x05 \x01(\x05\x12\x10\n\x08kafka_ip\x18\x06 \x01(\t\x12\x12\n\nkafka_port\x18\x07 \x01(\x05\x12\x16\n\x0ereload_enabled\x18\x08 \x01(\x08\x12\x1a\n\x12metricbeat_modules\x18\x0c \x03(\t\"\x12\n\x10GetHostStatusMsg\"\x95\x01\n\rHostStatusDTO\x12\x17\n\x0fmonitor_running\x18\x01 \x01(\x08\x12\x18\n\x10\x66ilebeat_running\x18\x02 \x01(\x08\x12\x1a\n\x12packetbeat_running\x18\x03 \x01(\x08\x12\x1a\n\x12metricbeat_running\x18\x04 \x01(\x08\x12\x19\n\x11heartbeat_running\x18\x05 \x01(\x08\"G\n\x11GetHostMetricsMsg\x12\x1b\n\x13\x66\x61iled_auth_last_ts\x18\x01 \x01(\x02\x12\x15\n\rlogin_last_ts\x18\x02 \x01(\x02\"\xd1\x01\n\x0eHostMetricsDTO\x12\x1b\n\x13num_logged_in_users\x18\x01 \x01(\x05\x12!\n\x19num_failed_login_attempts\x18\x02 \x01(\x05\x12\x1c\n\x14num_open_connections\x18\x03 \x01(\x05\x12\x18\n\x10num_login_events\x18\x04 \x01(\x05\x12\x15\n\rnum_processes\x18\x05 \x01(\x05\x12\x11\n\tnum_users\x18\x06 \x01(\x05\x12\n\n\x02ip\x18\x07 \x01(\t\x12\x11\n\ttimestamp\x18\x08 \x01(\x02\"\x12\n\x10StopHeartbeatMsg\"\x13\n\x11StartHeartbeatMsg\"\x9c\x01\n\x12\x43onfigHeartbeatMsg\x12\x11\n\tkibana_ip\x18\x01 \x01(\t\x12\x13\n\x0bkibana_port\x18\x02 \x01(\x05\x12\x12\n\nelastic_ip\x18\x03 \x01(\t\x12\x14\n\x0c\x65lastic_port\x18\x04 \x01(\x05\x12\x1a\n\x12num_elastic_shards\x18\x05 \x01(\x05\x12\x18\n\x10hosts_to_monitor\x18\x06 \x03(\t2\x98\x07\n\x0bHostManager\x12\x38\n\x0fstopHostMonitor\x12\x13.StopHostMonitorMsg\x1a\x0e.HostStatusDTO\"\x00\x12:\n\x10startHostMonitor\x12\x14.StartHostMonitorMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x34\n\rgetHostStatus\x12\x11.GetHostStatusMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x37\n\x0egetHostMetrics\x12\x12.GetHostMetricsMsg\x1a\x0f.HostMetricsDTO\"\x00\x12\x32\n\x0cstopFilebeat\x12\x10.StopFilebeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x34\n\rstartFilebeat\x12\x11.StartFilebeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x36\n\x0e\x63onfigFilebeat\x12\x12.ConfigFilebeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x36\n\x0estopPacketbeat\x12\x12.StopPacketbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x38\n\x0fstartPacketbeat\x12\x13.StartPacketbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12:\n\x10\x63onfigPacketbeat\x12\x14.ConfigPacketbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x36\n\x0estopMetricbeat\x12\x12.StopMetricbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x38\n\x0fstartMetricbeat\x12\x13.StartMetricbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12:\n\x10\x63onfigMetricbeat\x12\x14.ConfigMetricbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x34\n\rstopHeartbeat\x12\x11.StopHeartbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x36\n\x0estartHeartbeat\x12\x12.StartHeartbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x12\x38\n\x0f\x63onfigHeartbeat\x12\x13.ConfigHeartbeatMsg\x1a\x0e.HostStatusDTO\"\x00\x62\x06proto3')



_STOPHOSTMONITORMSG = DESCRIPTOR.message_types_by_name['StopHostMonitorMsg']
_STARTHOSTMONITORMSG = DESCRIPTOR.message_types_by_name['StartHostMonitorMsg']
_STOPFILEBEATMSG = DESCRIPTOR.message_types_by_name['StopFilebeatMsg']
_STARTFILEBEATMSG = DESCRIPTOR.message_types_by_name['StartFilebeatMsg']
_CONFIGFILEBEATMSG = DESCRIPTOR.message_types_by_name['ConfigFilebeatMsg']
_STOPPACKETBEATMSG = DESCRIPTOR.message_types_by_name['StopPacketbeatMsg']
_STARTPACKETBEATMSG = DESCRIPTOR.message_types_by_name['StartPacketbeatMsg']
_CONFIGPACKETBEATMSG = DESCRIPTOR.message_types_by_name['ConfigPacketbeatMsg']
_STOPMETRICBEATMSG = DESCRIPTOR.message_types_by_name['StopMetricbeatMsg']
_STARTMETRICBEATMSG = DESCRIPTOR.message_types_by_name['StartMetricbeatMsg']
_CONFIGMETRICBEATMSG = DESCRIPTOR.message_types_by_name['ConfigMetricbeatMsg']
_GETHOSTSTATUSMSG = DESCRIPTOR.message_types_by_name['GetHostStatusMsg']
_HOSTSTATUSDTO = DESCRIPTOR.message_types_by_name['HostStatusDTO']
_GETHOSTMETRICSMSG = DESCRIPTOR.message_types_by_name['GetHostMetricsMsg']
_HOSTMETRICSDTO = DESCRIPTOR.message_types_by_name['HostMetricsDTO']
_STOPHEARTBEATMSG = DESCRIPTOR.message_types_by_name['StopHeartbeatMsg']
_STARTHEARTBEATMSG = DESCRIPTOR.message_types_by_name['StartHeartbeatMsg']
_CONFIGHEARTBEATMSG = DESCRIPTOR.message_types_by_name['ConfigHeartbeatMsg']
StopHostMonitorMsg = _reflection.GeneratedProtocolMessageType('StopHostMonitorMsg', (_message.Message,), {
  'DESCRIPTOR' : _STOPHOSTMONITORMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StopHostMonitorMsg)
  })
_sym_db.RegisterMessage(StopHostMonitorMsg)

StartHostMonitorMsg = _reflection.GeneratedProtocolMessageType('StartHostMonitorMsg', (_message.Message,), {
  'DESCRIPTOR' : _STARTHOSTMONITORMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StartHostMonitorMsg)
  })
_sym_db.RegisterMessage(StartHostMonitorMsg)

StopFilebeatMsg = _reflection.GeneratedProtocolMessageType('StopFilebeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STOPFILEBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StopFilebeatMsg)
  })
_sym_db.RegisterMessage(StopFilebeatMsg)

StartFilebeatMsg = _reflection.GeneratedProtocolMessageType('StartFilebeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STARTFILEBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StartFilebeatMsg)
  })
_sym_db.RegisterMessage(StartFilebeatMsg)

ConfigFilebeatMsg = _reflection.GeneratedProtocolMessageType('ConfigFilebeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGFILEBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:ConfigFilebeatMsg)
  })
_sym_db.RegisterMessage(ConfigFilebeatMsg)

StopPacketbeatMsg = _reflection.GeneratedProtocolMessageType('StopPacketbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STOPPACKETBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StopPacketbeatMsg)
  })
_sym_db.RegisterMessage(StopPacketbeatMsg)

StartPacketbeatMsg = _reflection.GeneratedProtocolMessageType('StartPacketbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STARTPACKETBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StartPacketbeatMsg)
  })
_sym_db.RegisterMessage(StartPacketbeatMsg)

ConfigPacketbeatMsg = _reflection.GeneratedProtocolMessageType('ConfigPacketbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGPACKETBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:ConfigPacketbeatMsg)
  })
_sym_db.RegisterMessage(ConfigPacketbeatMsg)

StopMetricbeatMsg = _reflection.GeneratedProtocolMessageType('StopMetricbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STOPMETRICBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StopMetricbeatMsg)
  })
_sym_db.RegisterMessage(StopMetricbeatMsg)

StartMetricbeatMsg = _reflection.GeneratedProtocolMessageType('StartMetricbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STARTMETRICBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StartMetricbeatMsg)
  })
_sym_db.RegisterMessage(StartMetricbeatMsg)

ConfigMetricbeatMsg = _reflection.GeneratedProtocolMessageType('ConfigMetricbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGMETRICBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:ConfigMetricbeatMsg)
  })
_sym_db.RegisterMessage(ConfigMetricbeatMsg)

GetHostStatusMsg = _reflection.GeneratedProtocolMessageType('GetHostStatusMsg', (_message.Message,), {
  'DESCRIPTOR' : _GETHOSTSTATUSMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:GetHostStatusMsg)
  })
_sym_db.RegisterMessage(GetHostStatusMsg)

HostStatusDTO = _reflection.GeneratedProtocolMessageType('HostStatusDTO', (_message.Message,), {
  'DESCRIPTOR' : _HOSTSTATUSDTO,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:HostStatusDTO)
  })
_sym_db.RegisterMessage(HostStatusDTO)

GetHostMetricsMsg = _reflection.GeneratedProtocolMessageType('GetHostMetricsMsg', (_message.Message,), {
  'DESCRIPTOR' : _GETHOSTMETRICSMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:GetHostMetricsMsg)
  })
_sym_db.RegisterMessage(GetHostMetricsMsg)

HostMetricsDTO = _reflection.GeneratedProtocolMessageType('HostMetricsDTO', (_message.Message,), {
  'DESCRIPTOR' : _HOSTMETRICSDTO,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:HostMetricsDTO)
  })
_sym_db.RegisterMessage(HostMetricsDTO)

StopHeartbeatMsg = _reflection.GeneratedProtocolMessageType('StopHeartbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STOPHEARTBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StopHeartbeatMsg)
  })
_sym_db.RegisterMessage(StopHeartbeatMsg)

StartHeartbeatMsg = _reflection.GeneratedProtocolMessageType('StartHeartbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _STARTHEARTBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:StartHeartbeatMsg)
  })
_sym_db.RegisterMessage(StartHeartbeatMsg)

ConfigHeartbeatMsg = _reflection.GeneratedProtocolMessageType('ConfigHeartbeatMsg', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGHEARTBEATMSG,
  '__module__' : 'host_manager_pb2'
  # @@protoc_insertion_point(class_scope:ConfigHeartbeatMsg)
  })
_sym_db.RegisterMessage(ConfigHeartbeatMsg)

_HOSTMANAGER = DESCRIPTOR.services_by_name['HostManager']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STOPHOSTMONITORMSG._serialized_start=22
  _STOPHOSTMONITORMSG._serialized_end=42
  _STARTHOSTMONITORMSG._serialized_start=44
  _STARTHOSTMONITORMSG._serialized_end=134
  _STOPFILEBEATMSG._serialized_start=136
  _STOPFILEBEATMSG._serialized_end=153
  _STARTFILEBEATMSG._serialized_start=155
  _STARTFILEBEATMSG._serialized_end=173
  _CONFIGFILEBEATMSG._serialized_start=176
  _CONFIGFILEBEATMSG._serialized_end=455
  _STOPPACKETBEATMSG._serialized_start=457
  _STOPPACKETBEATMSG._serialized_end=476
  _STARTPACKETBEATMSG._serialized_start=478
  _STARTPACKETBEATMSG._serialized_end=498
  _CONFIGPACKETBEATMSG._serialized_start=501
  _CONFIGPACKETBEATMSG._serialized_end=632
  _STOPMETRICBEATMSG._serialized_start=634
  _STOPMETRICBEATMSG._serialized_end=653
  _STARTMETRICBEATMSG._serialized_start=655
  _STARTMETRICBEATMSG._serialized_end=675
  _CONFIGMETRICBEATMSG._serialized_start=678
  _CONFIGMETRICBEATMSG._serialized_end=899
  _GETHOSTSTATUSMSG._serialized_start=901
  _GETHOSTSTATUSMSG._serialized_end=919
  _HOSTSTATUSDTO._serialized_start=922
  _HOSTSTATUSDTO._serialized_end=1071
  _GETHOSTMETRICSMSG._serialized_start=1073
  _GETHOSTMETRICSMSG._serialized_end=1144
  _HOSTMETRICSDTO._serialized_start=1147
  _HOSTMETRICSDTO._serialized_end=1356
  _STOPHEARTBEATMSG._serialized_start=1358
  _STOPHEARTBEATMSG._serialized_end=1376
  _STARTHEARTBEATMSG._serialized_start=1378
  _STARTHEARTBEATMSG._serialized_end=1397
  _CONFIGHEARTBEATMSG._serialized_start=1400
  _CONFIGHEARTBEATMSG._serialized_end=1556
  _HOSTMANAGER._serialized_start=1559
  _HOSTMANAGER._serialized_end=2479
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: operatorpb.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10operatorpb.proto\x12\noperatorpb\"\x94\x01\n\x07Message\x12\x35\n\x0cmessage_type\x18\x01 \x01(\x0e\x32\x1f.operatorpb.Message.MessageType\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"D\n\x0bMessageType\x12\x0e\n\nSessionCmd\x10\x00\x12\x14\n\x10SessionCmdOutput\x10\x01\x12\x0f\n\x0bSessionInfo\x10\x02\"%\n\nSessionCmd\x12\x0b\n\x03\x63md\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\"1\n\x10SessionCmdOutput\x12\x11\n\tcmdOutput\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\"\xbc\x01\n\x0bSessionInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\x12\x0b\n\x03pid\x18\x04 \x01(\r\x12*\n\x04user\x18\x05 \x01(\x0b\x32\x1c.operatorpb.SessionInfo.User\x12,\n\x06groups\x18\x06 \x03(\x0b\x32\x1c.operatorpb.SessionInfo.User\x1a \n\x04User\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'operatorpb_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=33
  _MESSAGE._serialized_end=181
  _MESSAGE_MESSAGETYPE._serialized_start=113
  _MESSAGE_MESSAGETYPE._serialized_end=181
  _SESSIONCMD._serialized_start=183
  _SESSIONCMD._serialized_end=220
  _SESSIONCMDOUTPUT._serialized_start=222
  _SESSIONCMDOUTPUT._serialized_end=271
  _SESSIONINFO._serialized_start=274
  _SESSIONINFO._serialized_end=462
  _SESSIONINFO_USER._serialized_start=430
  _SESSIONINFO_USER._serialized_end=462
# @@protoc_insertion_point(module_scope)

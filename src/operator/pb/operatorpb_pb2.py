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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10operatorpb.proto\x12\noperatorpb\"\xe4\x01\n\x07Message\x12\x35\n\x0cmessage_type\x18\x01 \x01(\x0e\x32\x1f.operatorpb.Message.MessageType\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"\x93\x01\n\x0bMessageType\x12\t\n\x05\x45rror\x10\x00\x12\x10\n\x0cRegistration\x10\x01\x12\x1c\n\x18RegistrationConfirmation\x10\x02\x12\r\n\tServerCmd\x10\x03\x12\x13\n\x0fServerCmdOutput\x10\x04\x12\x0f\n\x0bSessionInfo\x10\x05\x12\x14\n\x10SessionConnected\x10\x06\"\x97\x01\n\x05\x45rror\x12/\n\nerror_type\x18\x01 \x01(\x0e\x32\x1b.operatorpb.Error.ErrorType\x12\x0f\n\x07message\x18\x02 \x01(\t\"L\n\tErrorType\x12\x11\n\rMessageDecode\x10\x00\x12\x10\n\x0cRegistration\x10\x01\x12\r\n\tServerCmd\x10\x02\x12\x0b\n\x07Session\x10\x03\"*\n\x0cRegistration\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"&\n\x18RegistrationConfirmation\x12\n\n\x02id\x18\x01 \x01(\t\"\x18\n\tServerCmd\x12\x0b\n\x03\x63md\x18\x01 \x01(\t\"$\n\x0fServerCmdOutput\x12\x11\n\tcmdOutput\x18\x01 \x01(\t\"\xbc\x01\n\x0bSessionInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\x12\n\n\x02os\x18\x03 \x01(\t\x12\x0b\n\x03pid\x18\x04 \x01(\r\x12*\n\x04user\x18\x05 \x01(\x0b\x32\x1c.operatorpb.SessionInfo.User\x12,\n\x06groups\x18\x06 \x03(\x0b\x32\x1c.operatorpb.SessionInfo.User\x1a \n\x04User\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04name\x18\x02 \x01(\t\" \n\x10SessionConnected\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'operatorpb_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=33
  _MESSAGE._serialized_end=261
  _MESSAGE_MESSAGETYPE._serialized_start=114
  _MESSAGE_MESSAGETYPE._serialized_end=261
  _ERROR._serialized_start=264
  _ERROR._serialized_end=415
  _ERROR_ERRORTYPE._serialized_start=339
  _ERROR_ERRORTYPE._serialized_end=415
  _REGISTRATION._serialized_start=417
  _REGISTRATION._serialized_end=459
  _REGISTRATIONCONFIRMATION._serialized_start=461
  _REGISTRATIONCONFIRMATION._serialized_end=499
  _SERVERCMD._serialized_start=501
  _SERVERCMD._serialized_end=525
  _SERVERCMDOUTPUT._serialized_start=527
  _SERVERCMDOUTPUT._serialized_end=563
  _SESSIONINFO._serialized_start=566
  _SESSIONINFO._serialized_end=754
  _SESSIONINFO_USER._serialized_start=722
  _SESSIONINFO_USER._serialized_end=754
  _SESSIONCONNECTED._serialized_start=756
  _SESSIONCONNECTED._serialized_end=788
# @@protoc_insertion_point(module_scope)
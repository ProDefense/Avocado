# proto

This directory contains the protocol buffer definitions.
Proto3 is used https://developers.google.com/protocol-buffers/docs/proto3

## Protocol Buffers
Compile the protocol buffers into python code with this:
```
$ protoc -I implant/ --python_out=../pb implant/implantpb.proto
$ protoc -I operator/ --python_out=../pb operator/operatorpb.proto
```

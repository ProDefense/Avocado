# server

This contains code for the C2 server.


## Protocol Buffers
Compile the protocol buffers into python code with this:
```
$ protoc -I ../proto/implant/ --python_out=./pb ../proto/implant/implantpb.proto
$ protoc -I ../proto/operator/ --python_out=./pb ../proto/operator/operatorpb.proto
```

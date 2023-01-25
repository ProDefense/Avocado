# server

This contains code for the C2 server.

## UI under construction

Using the tool pyuic6 to convert *.ui xml files generated in QtCreator into python code.

Usage:
```angular2html
$ pyuic6 ui/main_window.ui > main_window.py
```


## Protocol Buffers
Compile the protocol buffers into python code with this:
```
$ protoc -I../proto/implant/ --python_out=./pb ../proto/implant/implantpb.proto
```

# operator

This contains code for the C2 operator.

There are CLI and GUI versions of the operator.

## UI under construction

Using the tool pyuic6 to convert *.ui xml files generated in QtCreator into python code.

Usage:
```angular2html
$ pyuic6 gui/resources/ui/main_window.ui > gui/views/main_window.py
```

## Protocol Buffers
Compile the protocol buffers into python code with this:
```
$ protoc -I ../proto/implant/ --python_out=./pb ../proto/implant/implantpb.proto
$ protoc -I ../proto/operator/ --python_out=./pb ../proto/operator/operatorpb.proto
```

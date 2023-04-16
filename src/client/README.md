# operator
This contains code for the C2 operator.

There are CLI and GUI versions of the operator.

## GUI 
The GUI requires pyqt. 

Installation:
```angular2html
$ pip install -r gui-requirements.txt
```

## Implant Generation
Rust is needed to generate implants. 

Generation Dependencies:
- rustup
- musl-gcc

## GUI Development
Use the tool pyuic6 to convert *.ui xml files generated in QtCreator into python code.

Usage:
```angular2html
$ pyuic6 gui/resources/ui/main_window.ui > gui/views/main_window.py
```

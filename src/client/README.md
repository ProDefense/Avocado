# Operator
This contains code for the C2 operator.

There are CLI and GUI versions of the operator.

## GUI 
The GUI requires python and pyqt library. 

Installation (Arch):
```angular2html
$ pacman -Sy python python-pip --noconfirm
$ pip install -r ../requirements.txt
$ pip install -r gui-requirements.txt
```

## Implant Generation
Rust is needed to generate implants. 

Installation (Arch)
```angular2html
$ pacman -Sy base-devel rustup mingw-w64-gcc musl --noconfirm
$ rustup default nightly
$ rustup target add x86_64-unknown-linux-musl
$ rustup target add x86_64-pc-windows-gnu
$ rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu
$ cargo check --release --target=x86_64-pc-windows-gnu --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked windows"
$ cargo check --release --target=x86_64-unknown-linux-musl --manifest-path=$HOME/src/implant/Cargo.toml || echo "checked linux"
```

## GUI Development
Use the tool pyuic6 to convert *.ui xml files generated in QtCreator into python code.

Usage:
```angular2html
$ pyuic6 gui/resources/ui/main_window.ui > gui/views/main_window.py
```

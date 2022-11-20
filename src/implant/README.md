# implant

This is the implant that runs on a target machine.

For developer testing:
```
$ cargo run
```

To compile, run with cargo:
```
$ cargo build --release --target=x86_64-unknown-linux-musl
```

Dependencies:
- rustup
- musl-gcc
- protoc

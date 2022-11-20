# implant


This is the implant that runs on a target machine.
To compile, run with cargo:
```
$ cargo build --release --target=x86_64-unknown-linux-musl
```

For developer testing:
```
$ cargo run
```

Dependencies:
- rustup
- musl-gcc
- protoc
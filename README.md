# Avocado :avocado:

Avocado is currently in development. Expect bugs

## Running Avocado for development

1. Build and run docker container
```
$ docker build . -t avocado
$ docker run --rm --name avocado -it avocado
```

2. Inside the container, generate mTLS certs (these certs are ONLY to be used in development)
```
avocado$ cd src/certs
avocado$ ./mkcerts.sh
```

3. Inside the container, run the server
```
avocado$ cd src/server
avocado$ ./main.py
```

4. Inside the container, compile and run the implant.
```
avocado$ cd src/implant
avocado$ cargo run
```

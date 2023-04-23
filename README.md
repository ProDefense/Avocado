<h1 align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/70419560/226087624-a4c6a4b6-11fc-4195-9878-cb19b6089b66.png">
    <img alt="Shows different variants of the logo in dark and light mode." src="https://user-images.githubusercontent.com/70419560/226087634-67c086ce-2ea6-422a-b3a2-ade3822de914.png">
  </picture>
  Avocado C2
</h1>

<p align="center">
  Avocado is a C2 framework currently in development. Expect bugs.
  <br>

  <!-- Open github issues -->
  <a href="https://github.com/ProDefense/Avocado/issues?q=is%3Aissue+is%3Aopen+">
    <img src="https://img.shields.io/github/issues-raw/prodefense/avocado?color=f38ba8&style=for-the-badge">
  </a>

  <!-- Closed github issues -->
  <a href="https://github.com/ProDefense/Avocado/issues?q=is%3Aissue+is%3Aclosed">
    <img src="https://img.shields.io/github/issues-closed-raw/prodefense/avocado?color=a6e3a1&style=for-the-badge">
  </a>

  <!-- License -->
  <img src="https://img.shields.io/github/license/prodefense/avocado?color=b4befe&style=for-the-badge">

  ![demo](assets/avocado.gif)
</p>

## Quick Start

Avocado currently only supports a Docker installation.
1. **Build docker container**
```
$ docker build . -t avocado
```

1.1 **Check if port 5432 is in use & stop if necessary. By default, postgresql should be running on there if installed. Then create/start the container**
```
$ sudo netstat -plnt | grep 5432
$ service postgresql stop
$ docker run -d --name avocado-container -p 5432:5432 avocado
```

1.2 **If hash is outputted after previous command, container was built successfully. Grab container ID and exec docker. This assumes you have more than one Docker container. If not the case, ignore first two commands and use isolated line**
```
$ docker ps -a
$ docker exec -it <avocado_container ID> /bin/bash

$ docker exec -it $(docker ps -aq) /bin/bash
```

2 **Verify database creation & tables are created. Once verified exit to go back to Docker interface**
```
$ psql -U postgres
postgres-# \c loot
loot-# \dt
loot-# \q
```

3. **Inside the container, run the server**
```
avocado$ cd src/server
avocado$ ./main.py
```

4. **Inside the container, compile and run the implant.**
```
> generate
```
The implant will be output into the current working directory.

5. **Clean containers & free up space once done**
```
$ docker system prune -a
```

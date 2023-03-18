<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/70419560/226087624-a4c6a4b6-11fc-4195-9878-cb19b6089b66.png">
  <img alt="Shows different variants of the logo in dark and light mode." src="https://user-images.githubusercontent.com/70419560/226087634-67c086ce-2ea6-422a-b3a2-ade3822de914.png">
</picture>

Avocado is a C2 framework currently in development. Expect bugs.

![GitHub issues](https://img.shields.io/github/issues-raw/prodefense/avocado?color=f38ba8&style=for-the-badge)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/prodefense/avocado?color=a6e3a1&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/prodefense/avocado?color=b4befe&style=for-the-badge)

## Quick Start
![demo](assets/avocado.gif)

Avocado currently only supports a Docker installation.
1. **Build and run docker container**
```
$ docker build . -t avocado
$ docker run --rm --name avocado -it avocado
```

2. **Inside the container, run the server**
```
avocado$ cd src/server
avocado$ ./main.py
```

3. **Inside the container, compile and run the implant.**
```
> generate
```
The implant will be output into the current working directory.

# Avocado Dev Branch :avocado:

Pre-stable development branch dedicated towards working on items before they are released towards the main branch.

## Usage

### Running the test code
1. First, generate CA certs for mTLS (TODO: automatically do this in python)
```
$ cd Avocado/src/certs/
$ ./mkcerts.sh
```

2. Run the server
```
$ cd Avocado/src/server
$ ./main.py
```

3. Run the implant
```
$ cd Avocado/src/implant
$ ./main.py
```


## Packages

The server relies on Python 3.10. 
Install the requirements.
```angular2html
$ pip install requirements.txt
```

Add the packages that you've added to the requirements text.
```angular2html
$ pip freeze > requirements.txt
```

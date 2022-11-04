#!/bin/bash
# Generate TESTING certs with mkcert
# https://github.com/FiloSottile/mkcert

CURR=$PWD
mkdir client
mkdir server
mkdir operator

cd $CURR/server
CAROOT=$PWD mkcert 'avocado-server.c2'

cd $CURR/client
CAROOT=$PWD mkcert -client 'avocado-implant.c2'

cd $CURR/operator
CAROOT=$PWD mkcert -client 'avocado-operator.c2'

cd $CURR

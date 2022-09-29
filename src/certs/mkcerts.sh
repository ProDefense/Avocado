#!/bin/bash
# Generate TESTING certs with mkcert
# https://github.com/FiloSottile/mkcert

CURR=$PWD
mkdir client
mkdir server

cd $CURR/server
CAROOT=$PWD/server mkcert 'avacado-server.c2'

cd $CURR/client
CAROOT=$PWD/client mkcert -client 'avacado-implant.c2'

cd $CURR

#!/bin/bash
# Generate TESTING certs with mkcert
# https://github.com/FiloSottile/mkcert

CURR=$PWD
mkdir client

cd $CURR/client
CAROOT=$PWD mkcert -client 'avocado-implant.c2'

cd $CURR

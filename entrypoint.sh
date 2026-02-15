#!/bin/sh
set -e
cd /home/avocado/src

case "${1:-server}" in
  server)
    exec python3 avocado-server
    ;;
  operator)
    exec python3 avocado-operator-cli
    ;;
  *)
    exec "$@"
    ;;
esac

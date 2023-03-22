#!/usr/bin/env python3
import threading
from pb import operatorpb_pb2
from listener.listener import Listener

# convert message to protobuf and send to server

def shell_cli (listener, response_received, session_closed):
    session_closed.clear()  

    while True:
        response_received.wait()
        userin = input("[session] > ") 

        if not userin:
            continue

        listener.send(userin)

        if (userin=="exit"):
            break

        response_received.clear()

    session_closed.set()  

def handler(listener, response_received, session_closed):
    while True:
        message = listener.listen() 

        if not message:
            break

        elif message.message_type == operatorpb_pb2.Message.MessageType.SessionInfo:
            session_info = operatorpb_pb2.SessionInfo()
            session_info.ParseFromString(message.data)
            print("New session!")

        elif message.message_type == operatorpb_pb2.Message.MessageType.ServerCmdOutput:
            cmd_output = operatorpb_pb2.ServerCmdOutput()
            cmd_output.ParseFromString(message.data)
            print(cmd_output.cmdOutput)

        elif message.message_type == operatorpb_pb2.Message.MessageType.SessionConnected:
            session_connected = operatorpb_pb2.SessionConnected()
            session_connected.ParseFromString(message.data)
            print(f"Connected to session {session_connected.addr}")

            threading.Thread(target=shell_cli, args=(listener, response_received, session_closed)).start()

        response_received.set() 

def cli(listener, response_received, session_closed):
    while True:
        response_received.wait()
        session_closed.wait()

        msg = input("[Avocado] > ")

        if not msg:
            continue

        response_received.clear()  
        listener.send(msg)

        if msg.lower() == "exit":
            print("[+]Connection Terminated")
            break

def main():
    # TODO prompt the user to enter host/port instead
    hostname = "127.0.0.1"
    port = 12345

    listener = Listener(hostname, port)

    # response_received and session_closed are workarounds for some i/o issues
    # e.g. the server response overwrites the user input prompt

    response_received = threading.Event()  
    session_closed = threading.Event()  
    response_received.set()  
    session_closed.set()  

    threading.Thread(target=handler, args=(listener, response_received, session_closed)).start()

    cli(listener, response_received, session_closed)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import socket
import threading
from pb import operatorpb_pb2

# convert message to protobuf and send to server
def sendServer(message, server):
    server_cmd = operatorpb_pb2.ServerCmd(cmd=message.encode("ascii"))
    message = operatorpb_pb2.Message(
        message_type=operatorpb_pb2.Message.MessageType.ServerCmd, 
        data=server_cmd.SerializeToString()
    )
    server.send(message.SerializeToString())

def shell_cli (server, command_sent, session_enabled):
    session_enabled.clear()  

    while True:
        command_sent.wait()
        userin = input("[session] > ") 

        if not userin:
            continue

        sendServer(userin, server)

        if (userin=="exit"):
            break

        command_sent.clear()

    session_enabled.set()  

def listen(server, command_sent, session_enabled):
    while True: 
        data = server.recv(1024)

        message = operatorpb_pb2.Message()
        message.ParseFromString(data)

        if message.message_type == operatorpb_pb2.Message.MessageType.SessionInfo:
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

            t = threading.Thread(target=shell_cli, args=(server, command_sent, session_enabled,))
            t.start()

        elif (not data):
            break

        command_sent.set() 
    server.close()

def cli(server, command_sent, session_enabled):
    while True:
        # Wait until the server replies or session closed before prompting for input
        command_sent.wait()
        session_enabled.wait()

        msg = input("[Avocado] > ")

        if not msg:
            continue

        command_sent.clear()  
        sendServer(msg, server)

        if msg.lower() == "exit":
            print("[+]Connection Terminated")
            break

def main():
    # TODO prompt the user to enter host/port instead
    host = "127.0.0.1"
    port = 12345

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((host,port))

    # command_sent and session_enabled are workarounds for some i/o issues
    # e.g. the server response overwrites the user input prompt

    command_sent = threading.Event()  
    session_enabled = threading.Event()  
    command_sent.set()  
    session_enabled.set()  

    t = threading.Thread(target=listen, args=(server, command_sent, session_enabled, ))
    t.start()

    cli(server, command_sent, session_enabled)

if __name__ == '__main__':
    main()

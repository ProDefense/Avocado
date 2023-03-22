import socket
import threading
from pb import operatorpb_pb2

class Listener:
    def __init__(self, hostname, port):
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.connect((hostname,port))

    # convert message to protobuf and send to server
    def send(self, message):
        server_cmd = operatorpb_pb2.ServerCmd(cmd=message.encode("ascii"))
        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.ServerCmd, 
            data=server_cmd.SerializeToString()
        )
        self._server.send(message.SerializeToString())

    def listen(self):
        data = self._server.recv(1024)

        if data:
            message = operatorpb_pb2.Message()
            message.ParseFromString(data)
            return message

        else:
            self._server.close()
            return None

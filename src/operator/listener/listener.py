import socket
import threading
from pb import operatorpb_pb2

class Listener:
    def __init__(self, hostname, port, outputq, implantq, sessionq):
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.connect((hostname,port))

        threading.Thread(target=self._listen, args=(outputq, implantq, sessionq)).start()

    # convert message to protobuf and send to server
    def send(self, message):
        server_cmd = operatorpb_pb2.ServerCmd(cmd=message.encode("ascii"))
        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.ServerCmd, 
            data=server_cmd.SerializeToString()
        )
        self._server.send(message.SerializeToString())

    def _listen(self, outputq, implantq, sessionq):
        while True:
            data = self._server.recv(1024)

            if data:
                message = operatorpb_pb2.Message()
                message.ParseFromString(data)

                if message.message_type == operatorpb_pb2.Message.MessageType.SessionInfo:
                    session_info = operatorpb_pb2.SessionInfo()
                    session_info.ParseFromString(message.data)
                    implantq.put(session_info)

                elif message.message_type == operatorpb_pb2.Message.MessageType.SessionConnected:
                    session_connected = operatorpb_pb2.SessionConnected()
                    session_connected.ParseFromString(message.data)
                    sessionq.put(session_connected)

                elif message.message_type == operatorpb_pb2.Message.MessageType.ServerCmdOutput:
                    cmd_output = operatorpb_pb2.ServerCmdOutput()
                    cmd_output.ParseFromString(message.data)
                    outputq.put(cmd_output.cmdOutput)

            else:
                implantq.put(None)
                sessionq.put(None)
                outputq.put(None)
                self._server.close()
                break

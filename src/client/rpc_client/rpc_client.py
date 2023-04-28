import socket
import threading
from client.pb import operatorpb_pb2

class RPCClient:
    def __init__(self, hostname, port, outputq, implantq):
        self._implantq = implantq
        self._outputq = outputq
        
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.connect((hostname,port))

        threading.Thread(target=self._listen).start()

    def terminate(self):
        self._implantq.put(None)
        self._outputq.put(None)
        self._server.shutdown(socket.SHUT_RDWR)

    def sendSession(self, message, session_id):
        session_cmd = operatorpb_pb2.SessionCmd(cmd=message.encode("ascii"),id=session_id)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.SessionCmd, 
            data=session_cmd.SerializeToString()
        )

        self._server.send(message.SerializeToString())

    def _listen(self):
        while True:
            data = self._server.recv(1024)

            if data:
                message = operatorpb_pb2.Message()
                message.ParseFromString(data)

                if message.message_type == operatorpb_pb2.Message.MessageType.SessionInfo:
                    session_info = operatorpb_pb2.SessionInfo()
                    session_info.ParseFromString(message.data)
                    self._implantq.put(session_info)

                elif message.message_type == operatorpb_pb2.Message.MessageType.SessionCmdOutput:
                    output = operatorpb_pb2.SessionCmdOutput()
                    output.ParseFromString(message.data)
                    self._outputq.put((output.cmdOutput, output.id))

            else:
                break

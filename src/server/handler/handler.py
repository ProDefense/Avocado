# Handle registrations from new implants
import threading
from queue import Queue
from pb import operatorpb_pb2, implantpb_pb2

class Handler:
    def __init__(self, requestq: Queue, operators: dict):
        self._requestq = requestq
        self._operators = operators
        self._implants = list() # implant is a pair of a registration and id

    # Brodcast all current implant registrations to a new operator
    def brodcastImplants(self, operator):
        for implant in self._implants:
            self._brodcast_implant(implant, [operator])

    # Brodcast new implant registration to all operators
    def _brodcast_implant(self, implant, operators):
        registration, id = implant

        # converts the groups from implantpb groups to operatorpb groups
        user_groups = [operatorpb_pb2.SessionInfo.User(id=group.id, name=group.name) for group in registration.groups]

        # brodcast new session information to all operators
        session_info = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.SessionInfo,
            data=operatorpb_pb2.SessionInfo(
                    id=str(id),
                    addr=registration.addr,
                    os=registration.os,
                    pid=registration.pid,
                    user=operatorpb_pb2.SessionInfo.User(
                        id=registration.user.id,
                        name=registration.user.name
                    ),
                    groups = user_groups
                ).SerializeToString()
        ).SerializeToString()

        for c in operators:
            c.send(session_info)
        

    def start(self):
        t = threading.Thread(target=self._handle_implants, args=())
        t.start()

    # Handle incoming registrations
    def _handle_implants(self):
        # Get items from the queue
        while True:
            data, addr, id = self._requestq.get()
            self.readRegistration(data, addr, id)

    def readRegistration(self, data: bytes, addr, id):
        # Parse the incoming data
        message = implantpb_pb2.Message()
        message.ParseFromString(data)
        if message.message_type == implantpb_pb2.Message.MessageType.Registration:
            registration = implantpb_pb2.Registration()
            registration.ParseFromString(message.data)
            if len(registration.addr) < 1:
                registration.addr = str(addr)

            # TODO: Add the `registration` to the database

            # TODO: Log this part here instead of printing to stdout
            display = f"""
            Accepted new connection:
                addr: {registration.addr},
                os: {registration.os},
                pid: {registration.pid},
                user: {registration.user.name},
                groups: {registration.groups}"""
            print(display)

            new_implant = (registration,id)
            self._implants.append(new_implant)
            self._brodcast_implant(new_implant, self._operators)

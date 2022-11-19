# Handle registrations from new implants
import threading
from queue import Queue
from pb import implantpb_pb2


class Handler:
    def __init__(self, requestq: Queue):
        self._requestq = requestq

    def start(self):
        t = threading.Thread(target=self._handle_registrations, args=())
        t.start()

    # Handle incoming registrations
    def _handle_registrations(self):
        # Get items from the queue
        while True:
            data, addr = self._requestq.get()
            self.readRegistration(data, addr)

    def readRegistration(self, data: bytes, addr):
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

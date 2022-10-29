# Handle registrations from new implants
import threading
from queue import Queue
from pb import implantpb_pb2


class Handler:
    def __init__(self, requestq: Queue):
        self.__requestq = requestq

    def start(self):
        t = threading.Thread(target=self.__handle, args=())
        t.start()

    # Handle incoming registrations
    def __handle(self):
        # Get items from the queue
        while True:
            data = self.__requestq.get()

            implant = implantpb_pb2.Registration()
            implant.ParseFromString(data)

            # TODO: Add the `implant` to the database

            # TODO: Log this part here instead of printing to stdout
            display = f"""
            Accepted new connection:
                ip: {implant.ip},
                os: {implant.os},
                pid: {implant.pid},
                user: {implant.user.name},
                groups: {implant.groups}"""
            print(display)

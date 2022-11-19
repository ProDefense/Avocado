# Handle registrations from new implants
import threading
from queue import Queue
from pb import implantpb_pb2
from sqlalchemy import create_engine, engine, insert

class Handler:
    def __init__(self, requestq: Queue):
        self.__requestq = requestq

    def start(self):
        t = threading.Thread(target=self.__handle, args=())
        t.start()

        # Connect to SQLAlchemy engine
        engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/test_db')

    # Handle incoming registrations
    def __handle(self):
        # Get items from the queue
        while True:
            data, addr = self.__requestq.get()

            implant = implantpb_pb2.Registration()
            implant.ParseFromString(data)
            if len(implant.addr) < 1:
                implant.addr = str(addr)

            # TODO: Test adding implant to the database. May need to import database classes if this method does not work
            stmt = insert(Implants).values(OS = implant.os, Arch = "?", IPv4 = "?", Hostname = "?", Username = implant.user.name, PID = implant.pid)
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()

            
i
            # TODO: Log this part here instead of printing to stdout
            display = f"""
            Accepted new connection:
                addr: {implant.addr},
                os: {implant.os},
                pid: {implant.pid},
                user: {implant.user.name},
                groups: {implant.groups}"""
            print(display)

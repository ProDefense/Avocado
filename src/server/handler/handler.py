# Handle registrations from new implants
import threading
import sqlite3
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
            try:
                #test_db may need to be changed
                sqliteConnection = sqlite3.connect('test_db.db')
                cursor = sqliteConnection.cursor()
                print("Successfully Connected to SQLite")

                insert = """INSERT INTO implantRecords 
                            (Implant_UUID, OS, Arch, IPv4, Hostname, Username, PID, ImplantUpTime) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
            except sqlite3.Error as error:
                print("Failed to insert data into sqlite table", error)
            finally:
                if sqliteConnection:
                    sqliteConnection.close()
                    print("The SQLite connection is closed")
            # TODO: Log this part here instead of printing to stdout
            display = f"""
            Accepted new connection:
                ip: {implant.ip},
                os: {implant.os},
                pid: {implant.pid},
                user: {implant.user.name},
                groups: {implant.groups}"""
            print(display)

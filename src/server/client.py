#!/usr/bin/env python3
import socket

def main():
    host = "127.0.0.1"
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))
    msg = ""
    while True:
        msg = input("$")
        s.send(msg.encode('ascii'))
        data = s.recv(1024)
        if msg.lower() == "exit":
            print("[+]Connection Terminated")
            break
        elif (not data):
            print("no data")
        else:
            print(str(data.decode('ascii')))

    s.close()




if __name__ == '__main__':
    main()

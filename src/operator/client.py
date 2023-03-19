#!/usr/bin/env python3
import socket

def shell_cli(s):
    userin = ""
    while True:
        userin = input("[session] > ") 
        
        s.send(userin.encode('ascii'))

        data = s.recv(1024)
        print(str(data.decode('ascii')))

        if (userin=="exit"):
            break
    
def main():
    host = "127.0.0.1"
    port = 12345

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port))

    while True:
        msg = input("[Avocado] > ")

        if msg.lower() == "exit":
            print("[+]Connection Terminated")
            break

        elif not msg or len(msg.split())<1:
            continue

        s.send(msg.encode('ascii'))
        data = s.recv(1024)

        if (msg.split()[0]=="use") and (data.decode('ascii').split()[0]=="Using"):
            shell_cli(s)
            continue

        elif (not data):
            print("no data")

        else:
            print(str(data.decode('ascii')))

    s.close()


if __name__ == '__main__':
    main()

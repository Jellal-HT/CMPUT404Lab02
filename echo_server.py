#!/usr/bin/env python3
import socket
import time
import os
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def multiprocess(conn, addr):
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(1)
    conn.sendall(full_data) 
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        # set socket option, reuseaddress to true (1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            # instance of socket, IP of client
            conn, addr = s.accept()
            print("Connected by", addr)

            p = Process(target=multiprocess(conn, addr))      
            p.daemon = True
            p.start()
            conn.close()

if __name__ == "__main__":
    main()

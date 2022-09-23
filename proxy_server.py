#!/usr/bin/env python3
import socket, sys
import time
import os
from multiprocessing import Process


def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

def get_remote_ip(host):
    print(f'Getting IP for {host}...')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def send_data(serversocket, payload):
    print("Sending payload...")    
    try:
        # data from proxy client already encoded dont need to encode
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def send_to_int(payload):
    try:
        PS_HOST = 'www.google.com'
        PS_PORT = 80
        buffer_size = 4096

        s = create_tcp_socket()
        remote_ip = get_remote_ip(PS_HOST)
        s.connect((remote_ip , PS_PORT))
        
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)

        return_data = s.recv(buffer_size)
        return return_data

    except Exception as e:
        print(e)

    finally:
        s.close()

HOST = ""            
PORT = 8001          
BUFFER_SIZE = 4096   


def multiprocess(pc_conn, addr):
    full_data = pc_conn.recv(BUFFER_SIZE)
    if full_data: print('Data received from proxy client')
        
    ps_return_data = send_to_int(full_data)
    if ps_return_data: print('Data received from remote connection')

    pc_conn.sendall(ps_return_data)
    pc_conn.close()

full_data = b''

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(2)
        
        while True:
            pc_conn, addr = s.accept()
            
            p = Process(target=multiprocess, args=(pc_conn, addr))
            p.daemon = True
            p.start()
            pc_conn.close()            

if __name__ == "__main__":
    main()
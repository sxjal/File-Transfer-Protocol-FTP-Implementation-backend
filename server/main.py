import socket
import sys
import time
import os
import struct
import json
import hashlib
from handle_user import create_user, authenticate

print("Welcome to the FTP server.\n\nTo get started, connect a client.")

TCP_IP = "127.0.0.1"  
TCP_PORT = 1456  
BUFFER_SIZE = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print ("\nConnected to by address: ",addr)


def upld():
    print("inside upld")
    conn.send("911".encode())

    print("sent 911")
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size)
    conn.send("1".encode())
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    output_file = open(file_name, "wb")
    bytes_recieved = 0
    print ("\nRecieving...")
    while bytes_recieved < file_size:
        l = conn.recv(BUFFER_SIZE)
        output_file.write(l)
        bytes_recieved += BUFFER_SIZE
    output_file.close()
    print("\nRecieved file:",file_name)
    # Send upload performance details
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    return
 
 
data = conn.recv(BUFFER_SIZE).decode()

opcode = data.split(" ")[0]
username = data.split(" ")[1].split(":")[0]
password = data.split(" ")[1].split(":")[1]

print("Username:", username)
print("Password:", password)

authcode = authenticate(username,password)

while authcode:
     
    print ("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print ("\n Operation: ",data)
    if data == "UPLD":
        upld()
     
    data = None

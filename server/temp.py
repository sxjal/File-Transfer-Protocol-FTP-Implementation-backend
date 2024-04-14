# from handle_user import authenticate, create_user



# user = "sxjal"
# passw = "12345"


# print("create user: ",create_user(username=user,password=passw))
# print("login user: ",authenticate(username=user,password=passw))
# passw = "1235"
# print("create user: ",authenticate(username=user,password=passw))


import socket
import sys
import time
import os
import struct
import json
import hashlib
from handle_user import create_user, authenticate
from utils import TCP_IP,TCP_PORT,BUFFER_SIZE

print("Welcome to the FTP server.\n\nTo get started, connect a client.")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print ("\nConnected to by address: ",addr)


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

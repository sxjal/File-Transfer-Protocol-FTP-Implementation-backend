import socket
import sys
import time
import os
import struct
import json
import hashlib

print("Welcome to the FTP server.\n\nTo get started, connect a client.")

# Load credentials from JSON file
with open("credentials.json", "r") as file:
    credentials = json.load(file)

# Initialise socket stuff
TCP_IP = "127.0.0.1"  
TCP_PORT = 1456  
BUFFER_SIZE = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print ("\nConnected to by address: ",addr)

def authenticate(username, password):
    # Simple authentication function
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in credentials and credentials[username] == password:
        return True
    else:
        return False

def upld():
    print("inside upld")
    conn.send("911".encode())

    print("sent 911")
    # Recieve file name length, then file name
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size)
    # Send message to let client know server is ready for document content
    conn.send("1".encode())
    # Recieve file size
    file_size = struct.unpack("i", conn.recv(4))[0]
    # Initialise and enter loop to recive file content
    start_time = time.time()
    output_file = open(file_name, "wb")
    # This keeps track of how many bytes we have recieved, so we know when to stop the loop
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
    # Check the command and respond correctly
    if data == "UPLD":
        upld()
     
    # Reset the data to loop
    data = None

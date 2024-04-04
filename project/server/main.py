import socket
import sys
import time
import os
import struct

print("Welcome to the FTP server. To get started, connect a client.")


TCP_IP = "127.0.0.1"  
TCP_PORT = 1456  
BUFFER_SIZE = 1024  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

s.listen(1)
try:
    conn, addr = s.accept()
    print ("\nConnected to by address: ",addr)

except Exception as e:
    print("inside exception")
    print(e)


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
 
while True:
   
    print ("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print ("\nRecieved instruction:",data)
    # Check the command and respond correctly
    if data == "UPLD":
        upld()
    
    data = None

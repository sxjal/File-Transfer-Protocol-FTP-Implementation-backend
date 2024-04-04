import socket
import sys
import os
import struct


TCP_IP = "127.0.0.1"  
TCP_PORT = 1456  
BUFFER_SIZE = 1024   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Welcome to server, sending server request...")

#making connection request

try:
    s.connect((TCP_IP, TCP_PORT))
    print("Connection successful")
except Exception as e:
    print("Connection unsuccessful. Make sure the server is online.")
    print(e)


def upld(file_name):
    # Upload a file
    print("\nUploading file: {}...".format(file_name))
    try:
        print("inside try")
        
        if not os.path.exists(file_name):
            print("File doesn't exist. Make sure the file path is correct.")
            return
        # Make upload request
        print("making upload request")
        s.send("UPLD".encode())

        print("upld sent")
    except Exception as e:
        print("Couldn't make server request. Make sure a connection has been established.")
        print(e)
        return
    try:
        # Wait for server acknowledgement then send file details
        # Wait for server ok
        s.recv(BUFFER_SIZE).decode() 
        # Send file name size and file name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        # Wait for server ok then send file size
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except Exception as e:
        print("Error sending file details")
        print(e)
        return
    try:
        # Send the file in chunks defined by BUFFER_SIZE
        # Doing it this way allows for unlimited potential file sizes to be sent
        with open(file_name, "rb") as content:
            l = content.read(BUFFER_SIZE)
            print("\nSending...")
            while l:
                s.send(l)
                l = content.read(BUFFER_SIZE)
        # Get upload performance details
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except Exception as e:
        print("Error sending file")
        print(e)
        return

while True:
    
    print("1. UPLD: Upload File")
    prompt = input("\nEnter a command: ")
    
    if prompt[:4].upper() == "UPLD":
        upld(prompt[5:])
   
    else:
        print("Command not recognized; please try again")

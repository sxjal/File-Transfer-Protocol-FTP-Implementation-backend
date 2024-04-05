import socket
import sys
import os
import struct

# Initialise socket stuff
TCP_IP = "127.0.0.1"  # Only a local server
TCP_PORT = 1456  # Just a random choice
BUFFER_SIZE = 1024  # Standard choice
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    # Connect to the server
    print("Sending server request...")
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection successful")
    except Exception as e:
        print("Connection unsuccessful. Make sure the server is online.")
        print(e)

def upld():
    # Upload a file
    file_name = input("enter file name")
    print("\nUploading file:",file_name)
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

print("\nWelcome to the FTP client.")

conn()

print("Connected succesfully")

username = input('Enter username: ')
password = input('Enter password: ')

s.send("AUTH {username}:{password}".encode())


while True:
    print("Call one of the following functions:\n1. UPLD file_path : Upload file\nLIST           : List files\nDWLD file_path : Download file\nDELF file_path : Delete file\nQUIT           : Exit")
    # Listen for a command
    opcode = input("\nEnter a command: ")
    if opcode.upper() == "UPLD":
        upld()

    else:
        print("Command not recognized; please try again")

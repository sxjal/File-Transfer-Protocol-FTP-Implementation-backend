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

def list_files():
    # List the files available on the file server
    print("Requesting files...\n")
    try:
        # Send list request
        s.send("LIST".encode())
    except Exception as e:
        print("Couldn't make server request. Make sure a connection has been established.")
        print(e)
        return
    try:
        # First get the number of files in the directory
        number_of_files = struct.unpack("i", s.recv(4))[0]
        # Then enter into a loop to receive details of each, one by one
        for i in range(int(number_of_files)):
            # Get the file name size first to slightly lessen amount transferred over socket
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            # Also get the file size for each item in the server
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            # Make sure that the client and server are synchronized
            s.send("1".encode())
        # Get total size of directory
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("Total directory size: {}b".format(total_directory_size))
    except Exception as e:
        print("Couldn't retrieve listing")
        print(e)
        return
    try:
        # Final check
        s.send("1".encode())
        return
    except Exception as e:
        print("Couldn't get final server confirmation")
        print(e)
        return

def dwld(file_name):
    # Download given file
    print("Downloading file: {}".format(file_name))
    try:
        # Send server request
        s.send("DWLD".encode())
    except Exception as e:
        print("Couldn't make server request. Make sure a connection has been established.")
        print(e)
        return
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            # If file size is -1, the file does not exist
            print("File does not exist. Make sure the name was entered correctly")
            return
    except Exception as e:
        print("Error checking file")
        print(e)
        return
    try:
        # Send ok to receive file content
        s.send("1".encode())
        # Enter loop to receive file
        output_file = open(file_name, "wb")
        bytes_received = 0
        print("\nDownloading...")
        while bytes_received < file_size:
            # Again, file broken into chunks defined by the BUFFER_SIZE variable
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_received += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        # Tell the server that the client is ready to receive the download performance details
        s.send("1".encode())
        # Get performance details
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except Exception as e:
        print("Error downloading file")
        print(e)
        return

def delf(file_name):
    # Delete specified file from file server
    print("Deleting file: {}...".format(file_name))
    try:
        # Send request, then wait for go-ahead
        s.send("DELF".encode())
        s.recv(BUFFER_SIZE)
    except Exception as e:
        print("Couldn't connect to server. Make sure a connection has been established.")
        print(e)
        return
    try:
        # Send file name length, then file name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
    except Exception as e:
        print("Couldn't send file details")
        print(e)
        return
    try:
        # Get confirmation that file does/doesn't exist
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print("The file does not exist on server")
            return
    except Exception as e:
        print("Couldn't determine file existence")
        print(e)
        return
    try:
        # Confirm user wants to delete file
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
        # Make sure input is valid
        while confirm_delete != "Y" and confirm_delete != "N" and confirm_delete != "YES" and confirm_delete != "NO":
            # If user input is invalid
            print("Command not recognised, try again")
            confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    except Exception as e:
        print("Couldn't confirm deletion status")
        print(e)
        return
    try:
        # Send confirmation
        if confirm_delete == "Y" or confirm_delete == "YES":
            # User wants to delete file
            s.send("Y".encode())
            # Wait for confirmation file has been deleted
            delete_status = struct.unpack("i", s.recv(4))[0]
            if delete_status == 1:
                print("File successfully deleted")
                return
            else:
                # Client will probably send -1 to get here, but an else is used as more of a catch-all
                print("File failed to delete")
                return
        else:
            s.send("N".encode())
            print("Delete abandoned by user!")
            return
    except Exception as e:
        print("Couldn't delete file")
        print(e)
        return

def quit_connection():
    s.send("QUIT".encode())
    # Wait for server go-ahead
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return

print("\n\nWelcome to the FTP client.\n\nCall one of the following functions:\nCONN           : Connect to server\nUPLD file_path : Upload file\nLIST           : List files\nDWLD file_path : Download file\nDELF file_path : Delete file\nQUIT           : Exit")

while True:
    # Listen for a command
    prompt = input("\nEnter a command: ")
    if prompt[:4].upper() == "CONN":
        conn()
    elif prompt[:4].upper() == "UPLD":
        upld(prompt[5:])
    elif prompt[:4].upper() == "LIST":
        list_files()
    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:])
    elif prompt[:4].upper() == "DELF":
        delf(prompt[5:])
    elif prompt[:4].upper() == "QUIT":
        quit_connection()
        break
    else:
        print("Command not recognized; please try again")

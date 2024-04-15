import struct
import socket

server_address = '127.0.0.1'
server_port = 12356

ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ftp_socket.connect((server_address, server_port))

print('connected')

def files_on_server(conn):
   
    print("Requesting files...\n")

    try:
        # First get the number of files in the directory
        number_of_files = struct.unpack("i", conn.recv(4))[0]
        print(f"number_of_files {number_of_files}")
        # Then enter into a loop to receive details of each, one by one
        for i in range(int(number_of_files)):
            # Get the file name size first to slightly lessen amount transferred over socket
            file_name_size = struct.unpack("i", conn.recv(4))[0]
            conn.send("351".encode())
            print(f"file_name_size {file_name_size}")
            file_name = conn.recv(file_name_size).decode()
            conn.send("352".encode())
            print(f"file_name {file_name}")
            # Also get the file size for each item in the server
            file_size = struct.unpack("i", conn.recv(4))[0]
            conn.send("353".encode())
            print(f"file_size {file_size}")
            print("\t{} - {}b".format(file_name, file_size))
            # Make sure that the client and server are synchronized
            conn.send("200".encode())
        # Get total size of directory
        total_directory_size = struct.unpack("i", conn.recv(4))[0]  
        conn.send("355".encode())
        print("Total directory size: {}b".format(total_directory_size))
    except Exception as e:
        print("Couldn't retrieve listing")
        print(e)
        return
    try:
        # Final check
        conn.send("200".encode())
        return
    except Exception as e:
        print("Couldn't get final server confirmation")
        print(e)
        return

files_on_server(conn=ftp_socket) 
input("halt")
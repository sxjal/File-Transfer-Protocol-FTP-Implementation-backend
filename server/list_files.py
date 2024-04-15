import os,sys
from utils import directory,BUFFER_SIZE
import struct

def list_files_in_directory():
    files_dict = []
    print (directory)
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            files_dict.append(os.path.join(directory, filename))
    return files_dict


def files_on_server(conn):
    print ("Listing files...")
    listing = list_files_in_directory()
    print("list of files", listing)
    # Send over the number of files, so the client knows what to expect (and avoid some errors)
    total_directory_size = len(listing)
    conn.send(struct.pack("i", total_directory_size)) #number of files

    # Send over the file names and sizes whilst totaling the directory size
    for i in listing:
        # File name size
        conn.send(struct.pack("i", sys.getsizeof(i)))
        print("file name size sent")
        # File name
        conn.recv(BUFFER_SIZE).decode() #351
        conn.send(i.encode()) 
        conn.recv(BUFFER_SIZE).decode() #352
        print("file name sent")
        # File content size
        conn.send(struct.pack("i", os.path.getsize(i)))
        conn.recv(BUFFER_SIZE).decode() #353
        print("file content size sent")
        total_directory_size += os.path.getsize(i)
        # Make sure that the client and server are syncronised
        if(conn.recv(BUFFER_SIZE).decode() == "200"):
            print("sync checked")
        else: 
            break
    # Sum of file sizes in directory
    conn.send(struct.pack("i", total_directory_size))
    conn.recv(BUFFER_SIZE).decode() #355
    print("total directory size sent")
    #Final check
    if(conn.recv(BUFFER_SIZE).decode() == "200"):

        print ("Successfully sent file listing")
    return "200"


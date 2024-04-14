import socket
import threading
from handle_client import handle_client
from utils import TCP_IP,TCP_PORT


if __name__== '__main__':
    print("welcome to Sajal's Server")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)
    except Exception as e:
        print(e)

    print("Accepting connections...")
    
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
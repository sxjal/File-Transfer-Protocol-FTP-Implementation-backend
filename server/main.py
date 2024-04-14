import socket
import threading
from handle_client import handle_client
from utils import TCP_IP,TCP_PORT,connections


if __name__== '__main__':

    print("Welcome to Sajal's Server")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        
        print(f"Listening to connections at {TCP_IP}:{TCP_PORT}")

        s.listen(connections)
    
    except Exception as e:
        print(e)
    
    while True:
        conn, addr = s.accept()
        
        print('Connected with ', addr)

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()
import socket
import json
import threading

# Load user credentials from JSON file
def load_credentials():
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Authenticate user based on provided credentials
def authenticate(username, password):
    credentials = load_credentials()
    return credentials.get(username) == password

# Function to handle each client connection
def handle_client(client_socket):
    client_socket.send(b"220 Welcome to the FTP server\r\n")

    while True:
        request = client_socket.recv(1024).decode().strip()

        if request.startswith("USER"):
            username = request.split(" ")[1]
            client_socket.send(b"331 Enter password\r\n")
        elif request.startswith("PASS"):
            password = request.split(" ")[1]
            if authenticate(username, password):
                client_socket.send(b"230 User logged in\r\n")
            else:
                client_socket.send(b"530 Login incorrect\r\n")
        elif request.startswith("QUIT"):
            client_socket.send(b"221 Goodbye\r\n")
            break
        else:
            client_socket.send(b"500 Syntax error\r\n")

    client_socket.close()

# Main function to handle server operations
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 21))
    server_socket.listen(5)
    print("FTP server listening on port 21...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Connection from:", addr)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

main()

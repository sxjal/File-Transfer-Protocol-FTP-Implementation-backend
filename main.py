# # from pyftpdlib.authorizers import DummyAuthorizer
# # from pyftpdlib.handlers import FTPHandler
# # from pyftpdlib.servers import FTPServer

# # def main():
# #     # Instantiate a dummy authorizer for managing 'virtual' users
# #     authorizer = DummyAuthorizer()

# #     # Define a new user having full read/write access and a specific home directory
# #     authorizer.add_user("sxjal", "12345", "/", perm="elradfmw")

# #     # Instantiate an FTP handler object
# #     handler = FTPHandler
# #     handler.authorizer = authorizer

# #     # Specify the port and address to run the server
# #     server = FTPServer(("127.0.0.1", 12356), handler)

# #     print("server")
# #     # Start the FTP server
# #     server.serve_forever()

# #     print("server started")

# # if __name__ == "__main__":
# #     main()

# import socket

# HOST = '127.0.0.1'  # Server's IP address
# PORT = 12345        # Port to listen on

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     print(f"Server listening on {HOST}:{PORT}")
#     conn, addr = s.accept()
#     print("connect with ", addr)
#     with conn:
#         while True:
#             data = conn.recv(1024)
#             print(f"Received: {data.decode()}")

#             if(data.upper() == 'exit'):
#                 break

#             ans = input('enter response')
#             conn.sendall(ans.encode())


import socket

HOST = '127.0.0.1'  # Server's IP address
PORT = 12356        # Port to listen on

def receive_file(conn, filename):
    with open(filename, 'wb') as f:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
        print(f"File '{filename}' received successfully")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Receive filename from client
        filename = conn.recv(1024).decode()
        print(f"Receiving file '{filename}'")

        filename
        # Receive file content from client
        receive_file(conn, filename)

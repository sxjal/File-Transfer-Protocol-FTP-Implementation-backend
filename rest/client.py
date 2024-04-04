import socket

def main():
    server_address = '127.0.0.1'
    server_port = 21

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((server_address, server_port))
    print(ftp_socket.recv(1024).decode())

    while True:
        username = input("Username: ")
        ftp_socket.sendall(("USER " + username + "\r\n").encode())
        response = ftp_socket.recv(1024).decode()
        code = response.split(" ")[0]
        text = response.split(" ")[1]

        print(code)
        print(text)
        
        if response.startswith("331"):
            password = input("Password: ")
            ftp_socket.sendall(("PASS " + password + "\r\n").encode())
            response = ftp_socket.recv(1024).decode()
            print(response)

            if response.startswith("230"):
                # Authentication successful
                break

    ftp_socket.close()

if __name__ == "__main__":
    main()

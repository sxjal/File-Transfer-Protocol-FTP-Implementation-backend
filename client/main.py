import socket

def main():
    server_address = '127.0.0.1'
    server_port = 12356

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((server_address, server_port))

    print('connected')
    

    if(ftp_socket.recv(1024).decode() == "201"): #receive 201
        while True:
            opcode = input("100 or 103: ")  #100 - create, 103 - login
            username = input("Username: ")
            password = input("password: ")
            if(opcode == "100"):
                access_control = input("access: ") #900 - admin, 901- read only, 902- write only

            #100<SXJAL>12345:900
            message = opcode + "<" + username + ":" + password + ">" + access_control
            print(f"sending to server{message}")
            ftp_socket.sendall(message.encode())

            response = ftp_socket.recv(1024).decode()
            print(f"response: {response}")

            code = ["101","104","202"]

            if response in code:
                if response == "101":
                    print("User already exists, Please try again")
                elif response == "104":
                    print("Wrong Credentials, Please try again")
                elif response == "202":
                    print("Invalid OPCODE sent to server, kindly check the opcode again")
                continue
            
            else:
                if response == "102":
                    print(f"User created successfully! Welcome {username}!")
                elif response == "105":
                    print(f"Logged in. Welcome {username}!")
                break
        
        while(message != "204"):
            response = ftp_socket.recv(1024).decode('UTF-8')
            print(response)
            message = username + " > "
            message = input(message)



        
    # ftp_socket.close()

if __name__ == "__main__":
    main()

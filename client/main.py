import socket
from listfiles import files_on_server,local_files

def main(socket):
   

    if(socket.recv(1024).decode() == "201"): #receive 201 connection successfull, send credentials.
        while True:
            while(True):
                opcode = input("Login | SIGNUP: ")  #100 - create, 103 - login
                if opcode.upper() == "LOGIN": 
                    opcode = "103"
                    break
                elif opcode.upper() == "SIGNUP":
                    opcode = "100"
                    break
                else:
                    print("Invalid opcode, please try again.")
                    continue

            username = input("Username: ")
            password = input("password: ")
             
            if(opcode == "100"):
                try:
                    while(True):
                        access_control = input("Available Options\n ADMIN \n RO \n WO \nSet access Control: ") #900- admin, 901- read only, 902- write only
                        if access_control.upper() == "ADMIN": 
                            access_control = "900"
                            break
                        elif access_control.upper() == "RO":
                            access_control = "901"
                            break
                        elif access_control.upper() == "WO":
                            access_control = "902"
                            break
                        else:
                            print("Invalid code, please try again.")
                            continue

                except Exception as e:
                    print(e)
                    access_control = 0
                message = opcode + "<" + username + ":" + password + ">" + access_control
            else:
                message = opcode + "<" + username + ":" + password 
            # message = opcode + "<" + username + ":" + password + ">" + access_control
            print(f"sending to server {message}")
            
            socket.send(message.encode()) #sending credentials in an enoded message
            response = socket.recv(1024).decode('UTF-8') #receive response:105 for login
            
            print(f"useropcode from server: {response} \\n")
            print("\n")
            print(response)
            code = ["101","104","202"]
            print(response in code)
            if response in code:
                print("into if")
                if response == "101":
                    print("User already exists, Please try again")
                elif response == "104":
                    print("Wrong Credentials, Please try again")
                elif response == "202":
                    print("Invalid OPCODE sent to server, kindly check the opcode again")
                continue
            else:
                print("into else")
                if response == "102":
                    print(f"User created successfully! Welcome {username}!")
                elif response == "105":
                    print(f"Logged in. Welcome {username}!")
                break
        print("set msg = 200")
        message = "200"
        while(True):
            print("inside while")
            sync = socket.recv(1024).decode()  #recv 203
            print("recv sync")
            if(sync == "203"):
                print(sync)
                continue
            else: 
                print("lost connection with server")
                # break
            print("recv resp")
            response = socket.recv(1024).decode() #choices
            print(response)
            cmd = username + "> "
            message = input(cmd)
            print("sent msg")
            socket.sendall(message.encode()) 
            opcode = message.split(" ")[0]

            if(opcode == "301"):
            #List Files on server
                opcode = files_on_server(conn=socket)
            elif(opcode == "302"):
                opcode = local_files()
                print()
            elif(opcode == "303"):
                # Upload File : '303 filename' 
                print()
            elif(opcode == "304"): 
                #Download file from Server : '304 filename' 
                print()
            elif(opcode == "305"):
                # Delete file on server '305 filename'
                print()
            elif(opcode == "306"):
                #  - Rename file on server : '306 oldname>newname'",
                print()
            else:
                message = "307:Invalid Opcode"
            




        
    # ftp_socket.close()

if __name__ == "__main__":
    server_address = '127.0.0.1'
    server_port = 12456

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((server_address, server_port))

    print('connected')
    
    main(socket = ftp_socket)

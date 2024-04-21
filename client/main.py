import socket
from listfiles import files_on_server,local_files

def main(socket):
   

    if(socket.recv(1024).decode() == "201"): #receive 201 connection successfull, send credentials.
        while True:
            while(True):
                opcode = input("Login | SIGNUP ")  #100 - create, 103 - login
                if opcode == "LOGIN": 
                    opcode = 103
                    break
                elif opcode == "SIGNUP":
                    opcode = 100
                    break
                else:
                    print("Invalid opcode, please try again.")
                    continue

            username = input("Username: ")
            password = input("password: ")
             
            if(opcode == 100):
                try:
                    while(True):
                        access_control = input("Available Options\n ADMIN \n RO \n WO \nSet access Control:") #900- admin, 901- read only, 902- write only
                        if access_control == "ADMIN": 
                            opcode = 900
                            break
                        elif access_control == "RO":
                            opcode = 901
                            break
                        elif access_control == "WO":
                            opcode = 902
                        else:
                            print("Invalid code, please try again.")
                            continue

                except Exception as e:
                    print(e)
                    access_control = " "
                message = opcode + "<" + username + ":" + password + ">" + access_control
            else:
                message = opcode + "<" + username + ":" + password 
            # message = opcode + "<" + username + ":" + password + ">" + access_control
            print(f"sending to server {message}")
            
            socket.send(message.encode()) #sending credentials in an enoded message
            response = socket.recv(1024).decode() #receive response
            
            print(f"response: {response} \n")

            code = ["101","104","202"]

            if response in code:
                if response == 101:
                    print("User already exists, Please try again")
                elif response == "104":
                    print("Wrong Credentials, Please try again")
                elif response == "202":
                    print("Invalid OPCODE sent to server, kindly check the opcode again")
                continue
            
            else:
                if response == 102:
                    print(f"User created successfully! Welcome {username}!")
                elif response == 105:
                    print(f"Logged in. Welcome {username}!")
                break

        message = "200"
        while(message != "204"):
            sync = socket.recv().decode()
            if(sync == "203"):
                continue
            else: 
                print("lost connection with server")
                # break

            response = socket.recv().decode() #choices
            print(response)
            cmd = username + "> "
            message = input(cmd)
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
    server_port = 12356

    ftp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ftp_socket.connect((server_address, server_port))

    print('connected')
    
    main(socket = ftp_socket)

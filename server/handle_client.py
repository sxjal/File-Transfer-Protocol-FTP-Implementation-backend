from utils import BUFFER_SIZE, choice
from handle_user import authenticate, create_user, get_access_controll

def handle_client(conn, addr):

    conn.send("201".encode())  #connection succesfull send user creds
    
    code = ["101","104","202"]
    opcode = "101"

    while(opcode in code):
        
        data = conn.recv(BUFFER_SIZE).decode() #receive creds
        
        opcode = data.split("<")[0]
        if(opcode == "100"): #create_user
            try:
                id = data.split("<")[1].split(":")[0]
                psw = data.split("<")[1].split(":")[1].split(">")[0]
                accesscontroll = data.split("<")[1].split(":")[1].split(">")[1]
                print(f"Received message from client {opcode}<{id}:{psw}>{accesscontroll}")
            except Exception as e:
                e
                id = " "
                psw = ""
                accesscontroll = ""
            opcode = create_user(username=id,password=psw,access_control=accesscontroll)
        elif(opcode == "103"): #login
            id = data.split("<")[1].split(":")[0]
            psw = data.split("<")[1].split(":")[1]
            opcode = authenticate(username=id,password=psw)
            if(opcode == "105"):
                accesscontroll = get_access_controll(username=id)
            else: 
                accesscontroll = "000"
            print(f"Received message from client {opcode}<{id}:{psw}>{accesscontroll}")
        else:
            opcode = "202" #error        
        print(f"reponse form function: {opcode}")
        conn.send(opcode.encode('UTF-8')) #send response code to the client: 105

    opcode = "200"
    while(opcode != "204"): 
        print("inside while")
        msg = "203"
        conn.send(msg.encode())   #203
        print(f"sent {msg}")
        conn.send(choice[accesscontroll].encode()) #sending choice
        print("sent")
        data = conn.recv(BUFFER_SIZE).decode()   #recieve choice 
        opcode = data.split(" ")[0]

        if(opcode == "301"):
            #List Files on server
            print()
        elif(opcode == "302"):
            # List local files 
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
        
        

     

    

from utils import BUFFER_SIZE, choice
from handle_user import authenticate, create_user

def handle_client(conn, addr):

    conn.send("201".encode())  #connection succesfull send user creds
    
    code = ["101","104","202"]
    opcode = "101"

    while(opcode in code):
        
        data = conn.recv(BUFFER_SIZE).decode() #receive creds
        #EXAMPLES
        #100 SXJAL:12345
        #103 SXJAL:12345

        opcode = data.split("<")[0]
        id = data.split("<")[1].split(":")[0]
        psw = data.split("<")[1].split(":")[1].split(">")[0]
        accesscontroll = data.split("<")[1].split(":")[1].split(">")[1]

        print(f"{opcode}<{id}:{psw}>{accesscontroll}")
        if(opcode == "100"): #create_user
            opcode = create_user(username=id,password=psw,access_control=accesscontroll)
        elif(opcode == "103"):
            opcode,accesscontroll = authenticate(username=id,password=psw)
            
        else:
            opcode = "202"
        
        print(f"reponse formn function: {opcode}")
        conn.send(opcode.encode()) #send response code to the server
    
    opcode = "200"
    while(opcode != "204"): 
        conn.send(choice[accesscontroll].encode('UTF-8'))
        data = conn.recv(BUFFER_SIZE).decode()
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
        
        

     

    

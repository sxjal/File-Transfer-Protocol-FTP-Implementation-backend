from utils import BUFFER_SIZE
from handle_user import authenticate, create_user

def handle_client(conn, addr):
    print('Incoming Connection from ',addr)
    print('Connected with ', addr)

    conn.send("201".encode())  #connection succesfull send user creds
    data = conn.recv(BUFFER_SIZE).decode() #receive creds

    #EXAMPLES
    #100 SXJAL:12345
    #103 SXJAL:12345

    opcode = data.split(" ")[0]
    id = data.split(" ")[1].split(":")[0]
    psw = data.split(" ")[1].split(":")[1]

    if(opcode == '100'): #create_user
        res = create_user(username=id,password=psw)
        
    elif(opcode == '103'):
        res = authenticate(username=id,password=psw)
    else:
        conn.send("202".encode()) #wrong opcode closing connection
    
    print(res)
    return res

    

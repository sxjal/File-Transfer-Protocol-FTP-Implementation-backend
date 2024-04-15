from utils import BUFFER_SIZE, choice
from handle_user import authenticate, create_user
from list_files import files_on_server

def handle_client(conn, addr):

    # accesscontroll = 900
    opcode = "200"
    while(opcode != "204"): 
        # conn.send(choice[accesscontroll].encode('UTF-8'))
        response = files_on_server(conn=conn)
        print("response from list func: ",response)
        

     

    

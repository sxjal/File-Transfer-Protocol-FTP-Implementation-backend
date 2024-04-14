opcode = input("100 or 103: ")  #100 - create, 103 - login
            username = input("Username: ")
            password = input("password: ")
            access_control = input("access: ") #900 - admin, 901- read only, 902- write only
            #100 SXJAL:12345
            message = opcode + " " + username + ":" + password + ":" + access_control
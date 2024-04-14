opcode = input("100 or 103: ")  #100 - create, 103 - login
username = input("Username: ")
password = input("password: ")
access_control = input("access: ") #900 - admin, 901- read only, 902- write only

data = opcode + "<" + username + ":" + password + ">" + access_control

# 100 sajal>sajal:900
code = data.split("<")[0]
id = data.split("<")[1].split(":")[0]
psw = data.split("<")[1].split(":")[1].split(">")[0]
accesscontroll = data.split("<")[1].split(":")[1].split(">")[1]


print(code)
print(id)
print(psw)
print(accesscontroll)
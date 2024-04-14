import json
import hashlib

with open("credentials.json", "r") as file:
    credentials = json.load(file)

def create_user(username, password, access_control):
    if username in credentials:
        print("User already exists.")
        return "101"
    else:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        credentials[username] = {"password": hashed_password, "access_control": access_control}
        with open("credentials.json", "w") as file:
            json.dump(credentials, file)
        print("User created successfully.")
        return "102"
    

def authenticate(username, password):
    if username in credentials:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if credentials[username]['password'] == hashed_password:
            print('found, logged in, code 102')
            return "105"
    print('wrong creds, code 103')
    return "104"
import json

with open("backend/server/credentials.json", "r") as file:
    credentials = json.load(file)

def create_user(username, password):
    if username in credentials:
        print("User already exists, code 101")
        return "101"
    else:
        credentials[username] = password
        with open("credentials.json", "w") as file:
            json.dump(credentials, file)
        print("User created successfully.")
        return "102"
    

def authenticate(username, password):
    if username in credentials and credentials[username] == password:
        print('found, logged in, code 102')
        return "105"
    else:
        print('wrong creds, code 103')
        return "104"

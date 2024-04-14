from handle_user import authenticate, create_user



user = "sxjal"
passw = "12345"


print("create user: ",create_user(username=user,password=passw))
print("login user: ",authenticate(username=user,password=passw))
passw = "1235"
print("create user: ",authenticate(username=user,password=passw))

import socket
import time
import threading
from socket import socket, AF_INET, SOCK_STREAM

PORT = 5000
HOST = '127.0.0.1'
FORMAT = "utf-8"
groupList = {"0":"123456"}
groupServerToClient = {"0":[]}

class User:
    # user class
    def __init__(self,name,client_socket,client_address):
        self._name = name
        self._client_socket = client_socket
        self._client_address = client_address
    
def deleteFromTable(groupId,user):
    # if someone left, delete from table
    size = len(groupServerToClient[str(groupId)])
    for i in range(size):
        if groupServerToClient[str(groupId)][i] == user:
            groupServerToClient[str(groupId)].pop(i)
    return

def listenChat(client_socket, client_address,groupId, user):
    # chat
    client_socket.send(("Welcome to chat #" + str(groupId)).encode(FORMAT))
    while True:
        recieve = client_socket.recv(1024).decode(FORMAT)
        message = user._name + ": " + recieve
        # if someone left, notify every one and delete him from user table
        if recieve == "Bye, Bye" or recieve == "3" :
            client_socket.send(("Bye, Bye").encode(FORMAT))
            for u in groupServerToClient[str(groupId)]:
                if user != u:
                    u._client_socket.send((user._name + " left the group").encode(FORMAT))
            deleteFromTable(groupId,user)
            disConnectServer(client_socket, client_address)
            return -1
        # send to all users in the same group chat the message except the user who send
        for u in groupServerToClient[str(groupId)]:
            if user != u:
                u._client_socket.send(message.encode(FORMAT))
    return
def createGroup(client_socket, client_address, countGroup):
    # create and connect to new group
    name_message = "Enter your name:"
    client_socket.send(name_message.encode(FORMAT))
    name = client_socket.recv(1024).decode(FORMAT)
    password_message = "Enter password:"
    client_socket.send(password_message.encode(FORMAT))
    password = client_socket.recv(1024).decode(FORMAT)
    id = countGroup
    connection_message = name  + " connected to group chat " + "#" + str(id)
    countGroup = id + 1
    client_socket.send(connection_message.encode(FORMAT))
  
    groupList[str(id)] = password
    newUser = User(name, client_socket , client_address)
    groupServerToClient[str(id)] = []
    groupServerToClient[str(id)].append(newUser)

    return id,newUser

def connectGroup(client_socket, client_address):
    
    # connect to existing group
    name_message = "Enter your name:"
    client_socket.send(name_message.encode(FORMAT))
    name = client_socket.recv(1024).decode(FORMAT)
    
    while True :
        id_message = "Enter group ID:"
        client_socket.send(id_message.encode(FORMAT))
        id = client_socket.recv(1024).decode(FORMAT)
        password_message = "Enter password:"
        client_socket.send(password_message.encode(FORMAT))
        password = client_socket.recv(1024).decode(FORMAT)
        if id in groupList and groupList[id] == password:
            break
        else:
            client_socket.send(("Wrong ID or Password").encode(FORMAT))

    connection_message = name  + " connected to group chat " + "#" + str(id)
    client_socket.send(connection_message.encode(FORMAT))
    newUser = User(name, client_socket , client_address)
    groupServerToClient[str(id)].append(newUser)
    return id, newUser

def disConnectServer(client_socket, client_address):
    client_socket.send(("Bye, Bye").encode(FORMAT))
    print(str(client_address) + " discoonnect server")
    client_socket.close()
    return



def client_handle(client_socket, client_address,countGroup):
    try:
        #sending an opening message to client
        hello_message = "Hello client, please choose an option:\n1. Connect to a group chat.\n2. Create a group chat.\n3. Exit the server."
        client_socket.send(hello_message.encode(FORMAT))
        while True:
            # switch case for the client option
            data = client_socket.recv(1024).decode(FORMAT)
            if data == "1":
                groupId , userName =  connectGroup(client_socket, client_address)
            elif data == "2":
                groupId , userName = createGroup(client_socket, client_address,countGroup)
            elif data == "3":
                disConnectServer(client_socket, client_address)
                break
            else:
                client_socket.send("error, please insert valid number".encode(FORMAT))
            if data == "1" or data == "2":
                ret = listenChat(client_socket,client_address,groupId,userName)
                # if client left, break
                if ret == -1:
                    break
    except Exception as e:
        print(f"exception", {e})
        client_socket.close()
        return False
              



def server():
    server_socket = socket(AF_INET , SOCK_STREAM) #create a connection
    server_socket.bind((HOST, PORT)) #bind
    print("server is listening ...") #listening
    server_socket.listen()
    # generate groupId
    countGroup = 1000

    while True:
        # get client socket and client address who connect to the server
        client_socket , client_address = server_socket.accept()
        #create a thread for each client
        client_thread = threading.Thread(target = client_handle,args = (client_socket,client_address,countGroup))
        client_thread.start()
        countGroup += 1

        
       

if __name__ == "__main__":
    #server side begin
    server()
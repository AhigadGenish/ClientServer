import socket
import time
import threading

PORT = 5000
HOST = '127.0.0.1'
FORMAT = "utf-8"

# send thread
def send(client_socket, client_so):
    while True:
        message = input()
        try:
            client_socket.send(message.encode(FORMAT))
        except  Exception as e:
            print(f"server connection lost, insert something to exit", {e})
            return 
        if message == "Bye, Bye" or message == "3":
            break
# recieve thread
def receive(client_socket, client_so):
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            print(message)
        except Exception as e:
            print(f"server connection lost, insert something to exit", {e})
            return 
        if message == "Bye, Bye":
            break

def client():
    # create client socket
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    try:
        receive_thread = threading.Thread(target = receive,args = (client_socket,client_socket))
        receive_thread.start()
        send_thread = threading.Thread(target = send, args = (client_socket,client_socket))
        send_thread.start()
    except Exception as e:
        print(f"server connection lost, insert something to exit", {e})
        return 
if __name__ == "__main__":
    client()
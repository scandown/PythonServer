import threading
import socket

host = '127.0.0.1' # local host
port = 10000 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
        print(f"{nicknames[clients.index(client)]}: {message}")

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} has disconnected".encode("ascii"))
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("Connected to the server".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
recieve()

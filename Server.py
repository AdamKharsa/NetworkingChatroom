import socket
import threading

host = '127.0.0.1'
port = 44444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Client list [(client,nickname),(client,nickname)...]
clientlist = []


def broadcast(message):
    for tup in clientlist:
        tup[0].send(message)


def endClientConnection(client):
    nickname = ''
    for tup in clientlist:
        if tup[0] == client:
            nickname = tup[1]
            clientlist.remove(tup)
            print(nickname+" disconnected")

    broadcast(f'{nickname} left the chat!'.encode('ascii'))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)  # Send msg from client to other clients.
            print(message.decode('ascii'))
            if message.decode('ascii').split(":")[1] == " .exit":
                endClientConnection(client)
        except:
            e = sys.exc_info()[0]
            print(e)


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clientlist.append((client,nickname))

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send("connected to the server!".encode('ascii'))
        msg = ""
        for tup in clientlist:
            msg = msg + ","+tup[1]
        msg = msg + " are connected to the chat!"
        client.send(msg.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening...")
receive()

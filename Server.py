import socket
# import ssl
import threading

host = '127.0.0.1'
port = 44444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
#
# bindsocket = socket.socket()
# bindsocket.bind((host, port))
# bindsocket.listen(5)

# Client list [(client,nickname),(client,nickname)...]
clientlist = []

def deal_with_client(connstream):
    data = connstream.recv(1024)

    while data:
        print(data)
        data = connstream.recv(1024)

def broadcast(message):
    for tup in clientlist:
        tup[0].send(message)

#
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

# while True:
#     newsocket, fromaddr = bindsocket.accept()
#     connstream = context.wrap_socket(newsocket, server_side=True)
#     try:
#         deal_with_client(connstream)
#     finally:
#         connstream.shutdown(socket.SHUT_RDWR)
#         connstream.close()

print("Server is listening...")
receive()

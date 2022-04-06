import socket
import threading
import random
import string

# import Server
# nickname = input("Choose a nickname: ")
nickname = (''.join(random.choice(string.ascii_letters) for i in range(10))) + str(random.randint(0, 10000))
# print(nickname)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 44444))


# print(Server.nicknames)


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            # if message == '.exit':
            #     client.close()
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occurred!')
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


receive_threading = threading.Thread(target=receive)
receive_threading.start()

write_threading = threading.Thread(target=write)
write_threading.start()
# client.close()

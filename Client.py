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


def recieve():
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
            print('An error occured!')
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


recieve_threading = threading.Thread(target=recieve)
recieve_threading.start()

write_threading = threading.Thread(target=write)
write_threading.start()
#client.close()

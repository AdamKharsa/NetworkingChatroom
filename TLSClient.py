import socket
import ssl

from TLSServer import context

host_addr = '127.0.0.1'
host_port = 8082
server_sni_hostname = 'google.com'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.pem'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established. Peer: {}".format(conn.getpeercert()))
print("Sending: 'Hello, world!'")
conn.send(b"Hello, world!")
print("closing connection")
conn.close()

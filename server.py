
import socket

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind(("0.0.0.0", 1234))

sSocket.listen(4)




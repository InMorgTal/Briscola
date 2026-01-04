import socket

cSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    cSocket.connect(("localhost", 1234))
    cSocket.sendall(b"Posso giocare?")

    data=cSocket.recv(1024)
    print(data.decode())






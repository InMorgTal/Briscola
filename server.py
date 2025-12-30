
import socket

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind(("localhost", 1234))

sSocket.listen(4)

listaGiocatori=[]

while True: 
    cSocket,cAddr = sSocket.accept()
    listaGiocatori.append(cSocket)






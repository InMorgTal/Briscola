import socket

cSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    cSocket.connect(("localhost", 1234))
    cSocket.sendall(b"Posso giocare?")

    data=cSocket.recv(1024)
    print(data.decode())
    break

#NON ANCORA GESTITA SUL SERVER(INVIO DELLA MANO AI GIOCTORI)
mano=cSocket.recv(1024)
print("Ecco la tua mano:")
print(mano.decode())

#NON ANCORA GESTITO SUL SERVER (IVIO DELLA BRISCOLA)
briscola=cSocket.recv(1024)

#DA GESTIRE L'INVIO DELLA MANO---INVIAMO SEMPRE LA MANO COMPLETA,
while True:
    tavolo=cSocket.recv(1024)
    print("Tavolo: ", tavolo.decode())
    msg=cSocket.recV(1024)
    print(msg.decode())









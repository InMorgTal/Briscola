
import socket
#import threading da  utillizzare con il timer
import random

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind(("localhost", 1234))

sSocket.listen(2)
listaGiocatori=[]
mazzo = [
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'
]
def inizio_partita(giocatori):
    for c in giocatori:
        try:
            c.sendall("La partita inizia!")
            c.close
        except:
            print("impossibile avviasre la partita")
    

while True: 
    cSocket,cAddr = sSocket.accept()
    listaGiocatori.append(cSocket)
    if len(listaGiocatori)==2:
        break

inizio_partita(listaGiocatori)
random.shuflle(mazzo)

mani=[]
for i in range(len(listaGiocatori)):
    mano = []
    mani.append(mano)
for i in range (3):
    for mano in mani:
        mano.append(mazzo.pop(0))#abbiamo distribuit ocarte








import socket
#import threading da  utillizzare con il timer
import random

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socket.bind(("localhost", 1234))

sSocket.listen(2)


'''

sala d attesa: 

'o 2 o (4 giocatori coppie) '

partita inizia

mescola mazzo

dare 1 carta a testa fino a 3

pesca brisola e mettiamo in fondo mazzo

inizia turno di gioco dal primo della lista

ogni giocatore gioca 1 carta a turno

in base a punteggio carte vanno al vincitore del turno

ciclo:

togliamo carta da mano 

controlliamo se ce briscola

se ce :
{

entrambe briscole
{quale vince in base al numero controlliamo se ce 1 (prende) poi se ce 3 quali delle due e maggiore , altrimenti confronto numerico}

altrimenti
{briscola vince turno}

}

se non ce:
{






}


'''


listaGiocatori=[]

mazzo = [
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'
]

mazzoConfronti = 
{
    # Basti (B)
    'B1':  {'punti': 11, 'forza': 12},
    'B2':  {'punti': 0,  'forza': 2},
    'B3':  {'punti': 10, 'forza': 11},
    'B4':  {'punti': 0,  'forza': 4},
    'B5':  {'punti': 0,  'forza': 5},
    'B6':  {'punti': 0,  'forza': 6},
    'B7':  {'punti': 0,  'forza': 7},
    'B8':  {'punti': 2,  'forza': 8},
    'B9':  {'punti': 3,  'forza': 9},
    'B10': {'punti': 4,  'forza': 10},

    # Denari (D)
    'D1':  {'punti': 11, 'forza': 12},
    'D2':  {'punti': 0,  'forza': 2},
    'D3':  {'punti': 10, 'forza': 11},
    'D4':  {'punti': 0,  'forza': 4},
    'D5':  {'punti': 0,  'forza': 5},
    'D6':  {'punti': 0,  'forza': 6},
    'D7':  {'punti': 0,  'forza': 7},
    'D8':  {'punti': 2,  'forza': 8},
    'D9':  {'punti': 3,  'forza': 9},
    'D10': {'punti': 4,  'forza': 10},

    # Coppe (C)
    'C1':  {'punti': 11, 'forza': 12},
    'C2':  {'punti': 0,  'forza': 2},
    'C3':  {'punti': 10, 'forza': 11},
    'C4':  {'punti': 0,  'forza': 4},
    'C5':  {'punti': 0,  'forza': 5},
    'C6':  {'punti': 0,  'forza': 6},
    'C7':  {'punti': 0,  'forza': 7},
    'C8':  {'punti': 2,  'forza': 8},
    'C9':  {'punti': 3,  'forza': 9},
    'C10': {'punti': 4,  'forza': 10},

    # Spade (S)
    'S1':  {'punti': 11, 'forza': 12},
    'S2':  {'punti': 0,  'forza': 2},
    'S3':  {'punti': 10, 'forza': 11},
    'S4':  {'punti': 0,  'forza': 4},
    'S5':  {'punti': 0,  'forza': 5},
    'S6':  {'punti': 0,  'forza': 6},
    'S7':  {'punti': 0,  'forza': 7},
    'S8':  {'punti': 2,  'forza': 8},
    'S9':  {'punti': 3,  'forza': 9},
    'S10': {'punti': 4,  'forza': 10},
}


tavolo={}

carteGiocatori={}

# aspettiamo 2 giocatori
while True: 
    cSocket,cAddr = sSocket.accept()
    listaGiocatori.append(cSocket)
    if len(listaGiocatori)==2:          
        break

# avviamo partita
for c in listaGiocatori:
    c.sendall("La partita inizia!")

# mischiamo mazzo
random.shuffle(mazzo)

# creo una lista mano e pila per ogni giocatore e le metto in una lista cartegiocatori
for giocatore in listaGiocatori:
     carteGiocatori[giocatore] = {'mano': [], 'pila': []}

# peschiamo briscola e mettiamola in fondo mazzo

mazzo.append(mazzo.pop(0))
briscola=mazzo[-1][0]
# estraggo una carta alla volta dal mazzo per ogni mano, fino a quando ogni mano e' composta da 3 carte

for i in range (3):
    for giocatore in listaGiocatori:
        carteGiocatori[giocatore]['mano'].append(mazzo.pop(0))



# inizio il turno di gioco
turno = 0

while True:
    #pesca
    if len(mazzo)!=0 and len(carteGiocatori[turno]['mano'])==2:
        for _ in listaGiocatori:
            carteGiocatori[turno]['mano'].append(mazzo.pop(0))
            turno = (turno + 1) % len(listaGiocatori)
    # gioca turno x ogni giocatore
    for _ in listaGiocatori:
        # invio carte sul tavolo
        listaGiocatori[turno].sendall(tavolo)
        listaGiocatori[turno].sendall("Scegli una carta da giocare dalla tua mano")
        #receive valore carta
        cartaGiocata=listaGiocatori[turno].receive()
        #mette nel tavolo carta come key
        tavolo[cartaGiocata] = listaGiocatori[turno]
        carteGiocatori[giocatore]['mano'].remove(cartaGiocata)
        # cambio turno x giocatore successivo
        turno = (turno + 1) % len(listaGiocatori)

    
    vincente = tavolo[0][0]

    for carta in tavolo[1:]:
        s_vincente = vincente[0]
        s_carta = carta[0]

        # Se vincente è briscola e carta no, vincente resta
        if s_vincente == briscola and s_carta != briscola:
            continue

        # Se carta è briscola e vincente no, carta diventa vincente
        elif s_carta == briscola and s_vincente != briscola:
            vincente = carta

        # Se stesso seme, confronta forza
        elif s_carta == s_vincente:
            if mazzoConfronti[carta]['forza'] > mazzoConfronti[vincente]['forza']:
                vincente = carta

        # Se semi diversi e nessuna briscola, vincente resta (prima carta vince)
        else:
            continue
    print("Carta vincente:", vincente)
    #trovo il giocatore vincente e gli assegno le carte nella pila
    vincitoreTurno=tavolo[vincente]
    for carte in tavolo:
        carteGiocatori[vincitoreTurno]['pila'].append(carte)
    # imposta il vinvitore del turno come primo del successivo
    turno = listaGiocatori.index(vincitoreTurno)



        








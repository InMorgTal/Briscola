


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

import socket
import threading
import time
import random
#VARIABILI GLOBALI--------------------------------------------


mazzo = [
    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
    'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
    'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10'
]

mazzoConfronti = {
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

tavolo = {}

carteGiocatori = {}

listaGiocatori = []

avvio = False

tempo = 15

lock = threading.Lock()

# FUNZIONI-----------------------------------------------------


def timerScaduto():
    global avvio
    with lock:
        n = len(listaGiocatori)
        if n == 2:
            print("⏰ Timeout: parto con 2 client")
            avvio = True
        elif n == 4:
            print("🚀 Parto con 4 client")
            avvio = True
        else:
            print("numero giocatori invalido, riavvio timer")
     
           
def giocatore_arrivato(conn):

    with lock:
        listaGiocatori.append(conn)
        n = len(listaGiocatori)
        print(f"Giocatore arrivato, tot: {n}")


def giocatore_uscito(conn):
    with lock:
        if conn in listaGiocatori:
            listaGiocatori.remove(conn)
            n = len(listaGiocatori)
            print(f"Giocatore uscito, rimasti: {n}")
    conn.close()


def verificaConnessione(conn,addr):
    while avvio==False:
       
        try:
            conn.sendall(b"Connesso")
        except socket.error as e:
            print("Client disconnesso", e)
            giocatore_uscito(conn)
            break
        try:
            data = conn.recv(1024).decode()
            if not data:
                giocatore_uscito(conn)
                break
            print(f"{addr}:{data}")
            time.sleep(1.5)
        except(ConnectionResetError, ConnectionAbortedError):
            print("Client disconnesso", e)
            giocatore_uscito(conn)
            break
     

def accettaGiocatori(sSocket):

    while avvio==False:
        cSocket, cAddr = sSocket.accept()
        giocatore_arrivato(cSocket)
        t = threading.Thread(target=verificaConnessione,args=(cSocket,cAddr))
        t.start()

def calcolaPunteggio():
    punteggio={}
    for giocatore in listaGiocatori:
        punteggio[giocatore] = 0
    for giocatori in carteGiocatori:
        for carta in giocatore['pila']:
            punteggio[giocatore]+=mazzoConfronti[carta]['punti']

    if len(listaGiocatori)==2:
        vincitore=max(punteggio, key=punteggio.get)
        punteggio_max = max(punteggio.values())
        for giocatore in listaGiocatori:
            giocatore.sendall("il tuo punteggio è: "+punteggio[giocatore])
            if giocatore==vincitore:
                giocatore.sendall("Hai vinto, complimenti")
            else:
                giocatore.sendall("Il vincitore è: "+vincitore+", con un punteggio di: "+punteggio_max)
    elif len(listaGiocatori)==4:
        punti1=0
        punti2=0
        for i, giocatori in listaGiocatori:
            if(i %2==1):
                punti1+=punteggio[giocatore]
            elif(i%2==0):
                punti2+=punteggio[giocatore]
        punteggio_max=max(punti1, punti2)
        
        for i, giocatori in listaGiocatori:
            if(i %2==1):
                giocatore.sendall("il tuo punteggio è: "+punti1)
                if punteggio_max==punti1:
                    msg=	"Hai vinto, complimenti"
                else:
                    msg= "mi dispiace hai perso"
            elif(i%2==0):
                giocatore.sendall("il tuo punteggio è: "+punti2)
                if punteggio_max==punti2:
                    msg=	"Hai vinto, complimenti"
                else:
                    msg= "mi dispiace hai perso"
            giocatore.sendall(msg)

# MAIN---------------------------------------------------------

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sSocket.bind(("localhost", 1234))

sSocket.listen(4)


while True:

    c = input("Avviare nuova partita? Y/N: ").strip().upper()
    
    if c == 'N':
        break

    #ATTESA NUOVI GIOCATORI 

    listaGiocatori.clear()
    avvio = False
    print("Server in attesa...\n")

    t = threading.Thread(target=accettaGiocatori,args=(sSocket,))
    t.start()

    while avvio==False:
        time.sleep(15)
        timerScaduto()

    for g in listaGiocatori:
       
        g.sendall(b"La partita inizia!")

    print("inizio gioco")

'''

    # INIZIO GIOCO

    # comunichiamo avvio partita
    for g in listaGiocatori:
        print("inizio gioco")
        g.sendall("La partita inizia!")

    # mischiamo mazzo
    random.shuffle(mazzo)
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
        
        
        
        #GESTIRE VISIONE TAVOLO SE INIZIO PER PRIMO

        
'''

##############################################################
#CALCOLO PUNTEGGIO; è UN PO MACCHINOSO MA DOVREBBE FUNZIONARE
############################################################
calcolaPunteggio()

################### FINE CALCOLO PUNTEGGIO  ######################
#################################################################



'''
print("Terminando connessioni")


'''

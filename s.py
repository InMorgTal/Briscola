import socket
import threading
import time
import random

mazzo_base = [
    #'B1','B2','B3','B4','B5',
    'B6','B7','B8','B9','B10',
    #'D1','D2','D3','D4','D5',
    'D6','D7','D8','D9','D10',
    'C1','C2','C3','C4','C5',
    #'C6','C7','C8','C9','C10',
    #'S1','S2','S3','S4','S5',
    'S6','S7','S8','S9','S10'
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

listaGiocatori = []

avvio = False

lock = threading.Lock()

def ricevi(conn):
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            print("Errore ricezione: connessione chiusa dal client")
            return -1
        return data
    except Exception as e:
        print(f"Errore ricezione: {e}")
        return -1
        
def invia(conn, mess):
    try:
        conn.sendall(mess.encode())
    except:
        return -1

def giocatore_uscito(conn):
    with lock:
        if conn in listaGiocatori:
            listaGiocatori.remove(conn)
            print("Giocatore uscito, rimasti:", len(listaGiocatori))
    conn.close()

def timerScaduto():
    global avvio
    with lock:
        n = len(listaGiocatori)
        if n in (2, 4):
            print("⏱ Timeout: parto con", n, "client")
            avvio = True
        else:
            print("Numero giocatori invalido, riavvio timer")

def verificaConnessione(conn, addr):
    global avvio
    while not avvio:
        try:
            conn.sendall(b"In attesa...")
        except:
            giocatore_uscito(conn)
            break

        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                giocatore_uscito(conn)
                break
        except:
            giocatore_uscito(conn)
            break

        time.sleep(1.5)

def accettaGiocatori(sSocket):
    global avvio
    sSocket.settimeout(1)  # Imposto timeout di 1 secondo

    while not avvio:
        try:
            cSocket, cAddr = sSocket.accept()
        except socket.timeout:
            # Timeout scaduto, controllo se avvio è cambiato e riparto
            continue
        except Exception as e:
            print(f"Errore su accept: {e}")
            continue

        with lock:
            listaGiocatori.append(cSocket)
            print("Giocatore arrivato, tot:", len(listaGiocatori))

        threading.Thread(target=verificaConnessione, args=(cSocket, cAddr)).start()

    sSocket.settimeout(None)  # Rimetto modalità bloccante (opzionale)
    
def calcolaPunteggioPartita(carteGiocatori):
    
    vincitore = listaGiocatori[0]

    if len(listaGiocatori)==4: # se sono 4 gioctatori faccio la somma a squadre
        punteggioSquadra1 = carteGiocatori[listaGiocatori[0]]['pila'] + carteGiocatori[listaGiocatori[2]]['pila']
        punteggioSquadra2 = carteGiocatori[listaGiocatori[1]]['pila'] + carteGiocatori[listaGiocatori[3]]['pila']

        if punteggioSquadra1 > punteggioSquadra2:
            for g in listaGiocatori:
                invia(g,f"Hai totalizzato {carteGiocatori[g]['pila']} punti, Squadra di G1 e G2 vince! con {punteggioSquadra1} punti!\n")

            return
        for g in listaGiocatori:
                invia(g,f"Hai totalizzato {carteGiocatori[g]['pila']} punti, Squadra di G2 e G4 vince! con {punteggioSquadra2} punti!\n")
 
    else:   # altrimenti controllo il singolo vincitore
            
        for g in carteGiocatori:
            if carteGiocatori[g]['pila'] > carteGiocatori[vincitore]['pila']:
                vincitore = g
            
        for g in listaGiocatori:
            invia(g, f"Hai totalizzato {carteGiocatori[g]['pila']} punti, il vincitore della partita e' il giocatore {listaGiocatori.index(vincitore)+1} con {carteGiocatori[vincitore]['pila']} punti!\n")
        return 
        
def calcolaVincitoreTurno(tavolo,briscola,carteGiocatori):
    # DETERMINA VINCITORE DEL TURNO

    carta_vincente = list(tavolo.keys())[0]

    seme_vincente = carta_vincente[0]

    for carta in list(tavolo.keys())[1:]:
        seme_carta = carta[0]
        if seme_vincente == briscola and seme_carta != briscola:
            continue
        elif seme_carta == briscola and seme_vincente != briscola:
            carta_vincente = carta
            seme_vincente = seme_carta
        elif seme_carta == seme_vincente and mazzoConfronti[carta]['forza'] > mazzoConfronti[carta_vincente]['forza']:
            carta_vincente = carta
    
    vincitore=tavolo[carta_vincente]
    print("carta vincente:", carta_vincente, "giocatore:", listaGiocatori.index(vincitore)+1)
    carteGiocatori[vincitore]['pila'] += calcolaPunteggioTurno(tavolo)
    print("Punti fatti", calcolaPunteggioTurno(tavolo))
    return vincitore

def calcolaPunteggioTurno(tavolo):
    punteggio = 0
    for carta in tavolo.keys():
        punteggio += mazzoConfronti[carta]['punti']

    return punteggio

def isPartitaFinita(listaGiocatori, carteGiocatori):
    for g in listaGiocatori:
        if len(carteGiocatori[g]['mano']) != 0:
            return False  # Almeno un giocatore ha ancora carte
    return True  # Tutti hanno finito le carte

def partita(listaGiocatori):

    Fine = False

    carteGiocatori = {}

    for g in listaGiocatori:
        carteGiocatori[g] = {
            'mano': [],
            'pila': 0
        }

    tavolo = {}

    for g in listaGiocatori:
        invia(g, "start")# segnale per client di iniziare partita e uscire da verificaConnessione

    print("Inizio gioco")

    mazzo = mazzo_base.copy()

    random.shuffle(mazzo)
    random.shuffle(mazzo)

    mazzo.append(mazzo.pop(0))#prendo briscola da sopra mazzo 
    briscola = mazzo[-1][0]# metto la briscola in fondo mazzo

    for _ in range(3):#come nella briscola vera do una carta a testa per tre volte dal mazzo
        for g in listaGiocatori:
            carteGiocatori[g]['mano'].append(mazzo.pop(0))

    turno = 0

    while Fine == False:

        tavolo.clear()

        # peschiamo se necessario
        if len(mazzo) > 0 and len(carteGiocatori[listaGiocatori[turno]]['mano']) < 3:
            for g in listaGiocatori:
                carteGiocatori[g]['mano'].append(mazzo.pop(0))


        # turno dei giocatori
        for _ in listaGiocatori:

             #prendiamo il giocatore che iniziera il turno che si decide a fine round o a inizio partita dal primo
            g = listaGiocatori[turno] 

            # Invia turno briscola tavolo e mano
            for x in listaGiocatori:
                tavolo_str = ",".join(tavolo.keys())
                mano_str = ",".join(carteGiocatori[x]['mano'])

                invia(
                        x,
                        f"Numero giocatori:{len(listaGiocatori)}\n"
                        f"Tu sei giocatore:{listaGiocatori.index(x)+1}\n"
                        f"Turno giocatore:{listaGiocatori.index(g)+1}\n"
                        f"Briscola:{briscola} Tavolo:{tavolo_str}\n"
                        f"Mano:{mano_str}\n"
                    )
                # invia a tutti i giocatori lo stato attuale
            print ("attendo carta da giocatore", listaGiocatori.index(g)+1)
            carta = ricevi(g) # prendiamo la carta giocata dal giocatore (controlli lato client)
            
            if carta == -1:
                print("Giocatore disconnesso, terminazione partita")
                for x in listaGiocatori:
                    if x != g:
                        invia(x, "Un giocatore si e' disconnesso, partita terminata.\n")
                return
            
            print("ricevuta carta:", carta, "da giocatore", listaGiocatori.index(g)+1)
            tavolo[carta]= g # aggiungiamo carta al tavolo associata al giocatore

            carteGiocatori[g]['mano'].remove(carta)

            turno = (turno + 1) % len(listaGiocatori)
        
        vincitore = calcolaVincitoreTurno(tavolo, briscola,carteGiocatori)
      
        turno = listaGiocatori.index(vincitore) # il vincitore inizia il prossimo turno
        
        for x in listaGiocatori:
            invia(x, f"Il vincitore del round e' il giocatore {listaGiocatori.index(vincitore)+1}, totalizzando {carteGiocatori[vincitore]['pila']} punti\n")

        if isPartitaFinita(listaGiocatori, carteGiocatori)== True:
            Fine = True

    calcolaPunteggioPartita(carteGiocatori)
        

def main():

    global avvio

    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sSocket.bind(("localhost", 1234))
    sSocket.listen(4)

    while True:
        c = input("Avviare nuova partita? *Y/N: ").strip().upper()
        if c == "N":
            break

        listaGiocatori.clear()
        
        avvio = False

        print("Server in attesa...\n")
        threading.Thread(target=accettaGiocatori, args=(sSocket,)).start()

        while not avvio:
            time.sleep(10)
            timerScaduto()

        partita(listaGiocatori)

if __name__ == "__main__":
    main()
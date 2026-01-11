import socket
import threading
import time
import random

# Librerie principali, gestione socket e thread

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
# Mazzo base carte (usate nella partita)

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

# Connessioni client attivi
listaGiocatori = []

avvio = False

lock = threading.Lock()

def ricevi(conn):
    # Ricezione dati dal client, ritorna stringa o -1 su errore/disconnessione
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
    # Invio messaggi al client, ritorna -1 se invio fallisce
    try:
        conn.sendall(mess.encode())
    except:
        return -1

def giocatore_uscito(conn):
    # Rimuovi giocatore disconnesso e chiudi socket
    with lock:
        if conn in listaGiocatori:
            listaGiocatori.remove(conn)
            print("Giocatore uscito, rimasti:", len(listaGiocatori))
    conn.close()

def timerScaduto():
    global avvio
    # Timer avvio partita: verifica numero giocatori valido
    with lock:
        n = len(listaGiocatori)
        if n in (2, 4):
            print("⏱ Timeout: parto con", n, "client")
            avvio = True
        else:
            print("Numero giocatori invalido, riavvio timer")

def verificaConnessione(conn, addr):
    global avvio
    # Controllo connessione periodico durante fase attesa
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
    sSocket.settimeout(1)  # Timeout1s: accept non bloccante per controlli

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

        # Avvia thread che mantiene connessione e segnala disconnessione
        threading.Thread(target=verificaConnessione, args=(cSocket, cAddr)).start()

    sSocket.settimeout(None)  # Rimetto modalità bloccante (opzionale)
    
def calcolaPunteggioPartita(carteGiocatori):
    # Calcolo risultati finali: gestisce 2 o 4 giocatori, invio messaggi e log
    giocatori = list(carteGiocatori.keys())

    # 4 giocatori: somma per squadre (G1+G3 contro G2+G4)
    if len(giocatori) == 4:
        # Leggi punti individuali
        punti_g1 = carteGiocatori[giocatori[0]]['pila']
        punti_g2 = carteGiocatori[giocatori[1]]['pila']
        punti_g3 = carteGiocatori[giocatori[2]]['pila']
        punti_g4 = carteGiocatori[giocatori[3]]['pila']

        # Somma punteggi squadre (G1+G3 vs G2+G4)
        puntiS1 = punti_g1 + punti_g3  # G1 e G3
        puntiS2 = punti_g2 + punti_g4  # G2 e G4

        if puntiS1 > puntiS2:
            msg = f"Partita terminata.\nLa squadra di G1 e G3 vince con {puntiS1} punti!"
            print("la squadra di G1 e G3 vince con", puntiS1, "punti!")
        elif puntiS2 > puntiS1:
            msg = f"Partita terminata.\nLa squadra di G2 e G4 vince con {puntiS2} punti!"
            print("la squadra di G2 e G4 vince con", puntiS2, "punti!")
        else:
            msg = f"Partita terminata.\nPareggio! Squadra 1: {puntiS1} punti, Squadra 2: {puntiS2} punti."
            print("Pareggio! Squadra 1:", puntiS1, "punti, Squadra 2:", puntiS2, "punti.")

        # Invia risultato a ciascun giocatore e log
        for g in giocatori:
            invia(g, f"Hai totalizzato {carteGiocatori[g]['pila']} punti. {msg}\n")
            print("Il giocatore", giocatori.index(g)+1, "ha totalizzato", carteGiocatori[g]['pila'], "punti.")
        return

    # 2 giocatori: singolo vincitore
    vincitore = giocatori[0]
    for g in giocatori:
        if carteGiocatori[g]['pila'] > carteGiocatori[vincitore]['pila']:
            vincitore = g

    for g in giocatori:
        invia(g,
            f"Partita terminata.\nHai totalizzato {carteGiocatori[g]['pila']} punti. "
            f"Il vincitore della partita è il giocatore {giocatori.index(vincitore)+1} "
            f"con {carteGiocatori[vincitore]['pila']} punti!\n")
        print("Il giocatore", giocatori.index(g)+1, "ha totalizzato", carteGiocatori[g]['pila'], "punti.")
        
    print("Partita terminata")
    return

def calcolaVincitoreTurno(tavolo,briscola,carteGiocatori):
    # Determina carta vincente considerando briscola e forza carte

    carta_vincente = list(tavolo.keys())[0]

    seme_vincente = carta_vincente[0]

    for carta in list(tavolo.keys())[1:]:
        # Confronta seme e briscola
        seme_carta = carta[0]
        if seme_vincente == briscola and seme_carta != briscola:
            continue
        elif seme_carta == briscola and seme_vincente != briscola:
            # Briscola batte non-briscola
            carta_vincente = carta
            seme_vincente = seme_carta
        elif seme_carta == seme_vincente and mazzoConfronti[carta]['forza'] > mazzoConfronti[carta_vincente]['forza']:
            # Stesso seme: confronta forza
            carta_vincente = carta
    
    vincitore=tavolo[carta_vincente]
    print("carta vincente:", carta_vincente, "giocatore:", listaGiocatori.index(vincitore)+1)
    carteGiocatori[vincitore]['pila'] += calcolaPunteggioTurno(tavolo)
    print("Punti fatti", calcolaPunteggioTurno(tavolo))
    return vincitore

def calcolaPunteggioTurno(tavolo):
    # Somma punti delle carte sul tavolo per il turno
    punteggio = 0
    for carta in tavolo.keys():
        punteggio += mazzoConfronti[carta]['punti']

    return punteggio

def isPartitaFinita(listaGiocatori, carteGiocatori):
    # Controlla se tutti i giocatori hanno esaurito le carte
    for g in listaGiocatori:
        if len(carteGiocatori[g]['mano']) != 0:
            return False  # Partita non terminata
    return True  # Partita terminata

def partita(listaGiocatori):

    Fine = False

    # Inizializza strutture giocatori e tavolo
    carteGiocatori = {}

    for g in listaGiocatori:
        carteGiocatori[g] = {
            'mano': [],
            'pila': 0
        }

    # Stato carte sul tavolo per turno
    tavolo = {}

    for g in listaGiocatori:
        invia(g, "start") # Segnale inizio partita al client

    print("Inizio gioco")

    mazzo = mazzo_base.copy()

    # Mischia mazzo più volte per casualità
    random.shuffle(mazzo)
    random.shuffle(mazzo)

    # Seleziona la prima carta come briscola, spostandola in fondo mazzo
    mazzo.append(mazzo.pop(0)) # Seleziona briscola e sposta in fondo mazzo
    briscola = mazzo[-1][0] # Lettura seme briscola

    # Distribuzione iniziale di 3 carte per giocatore (ordine di mano)
    for _ in range(3): # Distribuzione iniziale: 3 carte a ciascun giocatore
        for g in listaGiocatori:
            carteGiocatori[g]['mano'].append(mazzo.pop(0))

    turno = 0

    while Fine == False:

        tavolo.clear()

        # Pesca carte dal mazzo se disponibili per mantenere 3 in mano
        if len(mazzo) > 0 and len(carteGiocatori[listaGiocatori[turno]]['mano']) < 3:
            # Ogni giocatore pesca una carta
            for g in listaGiocatori:
                carteGiocatori[g]['mano'].append(mazzo.pop(0))


        # Ciclo turno giocatori: ciascun giocatore gioca una carta per round
        for _ in listaGiocatori:

             # Seleziona giocatore corrente in base a turno
            g = listaGiocatori[turno] 

            # Invio stato a tutti i client: numero, turno, briscola, mano
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
                # Broadcast stato a client
            print ("attendo carta da giocatore", listaGiocatori.index(g)+1)
            # Ricezione carta giocata dal client (controllo disconnessione)
            carta = ricevi(g) # Ricezione carta dal client, -1 se disconnesso
            
            if carta == -1:
                print("Giocatore disconnesso, terminazione partita")
                # Notifica gli altri e termina partita
                for x in listaGiocatori:
                    if x != g:
                        invia(x, "Un giocatore si e' disconnesso, partita terminata.\n")
                return
            
            print("ricevuta carta:", carta, "da giocatore", listaGiocatori.index(g)+1)
            # Aggiunge carta giocata al tavolo e la rimuove dalla mano
            tavolo[carta]= g # Aggiungi carta al tavolo con riferimento giocatore

            carteGiocatori[g]['mano'].remove(carta)

            # Passa al giocatore successivo
            turno = (turno + 1) % len(listaGiocatori)
        
        vincitore = calcolaVincitoreTurno(tavolo, briscola,carteGiocatori)
      
        turno = listaGiocatori.index(vincitore) # ProssimoTurno: vincitore inizia round successivo
        
        for x in listaGiocatori:
            invia(x, f"Il vincitore del round e' il giocatore {listaGiocatori.index(vincitore)+1}, totalizzando {carteGiocatori[vincitore]['pila']} punti\n")

        if isPartitaFinita(listaGiocatori, carteGiocatori)== True:
            # Termina loop principale quando tutte le mani esaurite
            Fine = True

    # Calcola ed invia risultati finali
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
            time.sleep(20)  # Attesa 20 secondi per connessioni
            timerScaduto()

        partita(listaGiocatori)

if __name__ == "__main__":
    main()
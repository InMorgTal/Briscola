import socket
import threading
import time
import random

# VARIABILI GLOBALI --------------------------------------------

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

tavolo = []  # Cambiato da dict a lista di tuple (carta, giocatore)
carteGiocatori = {}

listaGiocatori = []

avvio = False
lock = threading.Lock()

# TEMPO PER ASPETTARE GIOCATORI PRIMA DI INIZIARE (esempio)
tempo = 15

# FUNZIONI -----------------------------------------------------

def timerScaduto():
    global avvio
    with lock:
        n = len(listaGiocatori)
        if n == 2 or n == 4:
            print(f"⏰ Timeout: parto con {n} client")
            avvio = True
        else:
            print("Numero giocatori invalido, riavvio timer")


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


def verificaConnessione(conn, addr):
    global avvio
    while True:
        with lock:
            if avvio:
                break
        try:
            conn.sendall(b"In attesa...")
        except socket.error as e:
            print("Client disconnesso", e)
            giocatore_uscito(conn)
            break
        try:
            data = conn.recv(1024).decode()
            if not data:
                giocatore_uscito(conn)
                break
            print(f"{addr}: {data}")
            time.sleep(1.5)
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print("Client disconnesso", e)
            giocatore_uscito(conn)
            break


def accettaGiocatori(sSocket):
    global avvio
    while True:
        with lock:
            if avvio:
                break
        cSocket, cAddr = sSocket.accept()
        giocatore_arrivato(cSocket)
        t = threading.Thread(target=verificaConnessione, args=(cSocket, cAddr))
        t.start()


def calcolaPunteggio():
    punteggio = {g: 0 for g in listaGiocatori}
    for g in listaGiocatori:
        for carta in carteGiocatori[g]['pila']:
            punteggio[g] += mazzoConfronti[carta]['punti']

    vincitore = max(punteggio, key=punteggio.get)
    punteggio_max = punteggio[vincitore]

    for g in listaGiocatori:
        invia(g, f"Il tuo punteggio è: {punteggio[g]}")
        if g == vincitore:
            invia(g, "Hai vinto, complimenti!")
        else:
            invia(g, f"Il vincitore è un altro giocatore con {punteggio_max} punti.")


def invia(conn, mess):
    try:
        conn.sendall(mess.encode())
    except Exception as e:
        print(f"Errore durante la comunicazione, partita interrotta:\n{e}")
        giocatore_uscito(conn)
        return -1
    return 0


def primaMano():
    for g in listaGiocatori:
        mano_msg = ",".join(carteGiocatori[g]['mano'])
        msg = f"Your_turn:{mano_msg}. La briscola è: {briscola}"
        if invia(g, msg) == -1:
            return -1
    return 0


# MAIN ---------------------------------------------------------

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sSocket.bind(("localhost", 1234))
sSocket.listen(4)

while True:
    c = input("Avviare nuova partita? Y/N: ").strip().upper()

    if c == 'N':
        break

    # RESET VARIABILI
    listaGiocatori.clear()
    carteGiocatori.clear()
    tavolo.clear()
    avvio = False

    print("Server in attesa...\n")

    t = threading.Thread(target=accettaGiocatori, args=(sSocket,))
    t.start()

    # Aspetta fino a quando timer scade e ci sono 2 o 4 giocatori
    while True:
        time.sleep(5)
        timerScaduto()
        with lock:
            if avvio:
                break

    # Comunico numero giocatori e avvio partita
    for g in listaGiocatori:
        if invia(g, str(len(listaGiocatori))) == -1:
            break
        if invia(g, "La partita inizia!") == -1:
            break

    print("Inizio gioco")

    # Mischio mazzo due volte
    random.shuffle(mazzo)
    random.shuffle(mazzo)

    # Creo struttura carte giocatori
    for g in listaGiocatori:
        carteGiocatori[g] = {'mano': [], 'pila': []}

    # Pesco briscola (ultima carta)
    mazzo.append(mazzo.pop(0))
    briscola = mazzo[-1][0]

    # Distribuisco 3 carte per ogni giocatore
    for i in range(3):
        for g in listaGiocatori:
            carteGiocatori[g]['mano'].append(mazzo.pop(0))

    # Invio prima mano
    if primaMano() == -1:
        continue

    turno = 0  # indice giocatore

    # ciclo gioco
    while True:
        # Pesca (se mazzo non vuoto e mano del giocatore con 2 carte)
        if len(mazzo) != 0 and len(carteGiocatori[listaGiocatori[turno]]['mano']) == 2:
            # il giocatore di turno pesca la prima carta dal mazzo
            pescata = mazzo.pop(0)
            carteGiocatori[listaGiocatori[turno]]['mano'].append(pescata)
            # comunico a tutti i giocatori la pesca e la nuova mano di chi ha pescato
            for g in listaGiocatori:
                mano_msg = ",".join(carteGiocatori[listaGiocatori[turno]]['mano'])
                msg = f"Pesca:{mano_msg}"
                invia(g, msg)

        # Turno di gioco: ogni giocatore gioca una carta (round)
        tavolo.clear()
        for _ in listaGiocatori:
            giocatore_corrente = listaGiocatori[turno]
            mano = carteGiocatori[giocatore_corrente]['mano']
            msg = "Your_turn:" + ",".join(mano)
            if invia(giocatore_corrente, msg) == -1:
                break

            try:
                cartaGiocata = giocatore_corrente.recv(1024).decode().strip()
            except Exception as e:
                print(f"Errore ricezione carta: {e}")
                giocatore_uscito(giocatore_corrente)
                break

            if cartaGiocata not in mano:
                print(f"Giocatore ha giocato carta non valida: {cartaGiocata}")
                # puoi decidere se far ripetere o altro, per ora skippo
                break

            # Aggiungo carta giocata a tavolo
            tavolo.append((cartaGiocata, giocatore_corrente))
            carteGiocatori[giocatore_corrente]['mano'].remove(cartaGiocata)

            # Comunico tavolo aggiornato a tutti
            carte_su_tavolo = ",".join(c for c, _ in tavolo)
            for g in listaGiocatori:
                invia(g, f"Tavolo:{carte_su_tavolo}")

            turno = (turno + 1) % len(listaGiocatori)

        # Se tutti hanno giocato (3 o altro numero carte giocate)
        if len(tavolo) == len(listaGiocatori):
            # Calcolo carta vincente turno
            vincente, vincitoreTurno = tavolo[0]
            seme_vincente = vincente[0]

            for carta, _ in tavolo[1:]:
                seme_carta = carta[0]

                # Regole briscola
                if seme_vincente == briscola and seme_carta != briscola:
                    continue
                elif seme_carta == briscola and seme_vincente != briscola:
                    vincente = carta
                    seme_vincente = seme_carta
                elif seme_carta == seme_vincente:
                    if mazzoConfronti[carta]['forza'] > mazzoConfronti[vincente]['forza']:
                        vincente = carta
                else:
                    continue

            # Trova vincitore reale del turno
            for carta, gioc in tavolo:
                if carta == vincente:
                    vincitoreTurno = gioc
                    break

            print(f"Carta vincente: {vincente}, giocatore vincente: {vincitoreTurno}")

            # Assegna carte prese al vincitore
            for carta, _ in tavolo:
                carteGiocatori[vincitoreTurno]['pila'].append(carta)

            # Comunico fine turno e vincitore a tutti
            for g in listaGiocatori:
                invia(g, f"Fine_turno:{vincitoreTurno.getpeername()}")

            # Imposto turno al vincitore
            turno = listaGiocatori.index(vincitoreTurno)

            # Se le mani sono finite (mano vuote), finisco partita
            if all(len(carteGiocatori[g]['mano']) == 0 for g in listaGiocatori):
                print("Partita finita, calcolo punteggi...")
                calcolaPunteggio()
                break


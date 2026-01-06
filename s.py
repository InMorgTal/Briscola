import socket
import threading
import time
import random

mazzo_base = [
    'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10',
    'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10',
    'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10',
    'S1','S2','S3','S4','S5','S6','S7','S8','S9','S10'
]

mazzoConfronti = {
    c: {
        'punti': {1:11, 2:0, 3:10, 4:0, 5:0, 6:0, 7:0, 8:2, 9:3, 10:4}[int(c[1:])],
        'forza': {1:12, 2:2, 3:11, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10}[int(c[1:])]
    }
    for c in mazzo_base
}

listaGiocatori = []
carteGiocatori = {}
tavolo = []
avvio = False
lock = threading.Lock()

def invia(conn, mess):
    try:
        conn.sendall(mess.encode())
        return 0
    except:
        return -1

def giocatore_arrivato(conn):
    with lock:
        listaGiocatori.append(conn)
        print("Giocatore arrivato, tot:", len(listaGiocatori))

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
    while not avvio:
        cSocket, cAddr = sSocket.accept()
        giocatore_arrivato(cSocket)
        threading.Thread(target=verificaConnessione, args=(cSocket, cAddr)).start()

def calcolaPunteggio():
    punteggio = {g: 0 for g in listaGiocatori}
    for g in listaGiocatori:
        for carta in carteGiocatori[g]['pila']:
            punteggio[g] += mazzoConfronti[carta]['punti']

    vincitore = max(punteggio, key=punteggio.get)
    maxpunti = punteggio[vincitore]

    for g in listaGiocatori:
        invia(g, f"Il tuo punteggio è: {punteggio[g]}")
        if g == vincitore:
            invia(g, "Hai vinto, complimenti!")
        else:
            invia(g, f"Il vincitore ha totalizzato {maxpunti} punti.")

def primaMano(briscola):
    for g in listaGiocatori:
        mano = ",".join(carteGiocatori[g]['mano'])
        invia(g, f"Your_turn:{mano}")
        invia(g, f"Briscola:{briscola}")
    return 0

sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sSocket.bind(("localhost", 1234))
sSocket.listen(4)

while True:
    c = input("Avviare nuova partita? Y/N: ").strip().upper()
    if c == "N":
        break

    listaGiocatori.clear()
    carteGiocatori.clear()
    tavolo.clear()
    avvio = False

    print("Server in attesa...\n")
    threading.Thread(target=accettaGiocatori, args=(sSocket,)).start()

    while not avvio:
        time.sleep(5)
        timerScaduto()

    for g in listaGiocatori:
        invia(g, "La partita inizia!")
    for g in listaGiocatori:
        invia(g, str(len(listaGiocatori)))

    print("Inizio gioco")

    mazzo = mazzo_base.copy()
    random.shuffle(mazzo)
    random.shuffle(mazzo)

    for g in listaGiocatori:
        carteGiocatori[g] = {'mano': [], 'pila': []}

    mazzo.append(mazzo.pop(0))
    briscola = mazzo[-1][0]

    for _ in range(3):
        for g in listaGiocatori:
            carteGiocatori[g]['mano'].append(mazzo.pop(0))

    turno = 0
    primaMano(briscola)

    while True:

        # PESCA
        if len(mazzo) > 0 and len(carteGiocatori[listaGiocatori[turno]]['mano']) == 2:
            pescata = mazzo.pop(0)
            carteGiocatori[listaGiocatori[turno]]['mano'].append(pescata)
            invia(listaGiocatori[turno], f"Pesca:{','.join(carteGiocatori[listaGiocatori[turno]]['mano'])}")

        tavolo.clear()

        # TURNO DI OGNI GIOCATORE
        for _ in listaGiocatori:
            g = listaGiocatori[turno]

            # Avvisa gli altri
            for x in listaGiocatori:
                if x != g:
                    invia(x, "Attendi_il_tuo_turno")

            # Manda la mano al giocatore di turno
            mano = ",".join(carteGiocatori[g]['mano'])
            invia(g, f"Your_turn:{mano}")

            try:
                carta = g.recv(1024).decode().strip()
            except:
                giocatore_uscito(g)
                break

            if carta not in carteGiocatori[g]['mano']:
                invia(g, "Carta non valida, riprova.")
                continue  # NON avanza il turno

            tavolo.append((carta, g))
            carteGiocatori[g]['mano'].remove(carta)

            for x in listaGiocatori:
                invia(x, "Tavolo:" + ",".join(c for c, _ in tavolo))

            turno = (turno + 1) % len(listaGiocatori)

        # DETERMINA VINCITORE DEL TURNO
        if len(tavolo) == len(listaGiocatori):
            vincente, vincitoreTurno = tavolo[0]
            seme_vincente = vincente[0]

            for carta, gioc in tavolo[1:]:
                seme_carta = carta[0]
                if seme_vincente == briscola and seme_carta != briscola:
                    continue
                elif seme_carta == briscola and seme_vincente != briscola:
                    vincente = carta
                    seme_vincente = seme_carta
                elif seme_carta == seme_vincente:
                    if mazzoConfronti[carta]['forza'] > mazzoConfronti[vincente]['forza']:
                        vincente = carta

            for carta, gioc in tavolo:
                if carta == vincente:
                    vincitoreTurno = gioc
                    break

            for carta, _ in tavolo:
                carteGiocatori[vincitoreTurno]['pila'].append(carta)

            for g in listaGiocatori:
                invia(g, f"Fine_turno:{listaGiocatori.index(vincitoreTurno)}")

            turno = listaGiocatori.index(vincitoreTurno)

            if all(len(carteGiocatori[g]['mano']) == 0 for g in listaGiocatori):
                calcolaPunteggio()
                break

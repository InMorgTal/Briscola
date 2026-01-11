import socket
import time

avvio = False

def invia(conn, mess):
    try:
        conn.sendall(mess.encode())
    except:
        return -1

def ricevi(conn):
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return -1
        return data
    except:
        return -1

def verificaConnessione(conn):
    global avvio
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                return -1

            if data == "start":
                print("Il gioco sta iniziando...\n")
                avvio = True
                return 0

            print(f"{data}\n")

        except:
            return -1

        try:
            conn.sendall(b"Connesso")
        except:
            return -1


cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    
    print("Connettendo al server...\n")

    try:
        cSocket.connect(("localhost", 1234))
  
    except Exception as e:
        print(f"Errore: {e}  Attendi per riprovare...\n")
        time.sleep(5)
        continue

    print("In attesa che il server avvii la partita...\n")
    if verificaConnessione(cSocket) == -1:
        print("Connessione persa, interruzione partita\n")
        cSocket.close()
        time.sleep(5)
        continue


    # --- CICLO DI GIOCO ---
    while True:
        try:
            msg = ricevi(cSocket)
            if msg == -1:
                print("Connessione persa, interruzione partita\n")
                cSocket.close()
                time.sleep(5)
                continue

            print(msg)#stampiamo lo stato del gioco

            

            righe = msg.split("\n")
            print("CONTROLLO1")
            mano = righe[4].split(":", 1)[1].split(",")#otteniamo list mano
            
            if mano == "":
                mano = []
            else:
                mano = mano.split(",")
            
            print("CONTROLLO2")
            numGiocatore = int(righe[1].split(":", 1)[1])# otteniamo num giocatore
            print("CONTROLLO3")
            turnoGiocatore = int(righe[2].split(":", 1)[1])# otteniamo turno giocatore
            print("CONTROLLO4")
            if numGiocatore == turnoGiocatore:
                print("È il tuo turno")
                while True:
                    carta = input("Scegli una carta da giocare: ").strip().upper()
                    if carta in mano:
                        break
                    print("Carta non valida.")

                cSocket.sendall(carta.encode())
            else:
                print("Attendi")

        except Exception as e:
            print(f"Errore: {e}")
            break

    cSocket.close()
    break

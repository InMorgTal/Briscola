import socket
import time
import os
avvio = False
# Flag avvio partita (True quando il server comunica start)

# Librerie

def invia(conn, mess):
    # Invio
    try:
        conn.sendall(mess.encode())
    except:
        return -1

def ricevi(conn):
    # Ricezione
    try:
        data = conn.recv(1024).decode().strip()
        if not data:
            return -1
        return data
    except:
        return -1

def verificaConnessione(conn):
    global avvio
    # Ascolto messaggi server e segnalo avvio
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

def main():

    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        
        print("Connettendo al server...\n")
        # Connessione al server
        try:
            cSocket.connect(("localhost", 1234))
    
        except Exception as e:
            print(f"Errore: {e}  Attendi per riprovare...\n")
            time.sleep(5)
            continue

        print("In attesa che il server avvii la partita...\n")
        # Attesa segnale start dal server
        if verificaConnessione(cSocket) == -1:
            print("Connessione persa, interruzione partita\n")
            cSocket.close()
            time.sleep(5)
            continue

        # CicloGioco
        while True:
        
            try:
                # Ricezione stato dal server
                msg = ricevi(cSocket)
                if msg == -1:
                    print("Connessione persa, interruzione partita\n")
                    cSocket.close()
                    time.sleep(5)
                    continue
                os.system('cls')
                print(msg) # StampaStato
                if "terminata" in msg:

                    break

                if "vincitore" in msg:
                    time.sleep(4)
                    continue
                
                # Parsing messaggio di stato in righe
                righe = msg.split("\n")

                # Estrai stringa mano dal messaggio
                mano_str = righe[4].split(":", 1)[1].strip()  # EstraiMano

                if mano_str == "":
                    mano = []
                else:
                    mano = mano_str.split(",")
    

                numGiocatore = int(righe[1].split(":", 1)[1].strip())  # NumGiocatore

                turnoGiocatore = int(righe[2].split(":", 1)[1].strip())  # TurnoGiocatore

                if numGiocatore == turnoGiocatore:
                    print("È il tuo turno")
                    while True:
                        carta = input("Scegli una carta da giocare: ").strip().upper()
                        if carta in mano:
                            break
                        print("Carta non valida.")

                    # Invia carta scelta al server
                    cSocket.sendall(carta.encode())

                else:
                    print("Attendi")

            except Exception as e:
                print(f"Errore: {e}")
                break

        # Chiudi socket client e termina
        cSocket.close()
        break

if __name__ == "__main__":
    main()
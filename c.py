import socket
import time

avvio = False

def verificaConnessione(conn):
    global avvio
    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                print("Connessione chiusa dal server\n")
                break

            if data == "La partita inizia!":
                print("Il gioco sta iniziando...\n")
                avvio = True
                break

            print(f"{data}\n")

        except:
            break

        try:
            conn.sendall(b"Connesso")
        except:
            break



cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connettendo al server...\n")

    try:
        cSocket.connect(("localhost", 1234))
        break
    except Exception as e:
        print(f"Errore: {e}  Attendi per riprovare...\n")
        time.sleep(5)

    print("In attesa che il server avvii la partita...\n")
    verificaConnessione(cSocket)

    # Numero giocatori
    n = int(cSocket.recv(1024).decode())
    print(f"Numero giocatori: {n}\n")

    # --- CICLO DI GIOCO ---
    while True:
        try:
            msg = cSocket.recv(4096).decode()
            if not msg:
                break

            print(msg)

            if "Mano:" in msg:
                mano = msg.split("Mano:")[1].strip().split(",")

                while True:
                    carta = input("Scegli una carta da giocare: ").strip().upper()
                    if carta in mano:
                        break
                    print("Carta non valida.")

                cSocket.sendall(carta.encode())

        except Exception as e:
            print(f"Errore: {e}")
            break

    cSocket.close()
    break

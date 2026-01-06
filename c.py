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

        except Exception as e:
            print(f"Errore durante la comunicazione: {e}\n")
            break

        try:
            conn.sendall(b"Connesso")
        except Exception as e:
            print(f"Errore durante la comunicazione: {e}\n")
            break


def main():
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        global avvio
        avvio = False

        while not avvio:
            print("Connettendo al server...\n")
            try:
                cSocket.connect(("localhost", 1234))
            except Exception as e:
                print(f"Errore: {e}  Attendi per riprovare...\n")
                time.sleep(5)
                continue

            print("In attesa che il server avvii la partita...\n")
            verificaConnessione(cSocket)

        # Ricevo numero giocatori
        n = int(cSocket.recv(1024).decode())
        print(f"Numero giocatori: {n}\n")

        # Ricevo mano iniziale + briscola
        mano_briscola = cSocket.recv(1024).decode()
        print(mano_briscola)

        # Ciclo di gioco
        while True:
            try:
                msg = cSocket.recv(1024).decode()
                if not msg:
                    print("Connessione chiusa dal server")
                    break

                parti = msg.split(":", 1)

                comando = parti[0]
                contenuto = parti[1] if len(parti) > 1 else ""

                if comando == "Tavolo":
                    print(f"Tavolo: {contenuto}\n")

                elif comando == "Your_turn":
                    print(f"La tua mano: {contenuto}")
                    carta = ""
                    mano = contenuto.split(",")
                    while True:
                        carta = input("È il tuo turno, scegli una carta da giocare: ").strip()
                        if carta in mano:
                            break
                        print("Carta non valida, riprova.")
                    cSocket.sendall(carta.encode())

                elif comando == "Fine_turno":
                    print(f"Prende le carte in tavolo {contenuto}, che ha vinto il turno\n")

                elif comando == "Pesca":
                    print(f"Hai pescato una carta, la tua mano è: {contenuto}\n")

                else:
                    print(f"Messaggio dal server: {msg}")

            except Exception as e:
                print(f"Errore durante la comunicazione: {e}\n")
                break

        cSocket.close()
        break


if __name__ == "__main__":
    main()

import socket
import time
#VARIABILI GLOBALI--------------------------------------------

avvio = False

# FUNZIONI-----------------------------------------------------

def verificaConnessione(conn):
        while True:
            try:
                data = cSocket.recv(1024).decode().strip()
                if not data:
                    print("Connessione chiusa dal server\n")
                    break
                if data == "La partita inizia!":
                    print("il gioco sta iniziando\n")
                    avvio = True
                    break
                print(f"{data}\n")
                
            except Exception as e:
                print(f"Errore durante la comunicazione: {e}\n")
                break
            try:
                cSocket.sendall(b"Connesso")
            except Exception as e:
                print(f"Errore durante la comunicazione: {e}\n")
                break

# MAIN---------------------------------------------------------

cSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    avvio = False

    while avvio == False:

        print("connettendo al server...\n")
        try:

            cSocket.connect(("localhost", 1234))
            
        except Exception as e:
            print(f"Impossibile connettersi al server: {e}\n")
            time.sleep(20)


        print("In attesa che il server avvii la partita...\n")

        verificaConnessione(cSocket)



    #NO ANCORA GESTITO SUL SERVER(COMUNICAZIONE NUMERO GIOCATORI)
    n=int(cSocket.recv(1024).decode())
    print("Numero giocatori: ", n)
    nGiocatori=n

    #NON ANCORA GESTITA SUL SERVER(INVIO DELLA MANO AI GIOCTORI)
    mano_briscola=cSocket.recv(1024)#includere nel messaggio del server "ecco la tua mano: "
    print(mano_briscola.decode())#e anche la briscola

    #DA GESTIRE L'INVIO DELLA MANO---INVIAMO SEMPRE LA MANO COMPLETA, da fare
    while True:
        #getsione turno dal ricevimento della mano, ovvero stampa tavolo e giocata carte
        msg=cSocket.recv(1024)
        parti=msg.split(":")
        match parti[0]:
            case "Tavolo":
                print("Tavolo: "+parti[1])
            case "Your_turn":
                print("la tua mano: "+parti[1])
                carta=input("E' il tuo turno, scegli una carta da giocare...")
                cSocket.sendall(carta)
            case "Fine_turno":
                print("Prende le carte in tavolo "+parti[1]+", che ha vinto il turno")
            case "Pesca":
                print("Hai pescato una carta, la tua mano e: "+parti[1])


    #DA GESTIRE ANCORA SUL SERVER(oltre a quello gia scritto):

        #-Stabilire il vincitore della partita, e comunicarlo
        #-Attesa(lo sta facendo morgan)
        #-Passaggio da una partita finita a una nuova
        #altro??







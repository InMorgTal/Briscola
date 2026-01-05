import socket

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
                cSocket.sendall(b"In attesa...")
            except:
                print(f"Errore durante la comunicazione: {e}\n")
                break

# MAIN---------------------------------------------------------

cSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    avvio = False

    while avvio == False:

        print("connettendo al server...\n")

        cSocket.connect(("localhost", 1234))

        print("In attesa che il server avvii la partita...\n")
    
        verificaConnessione(cSocket)



    #NO ANCORA GESTITO SUL SERVER(COMUNICAZIONE NUMERO GIOCATORI)
    n=cSocket.recv(1024)
    print("Numero giocatori: ", n.decode())
    nGiocatori=int(n.decode())

    #NON ANCORA GESTITA SUL SERVER(INVIO DELLA MANO AI GIOCTORI)
    mano=cSocket.recv(1024)#includere nel messaggio del server "ecco la tua mano: "
    print(mano.decode())

    #NON ANCORA GESTITO SUL SERVER (INVIO DELLA BRISCOLA)
    briscola=cSocket.recv(1024)#includere nel messaggio del server "briscola: "
    print(briscola.decode())


    #DA GESTIRE L'INVIO DELLA MANO---INVIAMO SEMPRE LA MANO COMPLETA, da fare
    while True:
        #getsione turno dal ricevimento della mano, ovvero stampa tavolo e giocata carte
        msg=cSocket.recv(1024)
        parti=msg.split(":")

        if parti[0]=="Tavolo":
            print("Tavolo: "+parti[1])
        elif parti[0]=="Your_turn":
            print("la tua mano: "+parti[1])
            carta=input("E' il tuo turno, scegli una carta da giocare...")
            cSocket.sendall(carta)
        elif parti[0]=="Fine_turno":
            print("Prende le carte in tavolo "+parti[1]+", che ha vinto il turno")



    #DA GESTIRE ANCORA SUL SERVER(oltre a quello gia scritto):

        #-Stabilire il vincitore della partita, e comunicarlo
        #-Attesa(lo sta facendo morgan)
        #-Passaggio da una partita finita a una nuova
        #altro??






'''
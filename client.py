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
                if data == "Start":
                    print("il gioco sta iniziando\n")
                    avvio = True
                    break
                print(f"{data}\n")
                cSocket.sendall(b"Pong\n")
            except Exception as e:
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


    #DA GESTIRE L'INVIO DELLA MANO---INVIAMO SEMPRE LA MANO COMPLETA,
    while True:
        #Gestire le carte del tavolo sul server per far capire all'utente chi le ha giocate 
        tavolo=cSocket.recv(1024)#includere nel messaggio del server "Tavolo: "
        print(tavolo.decode())
        
        #ricevo il messaggio per fare una scelta
        msg=cSocket.recv(1024)
        print(msg.decode())
        #Invio la scelta al server
        scelta=input()
        cSocket.sendall(b"",scelta)
        
        #Da gestire: stampa del tavolo dopo che ogni giocatore ha giocato la propria carta
        for i in range (nGiocatori-1):
            tavolofineturno=cSocket.recv(1024)
            print(tavolo.decode())

        #Gestire stampa per comunicare il vincitore 
        #forna: io farei stampare anche quali carte si aggiungono alla pila del vincitore
        #volendo possiamo non fare la stampa del tavolo a fine turno e fare solo la stampa delle carte prese dal vincitore(e il vincitore)
        vincitoreTurno=cSocket.recv(1024)
        print(vincitoreTurno.decode())


    #DA GESTIRE ANCORA SUL SERVER(oltre a quello gia scritto):

        #-Stabilire il vincitore della partita, e comunicarlo
        #-Attesa(lo sta facendo morgan)
        #-Passaggio da una partita finita a una nuova
        #altro??






'''
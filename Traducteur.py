#-*-coding:UTF-8-*-

#███████████████████████████████Initialisation█████████████████████████████████#
from evdev import InputDevice, categorize, ecodes #Librairie pour entrée Manette
import RPi.GPIO as GPIO
import socket #communication en réseau
import threading
import time
import I2C_LCD_driver   #Ecran LCD 1602
#Traducteur sur RPi 3
def InitLCD():
    global lcd
    lcd = I2C_LCD_driver.lcd()
    lcd.lcd_display_string("Initialisé",1,2)
    lcd.lcd_display_string("Pret à afficher",2)
#███████████████████████████████Gestion Manette█████████████████████████████████#
##### KeyMapping Manette #################################################
A_BTN = 304         #Bouton A est au code 304 sur event.code
B_BTN = 305         #Bouton B code 305, ect
X_BTN = 307         #Bouton X
Y_BTN = 308         #Bouton Y
LB_BTN = 310        #Bouton LB, arriere haut gauche
RB_BTN = 311        #Bouton RB, arriere haut droit
SELECT_BTN = 314    #Bouton Select
START_BTN = 315     #Bouton Start
LS_BTN = 317        #Bouton joystick gauche
RS_BTN = 318        #Bouton joystick droit
GAMESIR_BTN = 316   #Bouton central, marqué "g" à led bleu
JOY_R_X = 3         #Axe x du joystick droit
JOY_R_Y = 4         #Axe y du joystick droit
JOY_L_X = 0         #Axe x du joystick gauche
JOY_L_Y = 1         #Axe y du joystick gauche
JOY_RT = 5          #Axe RT
JOY_LT = 2          #Axe LT
##########################################################################
def DetectionManette():
    global Manette
    try:
        Manette = InputDevice('/dev/input/event0')	#là ou est branchée la manette
        print ("Manette connectée au port 0")
    except:
        try:
            Manette = InputDevice('/dev/input/event1')
            print("Manette connectée au port 1")
        except:
            try:
                Manette = InputDevice('/dev/input/event2')
                prin ("Manette connectée au port 2")
            except:
                print ("Pas de manette reconnue")

def CommandeManette(client):  #Reception et traitement des infos de la manette
    G=D=C=Av=Ar=N=0
    for event in Manette.read_loop():
        if event.code == JOY_RT and 10 < event.value < 110 and Av != 1 and Ar == 0:
            print ("Avant 30 1")
            Envoi = ("avant/30/1")  #Avant / vitesse 30% / vitesse n°1
            client.send(Envoi.encode('UTF-8'))
            Av=1
            Ar=N=0

        if event.code == JOY_RT and 110 < event.value < 190 and Av != 2 and Ar == 0:
            print ("Avant 60 2")
            Envoi = ("avant/60/2")
            client.send(Envoi.encode('UTF-8'))
            Av=2
            Ar=N=0

        if event.code == JOY_RT and event.value >= 190 and Av != 3 and Ar == 0:
            print ("Avant 90 3")
            Envoi = ("avant/90/3")
            client.send(Envoi.encode('UTF-8'))
            Av=3
            Ar=N=0
        elif event.code == JOY_LT and 10 < event.value < 190 and Ar != 1 and Av == 0:
            print ("Arriere 25 1")
            Envoi = ("arriere/25/1")
            client.send(Envoi.encode('UTF-8'))
            Ar=1
            Av=N=0
        elif event.code == JOY_LT and event.value >= 190 and Ar != 2 and Av == 0:
            print ("Arriere 50 2")
            Envoi = ("arriere/50/2")
            client.send(Envoi.encode('UTF-8'))
            Ar=2
            Av=N=0

        elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N == 0:
            print ("Neutre")
            Envoi = ("neutre")   #Pas Av, pas Ar, juste neutre
            N=1
            Av=Ar=0

        if event.code == JOY_L_X  and event.value >= 1000 and D == 0:
            print ("Droite")
            Envoi = ("droite")
            client.send(Envoi.encode('UTF-8'))
            D=1
            G=C=0

        elif event.code == JOY_L_X and event.value <= -1000 and G == 0:
            print ("Gauche")
            Envoi = ("gauche")
            client.send(Envoi.encode('UTF-8'))
            G=1
            D=C=0

        elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
            print ("Centre")
            Envoi = ("centre")
            client.send(Envoi.encode('UTF-8'))
            C=1
            G=D=0

        if Serveur.STOP:
            print ("Arret de la commande Manette")
            break

        else:
            pass
        #check arret du thread lors de la deconnexion client


#███████████████████████████Gestion serveur socket█████████████████████████████#

class GestionSocket():

    def __init__(self):
        self.serveur = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
        Serveur.serveur.setblocking(0)
        self.NomServeur = ("Pi 3B+")
        self.Host = "10.1.1.15"
        self.Port = 6789
        self.ListeClients = []
        self.ListeNomClients = []
        self.ListeAddrClients = []
        self.STOP = 0
        print ("Classe socket __init__ OK.")

    def ArretServeur(self): #Deconecte les clients et stoppe le serveur
        for i in range(len(self.ListeClients)):
            print ("Fermeture de la connexion avec", self.ListeNomClients[0])
            Envoi = ("!leave")
            self.ListeClients[0].send(Envoi.encode("UTF-8"))
            time.sleep(0.5)
            self.ListeClients[0].close()
            del self.ListeClients[0]
            del self.ListeNomClients[0]
            del self.ListeAddrClients[0]
        self.serveur.close()
        print ("Serveur Fermé.")

    def Launch(self): #Lance l'écoute du serveur
        try:
            self.serveur.bind((self.Host,self.Port))
            self.serveur.listen(5)
            lcd.lcd_clear()
            lcd.lcd_display_string("Serveur Lancé",1,1)
            ThreadServeurJoin.start()
            
        except:
            print ("Impossible d'heberger le serveur sur {}:{}".format(self.Host,self.Port))
            lcd.lcd_clear()
            lcd.lcd_display_string("Host {}".format(self.Host),1)
            lcd.lcd_display_string("Impossible",2)
            self.ArretServeur()

    def Join(self): #Accepte la connexion d'un client
        while True:
            try:
                client, AdresseClient = serveur.accept()
                self.ListeAddrClients.append(AdresseClient)
                self.ListeClients.appent(client)
                ThreadGestionClients = threading.Thread(target = self.GestionClients, args = (client,AdresseClient))
                ThreadGestionClients.start()
                ThreadManette = threading.Thread(target = CommandeManette, args = client)
                ThreadManette.start()
            except:
                pass
            if self.STOP:
                print ("Arret thread 'Join'")
                break

            else:
                time.sleep(0.1)

    def GestionClients(self,client,AdresseClient):  #Gestion individuelle des clients

        while True:
            Erreur = 0
            NomClient = client.recv(1024)
            if not NomClient:
                print ("Nom du client non reçu")
                time.sleep(0.5)
            else:
                print (NomClient,"s'est connecté depuis", AdresseClient)
                client.send(self.NomServeur.encode("UTF-8"))
                self.ListeNomClients.append(NomClient)
                break

        while True:
            data = client.recv(1024)
            Recu = data.decode("UTF-8")
            CheckCMD = Recu.startswith("!",0,2)

            if not Recu:
                print ("Erreur de reception")
                Erreur += 1
            if Erreur == 10:
                print (AdresseClient, "deconnecté. \nTrop d'erreurs de reception")
                client.close()
                break

            elif CheckCMD:

                if Recu.lower() == ("!leaveok"):    #Pour def d'arret, check pour y definir une variable pour eviter une reponse
                    break
                elif Recu.lower() == ("!leave"):
                    print ("Deconnexion de", NomClient)
                    Envoi = ("!leaveok")
                    client.send(Envoi.encode("UTF-8"))
                    client.close()
                    print (NomClient, "Deconnecté")
                    self.ListeAddrClients.remove(AdresseClient)
                    self.ListeClients.remove(client)
                    self.ListeNomClients.remove(NomClient)
                else:
                    self.TraitementCMDclient(Recu,NomClient)
            else:
                self.TraitementRecuClients(Recu,NomClient)

    def TraitementCMDclient(self,Recu,NomClient):
        if Recu == ("!"):
            pass
        else:
            print ("Commande '{}' de {} non reconnue".format(Recu,NomClient))
    
    def TraitementRecuClients(self,Recu,NomClient):
        print ("Reception non traitée:")
        print (Recu)

# Serveur = GestionSocket()   #defini la classe, (et appelle Srv.__init__)

#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Réception des  données▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒#
def ReceptionProgPrincipal(datapr):
    pass

#████████████████████████████████████RPI███████████████████████████████████████#


#██████████████████████████████████Arduino█████████████████████████████████████#

print ("Carabistouille.")

#████████████████████████████Execution du programme████████████████████████████#
ListeInit = []
while True:
    Saisie = input ("> ")
    if Saisie.lower() == ("init"):
        if not ("LCD") in ListeInit:
            try:
                InitLCD()
                print ("Init LCD OK.")
                ListeInit.append("LCD")
            except:
                print ("Impossible d'initialiser l'ecran LCD")
        else:
            print ("LCD deja initialisé")

        if not ("Socket") in ListeInit:
            try:
                Serveur = GestionSocket()
                print ("Init Serveur OK.")
                ListeInit.append("Socket")
            except:
                print ("Impossible d'initialiser le serveur")
        else:
            print ("Socket deja initialisé")
            
    elif Saisie.lower() == ("start"):
        try:
            Serveur.Launch()
        except:
            print ("Erreur au lancement du serveur (Serveur.Launch)")

    elif Saisie == ("stop"):
        Serveur.ArretServeur()

    elif Saisie.lower() == ("gamepad") or Saisie.lower() == ("manette"):
        DetectionManette()

    elif Saisie.lower() == ("exit"):
        break
    elif Saisie.lower() == ("help"):
        print ("##################################################")
        print ("### init     Lance une initialisation generale ###")
        print ("### gamepad  Lance une detection de la manette ###")
        print ("### start    lance le serveur (Thread Launch)  ###")
        print ("### stop     Stoppe le serveur                 ###")
        print ("### exit     Quitte le programme               ###")
        print ("##################################################")

    else:
        print ("Commande non reconnue.")
exit()
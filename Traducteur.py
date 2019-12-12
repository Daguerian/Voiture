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

#███████████████████████████Gestion serveur socket█████████████████████████████#

class GestionSocket():

    def __init__(self):
        self.serveur = socket.socket(socket.AF_NET, socket.SOCK_STREAM)
        serveur.setblocking(0)
        sef.NomServeur = ("Pi 3B+")
        self.Host = "10.1.1.15"
        self.Port = 6789
        self.ListeClients = []
        self.ListeNomClients = []
        self.ListeAddrClients = []
        # self.STOP = 0
        print ("Classe socket __init__ OK.")

    def ArretServeur(self): #Deconecte les clients et stoppe le serveur
        for i in range(len(ListeClients)):
            print ("Fermeture de la connexion avec", ListeNomClients[0])
            self.Envoi = ("!leave")
            self.ListeClients[0].send(self.Envoi.encode("UTF-8"))
            time.sleep(0.5)
            ListeClients[0].close()
            del ListeClients[0]
            del ListeNomClients[0]
            del ListeAddrClients[0]
        self.serveur.close()
        print ("Serveur Fermé.")

    def Join(self): #Lance l'écoute du serveur
        try:
            self.serveur.bind((self.Host,self.Port))
            self.serveur.listen(5)
            lcd.lcd_clear()
            lcd.lcd_display_string("Serveur Lancé",1,1)
        except:
            print ("Impossible d'heberger le serveur sur {}:{}".format(self.Host,self.Port))
            lcd.lcd_clear()
            lcd.lcd_display_string("Host {}".format(Host),1)
            lcd.lcd_display_string("Impossible",2)
            self.ArretServeur()

        while True:
            try:
                client, AdresseClient = serveur.accept()
                ListeAddrClients.append(AdresseClient)
                ListeClients.appent(client)
                ThreadGestionClients = threading.Thread(target = self.GestionClients, args = client,AdresseClient)
                ThreadGestionClients.start()

            except:
                pass
            if self.STOP:
                break
                print ("Arret thread 'Join'")

            else:
                time.sleep(0.1)

    def GestionClients(client,AdresseClient,self):  #Gestion individuelle des clients
        while True:
            while True:
                NomClient = client.recv(1024)
                if NomClient in ListeNomClients:
                    Envoi = ("!name-already-used")
                    client.send(Envoi.encode("UTF-8"))

                else:
                    print (NomClient,"s'est connecté depuis", AdresseClient)
                    client.send(self.NomServeur.encode("UTF-8"))
                    self.ListeNomClients.append(NomClient)
                    break

        while True:
            data = client.recv(1024)
            Recu = data.decode("UTF-8")
            x = 0
            if not Recu:
                print ("Erreur de reception")
                x += 1

            if x == 10:
                print (AdresseClient, "deconnecté. \nTrop d'erreurs de reception")
                client.close()

            CheckCMD = Recu.startswith("!",0,2)
            if CheckCMD:

                if Recu.lower() == ("!leaveok"):
                    break
                else:
                    print ("Commande {} de {} non reconnue".foramt(Recu,NomClient))

            else:
                TraitementRecuClients()


Serveur = GestionSocket()   #defini la classe, (et appelle Srv.__init__)
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Réception des  données▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒#
def ReceptionProgPrincipal(datapr):
    pass

#████████████████████████████████████RPI███████████████████████████████████████#
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
            Envoi = ("avant/30/1")  #Avant / vitesse 30% / vitesse n°1
            client.send(Envoi.encode('UTF-8'))
            Av=1
            Ar=N=0

        if event.code == JOY_RT and 110 < event.value < 190 and Av != 2 and Ar == 0:
            Envoi = ("avant/60/2")
            client.send(Envoi.encode('UTF-8'))
            Av=2
            Ar=N=0

        if event.code == JOY_RT and event.value >= 190 and Av != 3 and Ar == 0:
            Envoi = ("avant/90/3")
            client.send(Envoi.encode('UTF-8'))
            Av=3
            Ar=N=0
        elif event.code == JOY_LT and 10 < event.value < 190 and Ar != 1 and Av == 0:
            Envoi = ("arriere/25/1")
            client.send(Envoi.encode('UTF-8'))
            Ar=1
            Av=N=0
        elif event.code == JOY_LT and event.value >= 190 and Ar != 2 and Av == 0:
            Envoi = ("arriere/50/2")
            client.send(Envoi.encode('UTF-8'))
            Ar=2
            Av=N=0

        elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N == 0:
            Envoi = ("neutre")   #Pas Av, pas Ar, juste neutre
            N=1
            Av=Ar=0

        if event.code == JOY_L_X  and event.value >= 1000 and D == 0:
            Envoi = ("droite")
            client.send(Envoi.encode('UTF-8'))
            D=1
            G=C=0

        elif event.code == JOY_L_X and event.value <= -1000 and G == 0:
            Envoi = ("gauche")
            client.send(Envoi.encode('UTF-8'))
            G=1
            D=C=0

        elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
            Envoi = ("centre")
            client.send(Envoi.encode('UTF-8'))
            C=1
            G=D=0

        if STOP:
            print ("Arret de la commande Manette")
            break
ThreadManette = threading.Thread(target=CommandeManette,args=client)
#██████████████████████████████████Arduino█████████████████████████████████████#

print ("Carabistouille.")

#████████████████████████████Execution du programme████████████████████████████#
# while True:
#     ReceptionProgPrincipale(Donnees)

# ThreadServeurJoin.start()   #Gestion des join serveur
# DetectionManette()
while True:
    Saisie = input ("> ")
    if Saisie.lower() == ("init"):
        try:
            InitLCD()
            print ("Init LCD OK.")
        except:
            print ("Impossible d'initialiser l'ecran LCD")
        try:
            Init_Serveur()
            print ("Init Serveur OK.")
        except:
            print ("Impossible d'initialiser le serveur")
    elif Saisie.lower() == ("start"):
        try:
            ThreadServeurJoin.start()
            ThreadManette.start()
        except:
            print ("Erreur")
    elif Saisie == ("stop"):
        ArretServeur()
    elif Saisie == ("lcd"):
        InitLCD()
    elif Saisie.lower() == ("gamepad"):
        DetectionManette()
    elif Saisie.lower() == ("help"):
        print ("##################################################")
        print ("### init     Lance une initialisation generale ###")
        print ("### start    lance le serveur (Thread Join)    ###")
        print ("### stop     Stoppe le serveur                 ###")
        print ("### exit     Quitte le programme               ###")
        print ("##################################################")

    else:
        print ("Commande non reconnue.")

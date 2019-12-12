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
def Init_Serveur():
    global serveur,NomServeur,STOP,Host,Port,ListeAddrClients,ListeClients,ListeNomClients
    serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ouverture du socket
    serveur.setblocking(0) #socket serveur non bloquant, exemple serveur.accept
    NomServeur = "Tr Pi 3B+"
    STOP = 0
    Host = "10.1.1.15"
    Port = 6789
    ListeAddrClients = []   #Listes des "AdresseClient"
    ListeClients = []       #Liste "client"
    ListeNomClients = []    #Liste noms clients, etablis à la connexion

def ArretServeur(): #Deconnecte les clients & ferme le socket
    global STOP
    STOP = True #Variable pour l'arret du thread Join() et CommandeManette()
    for i in range(len(ListeClients)):  #Deconnecte les clients un par un
        print ("Fermeture de la connexion avec", ListeNomClients[0])
        t = ("!leave")
        ListeClients[0].send(t.encode("UTF-8"))
        time.sleep(0.5) #delais d'attente de reponse pour l'arret du Thread client associé
        ListeClients[0].close()
        del ListeClients[0]
        del ListeAddrClients[0]
        del ListeNomClients[0]

    serveur.close() #Fermeture du socket serveur
        #Update suite

def InitLCD():
    global lcd
    lcd = I2C_LCD_driver.lcd()

def Join():
	try:
		serveur.bind((Host, Port))
		serveur.listen(5) #Ecoute jusqu'a 5 connexions
		lcd.lcd_display_string("Serveur lancé",1)
	except:
		print ("Impossible d'heberger le serveur sur {}:{}".format(Host,Port))
		lcd.lcd_display_string("Hebergement",1,2)
		lcd.lcd_display_string("Impossible",2,3)
		ArretServeur()

	while True:		#Boucle d'attente de nouvelle Connexion
		try:
			client, AdresseClient = serveur.accept() #Accepte la connexion, non bloquant
			ListeAddrClients.append(AdresseClient)   #Ajoute l'adresse à la liste
			ListeClients.append(client)              #Ajoute le client à la liste
			ThreadGestionClients = threading.Thread(target=GestionClients, args = (client, AdresseClient))
			ThreadGestionClients.start() #Lance le Thread de gestion du client
			ThreadManette.start(client)
		except: # devrait ignorer une eventuelle erreur
			pass
		if STOP:   #Arret du thread en cas d'arret
			break
		else:
			time.sleep(0.1)
ThreadServeurJoin = threading.Thread(target = Join)

def GestionClients(client, AdresseClient):	#à renommer "Gestion clients"
	global NomClient
	x = 0  #Gestion des erreurs de reception
	while True:		#Boucle verification de nom deja utilisé
		NomClient = client.recv(1024).decode('UTF-8')
		if NomClient in ListeNomClients:
			t = ('!name-already-used') #t est une variable temporaire
			client.send(t.encode('UTF-8'))
		else:
			print (NomClient, "s'est connecté depuis",AdresseClient)
			client.send(NomServeur.encode('UTF-8'))
			ListeNomClients.append(NomClient)
			break

	while True:
		data = client.recv(1024)
		Recu = data.decode('UTF-8')

		if not Recu:
			print('Erreur de reception')
			x += 1

		if x == 10:
			print (AdresseClient, "déconnecté. \nTrop d'erreurs de reception")
			client.close()
		CheckCMD = Recu.startswith('!',0,2)
		if CheckCMD:

			if Recu.lower() == ('!leave'): #Demande de deconnexion depuis le client
				t = ('!leaveOK')
				client.send(t.encode('UTF-8')) #Envoi de confirmation de deconnexion
				print(AdresseClient,'deconecté') #sendall plus tard
				ListeAddrClients.remove(AdresseClient)  #Remove le client des listes
				ListeNomClients.remove(NomClient)
				ListeClients.remove(client)
				break
			if Recu.lower() == ('!leaveok'): #confirmation deconnexion du client par le serveur
				break
			# if Recu.lower() == ('!listeusers'):
			# 	t = ('Liste des clients connectés:', ListeNomClients)
			# 	client.send(t.encode('UTF-8'))
			# 	print ('Liste des utilisateur envoyé à ', NomClient)

			else:
				print ("Commande '{}' de '{}' non reconnue".format(Recu,NomClient))
		else:
			TraitementRecuClients()

def TraitementRecuClients():
    pass
            #Update
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

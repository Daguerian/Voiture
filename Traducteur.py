#███████████████████████████████Initialisation█████████████████████████████████#
from evdev import InputDevice, categorize, ecodes #Librairie pour entrée Manette
import RPi.GPIO as GPIO
import socket #communication en réseau
import threading
import time
#Traducteur sur RPi 3
#███████████████████████████Gestion serveur socket█████████████████████████████#
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ouverture du socket
serveur.setblocking(0) #socket serveur non bloquant, exemple serveur.accept
NomServeur = "Tr Pi 3B+"
STOP = 0

ListeAddrClients = []   #Listes des "AdresseClient"
ListeClients = []   #Liste "client"
ListeNomsClients = []   #Liste noms clients, etablis à la connexion

def ArretServeur(): #Deconnecte les clients & ferme le socket
    STOP = True #Variable pour l'arret du thread Join() et CommandeManette()
    for i in range(len(ListeClients)):  #Deconnecte les clients un par un
        print ("Fermeture de la connexion avec", ListeNomClients[0])
        t = ("!leave")
        ListeClients.send(t.encode("UTF-8"))
        time.sleep(0.5) #delais d'attente de reponse pour l'arret du Thread client associé
        ListeClients[0].close()
        del ListeClients[0]
        del ListeAddrClients[0]
        del ListeNomClients[0]

    serveur.close() #Fermeture du socket serveur
        #Update suite

def Join():
	serveur.listen(5) #Ecoute jusqu'a 5 connexions
	while True:		#Boucle d'attente de nouvelle Connexion
		try:
			client, AdresseClient = serveur.accept() #Accepte la connexion, non bloquant
			ListeAddrClients.append(AdresseClient)   #Ajoute l'adresse à la liste
			ListeClients.append(client)              #Ajoute le client à la liste
			ThreadGestionClients = threading.Thread(target=GestionClients, args = (client, AdresseClient))
			ThreadGestionClients.start() #Lance le Thread de gestion du client
		except: # devrait ignorer une eventuelle erreur
			pass
		if STOP in ArretServeur == True:   #Arret du thread en cas d'arret
			break
		else:
			time.sleep(0.1)
ThreadServeurJoin = threading.Thread(target = ArretServeur)

def GestionClients(client, AdresseClient):	#à renommer "Gestion clients"
	x = 0  #Gestion des erreurs de reception
	while True:		#Boucle verification de nom deja utilisé
		NomClient = client.recv(1024).decode('UTF-8')
		if NomClient in ListeNomClients:
			t = ('!name-already-used') #t est une variable temporaire
			client.send(t.encode('UTF-8'))
		else:
			print (NomClient, "s'est connecté depuis",AdresseClient)
			client.send(NomServeur.encode('UTF-8'))
			ListeNomsClients.append(NomClient)
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
				print ("Commande '{}' de '{}' non reconnue".format(recu,NomClient))
		else:
            TraitementRecuClients():
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
try:
    Manette = InputDevice('/dev/input/event0')	#là ou est branchée la manette
    Manette connectée au port 0
except:
    try:
        Manette = InputDevice('/dev/input/event1')
    except:
        try:
            Manette = InputDevice('/dev/input/event2')
    except:
        print ("Pas de manette reconnue")
def CommandeManette():  #Reception et traitement des infos de la manette
    for event in Manette.read_loop():
        if event.code == JOY_RT and 10 < event.value < 110 and Av != 1 and Ar == 0:
			Envoi = ("avant/30/1")  #Avant / vitesse 30% / vitesse n°1
			client.send(Envoi.encode('UTF-8'))

        if event.code == JOY_RT and 110 < event.value < 190 and Av != 2 and Ar == 0:
            Envoi = ("avant/60/2")
			client.send(Envoi.encode('UTF-8'))

        if event.code == JOY_RT and event.value >= 190 and Av != 3 and Ar == 0:
            Envoi = ("avant/90/3")
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_LT and 10 < event.value < 190 and Ar == 1 and Av == 0:
            Envoi = ("arriere/25/1")
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_LT and event.value >= 190 and Ar != 2 and Av == 0:
            Envoi = ("arriere/50/2")
			client.send(Envoi.encode('UTF-8'))

        elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N = 0:
            Envoi = ("neutre")   #Pas Av, pas Ar, juste neutre

        if event.code == JOY_L_X  and event.value >= 1000 and D = 0:
            Envoi = ("droite")
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_L_X and event.value <= -1000 and G = 0:
            Envoi = ("gauche")
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
            Envoi = ("centre")
			client.send(Envoi.encode('UTF-8'))
        if STOP:
            print ("Arret de la commande Manette")
            break

#██████████████████████████████████Arduino█████████████████████████████████████#

print ("Carabistouille.")

#████████████████████████████Execution du programme████████████████████████████#
while True:
    ReceptionProgPrincipale(Donnees)

ThreadServeurJoin.start()   #Gestion des join serveur

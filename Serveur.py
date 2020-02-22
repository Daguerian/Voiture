from evdev import InputDevice, categorize, ecodes
import socket
import threading
import time

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
PAD_X = 16			#Croix directionelle axe x
PAD_Y = 17			#Croix directionelle axe y
##########################################################################

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Manette = InputDevice('/dev/input/event0')	#là ou est branchée la manette

def init():
	GPIO.setmode(GPIO.BCM)
	#set un BP d'entrée pour activer/desactiver le debug
	#acces au text
def CommandList():	#Commandes de debug disponibles
	if Saisie.lower() == ('-help'):
		print ("## Help ##")
		print ("##		##")
	elif Saisie.lower() == (" "):
		pass

def CommandeManette():	# Voiture 1
	for event in Manette.read_loop():
		if event.code == JOY_RT and 10 < event.value < 110 and Av != 1 and Ar == 0:
			Envoi = ('Av1')
			client.send(Envoi.encode('UTF-8'))

        if event.code == JOY_RT and 110 < event.value < 190 and Av != 2 and Ar == 0:
            Envoi = 'Av2'
			client.send(Envoi.encode('UTF-8'))

        if event.code == JOY_RT and event.value >= 190 and Av != 3 and Ar == 0:
            Envoi = 'Av3'
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_LT and 10 < event.value < 190 and Ar == 1 and Av == 0:
            Envoi = 'Ar1'
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_LT and event.value >= 190 and Ar != 2 and Av == 0:
            Envoi = 'Ar2'
			client.send(Envoi.encode('UTF-8'))

        elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N = 0:
            ArretMoteur()

        if event.code == JOY_L_X  and event.value >= 1000 and D = 0:
            Envoi = 'Droite'
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_L_X and event.value <= -1000 and G = 0:
            Envoi = 'Gauche'
			client.send(Envoi.encode('UTF-8'))

        elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
            Envoi = 'Centre'
			client.send(Envoi.encode('UTF-8'))

        if event.code == GAMESIR_BTN and event.value == 1:
        	print ('ARRET PROG')
        	break

####  Start Prog ####
Host, Port = 'localhost', 6789
try:
	serveur.bind((Host, Port))	#Hebergement du serveur
except:
	print ("Impossible d'heberger le serveur sur {}:{}".format(Host,Port))
	exit()

print ("Serveur hebergé sur {}:{} \nNom de la machine: {}".format(Host,Port,socket.gethostname()))

print ("En attente de connexion...\n")

### attente de connexion du client
serveur.listen(3) #3 connexions maxi
client, AdresseClient = serveur.accept()
#Blocage tant que le client n'est pas connecté
ThreadReception = threading.Thread(target=Reception)

EnvoiNameServer = (socket.gethostname())			#Envoi Nom du serveur
client.send(EnvoiNameServer.encode('UTF-8'))

données = client.recv(1024)							#Reception Nom du client
NomClient = données.decode('UTF-8')
print (NomClient,'connecté')
ThreadReception.start()

while True:	#Activation debug

	Saisie = input('> ')

	# if Saisie.lower() == ('-arret'):
	# 	Stop()
	# 	break
	y = Saisie.startswith('-',0,2) #'-' entre 0 et 2, non inclus
	if y:
		CommandList()	#Action en fonction d'une demande syntaxée
		y = 0
	else:
		n = client.send(Saisie.encode('UTF-8'))
		if not n:
			print ('Erreur d\'envoi')
		else:
			print ('Envoyé.')

#████████████████████████████████████Arduino███████████████████████████████████#

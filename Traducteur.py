#███████████████████████████████Initialisation█████████████████████████████████#
from evdev import InputDevice, categorize, ecodes #Librairie pour entrée Manette
import socket #communication en réseau
import threading
import time
#Traducteur sur RPi 3
#███████████████████████████Gestion serveur socket█████████████████████████████#
#▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒Réception des  données▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒#
def ReceptionProgPrincipale(Donnees):
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
Manette = InputDevice('/dev/input/event0')	#là ou est branchée la manette
def CommandeManette():
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

#██████████████████████████████████Arduino█████████████████████████████████████#

#████████████████████████████Execution du programme████████████████████████████#
while True:
    ReceptionProgPrincipale(Donnees)

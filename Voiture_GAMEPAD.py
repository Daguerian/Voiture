#!/usr/bin/env python
#######################################
###           Version 0.3           ###
#######################################
# v0.1 : Servos Only, entrées boutons
# v0.2 : Ajout Moteur
# v0.3 : Ajout entrée Gamepad
#######################################


from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time
import threading
#import bluetooth

gamepad0 = InputDevice('/dev/input/event0')
gamepad1 = InputDevice('/dev/input/event1')
gamepad2 = InputDevice('/dev/input/event2')


GPIO.setmode(GPIO.BCM)
StopCommand = 0
End = 0

### Sortie pins BCM ###
SERVO = 26          #Sortie Servomoteur
in1 = 24            #Sortie controller avant moteur
in2 = 23            #Sortie controller arriere moteur
ena = 25            #Sortie controller vitesse moteur
LedRouge =
### KeyMapping ###
###  Manette   ###
A_BTN = 304         #Bouton A est au code 304 sur event.code
B_BTN = 305         #Bouton B code 305, defini materielement
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

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT) #Sortie Servo
pwm = GPIO.PWM(SERVO, 50)   # pwm au pin SERVO, fréquence de 50 Hz

################
#     defs     #>
################

#####  Initialisations  #####

def init_General():
    GPIO.setup(16,GPIO.OUT)  #Led rouge
    GPIO.setup(12,GPIO.OUT)  #Led verte

def init_Servo():
    C = 0  #Centre = 0, Centrage des roues = 0

    #Nothing ?


def Init_Moteur():
    GPIO.setup(in1,GPIO.OUT) #Sortie Controller, Pin avant moteur
    GPIO.output(in1,GPIO.LOW)
    GPIO.setup(in2,GPIO.OUT) #Sortie Controller, Pin arriere moteur
    GPIO.output(in2,GPIO.LOW)
    GPIO.setup(ena,GPIO.OUT) #Sortie Controller, Pin vitesse moteur
    p = GPIO.PWM(ena,1000)   #set default vitesse
    global N
    N = 0
####  Sorties Moteur / Servo  #####

def Droite():
    pwm.start(7.8)      #/!\ à re-set pour egalité gauche-droite
    print ('DROITE')
    time.sleep(0.15)    #Arret du servo sur sa position
    pwm.stop
    global C,D,G
    C = 0  #Centre, Roues centre
    D = 1  #Droite, Roues droite
    G = 0  #Gauche, Roues Gauche

def Gauche():
    pwm.start(6)        #/!\ à re-set pour egalité gauche-droite
    print ('GAUCHE')
    time.sleep(0.15)
    pwm.stop            #Arret du servo sur sa position
    global C,D,G
    C = 0
    D = 0
    G = 1

def Centre():
    pwm.start(6.8)
    print ('NONE')
    time.sleep(0.15)
    pwm.stop
    global C,D,G
    C = 1
    D = 0
    G = 0

def Avant(Vitesse):             #Marche avant en fonction de la vitesse en %
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Arriere')
    global Av,Ar,N
    Av = 1
    Ar = 0
    N = 0

def Arriere(Vitesse):           #Marche arriere en fonction de la vitesse en %
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Arriere')
    global Av,Ar,N
    Av = 0
    Ar = 1
    N = 0

def ArretMoteur()
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    print ('Stop Moteur')
    global Av,Ar,N
    Av = 0
    Ar = 0
    N = 1

#####  Commandes Arrets  #####

def Arret():
    print('--- ARRET ---')
    pwm.stop
    GPIO.cleanup()  #reset des Pins GPIO
    GPIO.output(in1,GPIO.LOW) #Arret du moteur
    GPIO.output(in1,GPIO.LOW) #(Vitesse inchangée, Rotation =  NONE)
    # + Arret des Threads
    global StopCommand
    StopCommand = 1   #"Commande Stop enclenchée" Plus tard, pour le thread des leds
    #break

def Restart(): #Demande de restart, declenché par GAMESIR_BTN
    global StopCommand
    Arret()
    print ('#############################')
    print ('# Redemarrer le programme ? #')
    print ('# Start: Oui | Select: Non  #')
    print ('#############################')

    for event in gamepad.read_loop():

        if event.code == START_BTN and event.value == 1:
                print ('Rechargement...')
                StopCommand = 0 #"Commande Stop desenclenchée" Plus tard, pour le threading des leds

        elif event.code == SELECT_BTN and event.value == 1:
            #Arret du reste
            print ('End.')
            End = 1

##### Leds / stats  #####

def LedStopCommand()    #Clignotement led rouge si StopCommand à été pressé
    GPIO.output(LedRouge,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LedRouge,GPIO.HIGH)
    time.sleep(0.5)

def CameraConnected()   #Led/info statut de connexion camera, if nbr FPS < 40: info probleme de transmission
    ##


##########################
#     Début du prog      #
##########################


#####  Demarrage, selection gamepad  #####

while True:
    print ('--- Selection controller ---')

    if InputDevice('/dev/input/event0') == True:
        gamepad = InputDevice('/dev/input/event0')
        print gamepad
        break

    elif InputDevice('/dev/input/event1') == True:
        gamepad = InputDevice('/dev/input/event1')
        print gamepad
        break

    else:
        print ('Controleur non détecté')
        print ('Redetection dans 3 secondes')
        time.sleep(3)

#####  Boucle Leds/stats  #####
        


#####  Boucle Arret/Restart prog  #####

while True

    if event.type in gamepad.read_loop() == ecodes.EV_KEY and event.code == GAMESIR_BTN and event.value == 1:
            Restart()

    elif

#####  Boucle Servo direction  #####
'''while End == 0:'''

init_Servo()
for event in gamepad.read_loop():

        if event.code == JOY_L_X  and event.value >= VALUE and event.value <VALUE and D = 0: #Gauche press, Droite
            Droite()

        elif GPIO.input(6) == True and GPIO.input(13) == False and G == 0:
           Gauche()

        elif GPIO.input(6) == True and GPIO.input(13) == True and C == 0:
           Centre()

        elif GPIO.input(5) == False:
            Arret()


#####  Boucle Moteur  #####

'''while End == 0:'''
init_Moteur()
for event in gamepad.read_loop():

    if event.code == JOY_RT and event.value >= 10 and event.value < 110 and Av == 0:
        Avant(25)  #Marche avant, Vitesse 1, 25%

    elif event.code == JOY_RT and event.value >= 110 and event.value < 190 and Av == 0:
        Avant(50)  #Marche avant, Vitesse 2, 50%

    elif event.code == JOY_RT and event.value >=190 and Ar == 0:
        Avant(75)  #Marche avant, Vitesse 3, 75%

    elif event.code == JOY_LT and event.value >= 10 and event.value < 190 and Ar == 0:
        Arriere(25) #Marche arriere, Vitesse 1, 25%

    elif event.code == JOY_LT and event.value >= 190 and Ar == 0:
        Arriere(50) #Marche arriere, Vitesse 2, 50%

    elif (event.code == JOY_LT and event.value < 10) or (event.code == JOY_RT and event.value < 10) and N = 0:
        ArretMoteur()



'''threading.Thread(target=CIBLE).start() #lance le threading
threading.Thread(target=CIBLE).start()'''

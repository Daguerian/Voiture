#!/usr/bin/env python
#######################################
###         The RC Project          ###
###           version 0.4           ###
#######################################
# v0.1 : Servos Only, entrées boutons #
# v0.2 : Ajout Moteur                 #
# v0.3 : Ajout Gamepad                #
# v0.4 : Ajout Threads                #
#######################################

from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time
import threading
#import bluetooth



### Sortie pins BCM ###
SERVO = 26          #Sortie Servomoteur
in1 = 24            #Sortie controller avant moteur
in2 = 25            #Sortie controller arriere moteur
ena = 23            #Sortie controller vitesse moteur
LedRouge = 12
#LedVerte = 
LedJaune = 16
#LedBleue = 
RGB_R = 13
RGB_G = 6
RGB_B = 5
Buzzer = 18
### KeyMapping ###
###  Manette   ###
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

StopCommand = False     #Demande d'arret
GPIO.setwarnings(False) # desactive les erreurs GPIOs
GPIO.setmode(GPIO.BCM)

################
#     defs     #
################

#####  Initialisations  #####

def init_General():
    GPIO.setup(LedRouge,GPIO.OUT)   #Led Rouge
    #GPIO.setup(LedVerte,GPIO.OUT)   #Led Verte
    #GPIO.setup(LedBleue,GPIO.OUT)   #Led Bleue
    GPIO.setup(LedJaune,GPIO.OUT)   #Led Jaune
    GPIO.setup(RGB_R,GPIO.OUT)      #Led RGB, pin Rouge
    GPIO.setup(RGB_G,GPIO.OUT)      #Led RGB, pin Vert
    GPIO.setup(RGB_B,GPIO.OUT)      #Led RGB, pin Bleu
    GPIO.setup(Buzzer,GPIO.OUT)     #Buzzer passif

def init_Servo():
    global C,D,G,pwm_servo
    GPIO.setup(SERVO, GPIO.OUT) #Sortie Servo
    pwm_servo = GPIO.PWM(SERVO, 50)   # pwm au pin SERVO, fréquence de 50 Hz
    C = 0  #Centre = 0, Centrage des roues = 0
    D = 0
    G = 0

def Init_Moteur():
    GPIO.setup(in1,GPIO.OUT) #Sortie Controller, Pin avant moteur
    GPIO.output(in1,GPIO.LOW)
    GPIO.setup(in2,GPIO.OUT) #Sortie Controller, Pin arriere moteur
    GPIO.output(in2,GPIO.LOW)
    GPIO.setup(ena,GPIO.OUT) #Sortie Controller, Pin vitesse moteur
    global N,p
    p = GPIO.PWM(ena,1000)   #set default vitesse ####### RECHECK LA FREQUENCE ########
    N = 0


####  Sorties Moteur / Servo  #####

def Droite():
    pwm_servo.start(7.8)      #/!\ à re-set pour egalité gauche-droite
    print ('DROITE')
    time.sleep(0.15)    #Arret du servo sur sa position
    pwm_servo.stop
    global C,D,G
    C = 0  #Centre, Roues centre
    D = 1  #Droite, Roues droite
    G = 0  #Gauche, Roues Gauche

def Gauche():
    pwm_servo.start(6)        #/!\ à re-set pour egalité gauche-droite
    print ('GAUCHE')
    time.sleep(0.15)
    pwm_servo.stop            #Arret du servo sur sa position
    global C,D,G
    C = 0
    D = 0
    G = 1

def Centre():
    pwm_servo.start(6.8)
    print ('NONE')
    time.sleep(0.15)
    pwm_servo.stop
    global C,D,G
    C = 1
    D = 0
    G = 0

def Avant(Vitesse, Mode):       #Marche avant en fonction de la vitesse en %
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Avant')
    global Av,Ar,N
    Av = (Mode)
    Ar = 0
    N = 0

def Arriere(Vitesse, Mode):     #Marche arriere en fonction de la vitesse en % et du mode de vitesse
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Arriere')
    global Av,Ar,N
    Av = 0
    Ar = (Mode)
    N = 0

def ArretMoteur():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    print ('Stop Moteur')
    global Av,Ar,N
    Av = 0
    Ar = 0
    N = 1

#####  Commandes Arrets  #####

def Arret():
    print('--- ARRET ---')
    Centre()                  #Recentrage des roues
    GPIO.output(in1,GPIO.LOW) #Arret du moteur
    GPIO.output(in1,GPIO.LOW) #(Vitesse inchangée, Rotation =  NONE)
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
            GPIO.cleanup()  #reset des Pins GPIO
            print ('End.')
            End = 1
            break

##### Leds / stats  #####

def LedStopCommand():    #Clignotement led rouge si StopCommand à été pressé, peut etre a Thread :shrug:
    while StopCommand = 1:
        GPIO.output(LedRouge,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LedRouge,GPIO.LOW)
        time.sleep(0.5)


##### target Thread #####

def THREAD_DIRECTION():

    init_Servo()
    while StopCommand == False:

        for event in gamepad.read_loop():

                if event.code == JOY_L_X  and event.value >= 1000 and D = 0:
                    Droite()

                elif event.code == JOY_L_X and event.value <= -1000 and G = 0:
                    Gauche()

                elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
                    Centre()

                elif StopCommand == False:
                    print ('Arret temporaire THREAD_MOTEUR')
                    break


def THREAD_MOTEUR():

    init_Moteur()
    while StopCommand == False:

        for event in gamepad.read_loop():

            if event.code == JOY_RT and 10 < event.value < 110 and Av != 1:
                Avant(25,1)  #Marche avant, Vitesse 1, 25%

            if event.code == JOY_RT and 110 < event.value < 190 and Av != 2:
                Avant(50,2)  #Marche avant, Vitesse 2, 50%

            if event.code == JOY_RT and event.value >= 190 and Av != 3:
                Avant(75,3)  #Marche avant, Vitesse 3, 75%

            elif event.code == JOY_LT and 10 < event.value < 190 and Ar == 1:
                Arriere(25,1) #Marche arriere, Vitesse 1, 25%

            elif event.code == JOY_LT and event.value >= 190 and Ar != 2:
                Arriere(50,2) #Marche arriere, Vitesse 2, 50%

            elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N = 0:
                ArretMoteur()

            if StopCommand == True:
                print ('Arret temporaire THREAD_MOTEUR')
                break
  
def EclairagesLED():


##### Threads Name #####

Thread_Direction = threading.Thread(name = Direction, target = THREAD_DIRECTION, args = ())
Thread_Moteur = threading.Thread(name = Moteur, target = THREAD_MOTEUR, args = ())
#Thread_RGB = 
#Thread_Leds = 
#Thread_Web = 

##########################
#     Début du prog      #
##########################


#####   Demarrage   #####

print ('###  DEMARRAGE DU PROGRAMME   ### \n')

while True:
    
    print ('--- Selection automatique controller --- \n')
    time.sleep (0.5)
    print ('--- ... --- \n')


    if InputDevice('/dev/input/event0') == True:

        gamepad = InputDevice('/dev/input/event0')
        print ('--- Controller detecté ! ---')
        print ('--- {} --- \n'.format (gamepad))
        break


    elif InputDevice('/dev/input/event1') == True:

        gamepad = InputDevice('/dev/input/event1')
        print ('--- Controller detecté ! ---')
        print ('--- {} --- \n'.format (gamepad))
        break


    else:

        print ('Controleur non détecté')
        print ('Redetection dans 3 secondes')
        time.sleep(3)

### Lancement des Thread, apres selection du controller ###
Thread_Direction.start()
Thread_Moteur.start()
#Thread_RGB.start()
#Thread_Leds.start()
#Thread_Web.start()


### Detection commande d'arret ###
while True:
    if event.code == GAMESIR_BTN and event.value == 1 and StopCommand == False:
        StopCommand = True
        Reset_all()     #repasse les valeurs a 0, comme moteur a l'arret, roues droites, leds eteintes (sauf RGB en rouge)
        print ('--- Commande d\'arret ---\n')
        print ('--- Redemarrer | Arreter ---')
        print ('---   Start    |   GS    ---\n')

    elif event.code == START_BTN and event.value == 1 and StopCommand == True:
        StopCommand = False
        print ('--- Relancement... ---\n')

    elif event.code == SELECT_BTN and event.value == 1 and StopCommand == True:
        print ('--- ARRET DU PROGRAMME ---')
        Arret()
        #Envoi infos sur l'arret
        break

#############
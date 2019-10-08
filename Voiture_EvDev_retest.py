from evdev import InputDevice, categorize, ecodes
import RPi.GPIO as GPIO
import time
import threading
#import bluetooth



### Sortie pins BCM ###
Servo = 26          #Sortie Servomoteur
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

GPIO.setwarnings(False) # desactive les erreurs GPIOs
GPIO.setmode(GPIO.BCM)

pwm_servo = GPIO.PWM(Servo, 50)
pwm_moteur = GPIO.PWM(ena,1000)

def InitCapteurs():
	global StopCommand,Av,Ar,N,G,D,C
	StopCommand = False     #Demande d'arret
	Av = 0		#Moteur Avant
	Ar = 0		#Moteur Arriere
	N = 0		#Moteur Neutre, Arret moteur (roue libre)
	G = 0		#Direction Gauche
	D = 0		#Direction Droite
	C = 0		#Direction Centrée

def Droite():
	pwm_servo.start(8)
	print ('Droite')
	time.sleep(0.15)
	pwm_servo.stop 
	global G,D,C
	G = 0
	D = 1
	C = 0

def Gauche():
	pwm_servo.start(6)
	print ('Gauche')
	time.sleep(0.15)
	pwm_servo.stop
	global G,D,C
	G = 1
	D = 0
	C = 0

def Centre():
	pwm_servo.start(6.8)
	print ('Centre')
	time.sleep(0.15)
	pwm_servo.stop
	global G,D,C
	G = 0
	D = 0
	C = 1

def Avant(Vitesse, Mode)
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	pwm_moteur.ChangeDutyCycle(Vitesse)
	print ('Marche avant, {}e vitesse {}%'.format(Mode,Vitesse))
	global Av,Ar,N
	Av = (Mode)
	Ar = 0
	N = 0

def Arriere(Vitesse, Mode)
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	pwm_moteur.ChangeDutyCycle(Vitesse)
	print ('Marche Arriere, {}e vitesse {}%'.format(Mode,Vitesse))
	global Av,Ar,N
	Av = 0
	Ar = (Mode)
	N = 0

def ArretMoteur():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.LOW)
	print ('Arret Moteur')
	global Av,Ar,N
	Av = 0
	Ar = 0
	N = 1

def Frein():
	GPIO.output(in1,GPIO.HIGH)
	GPOI.output(in2,GPIO.HIGH)
	print ('FREINAGE')

def Controle():

	while StopCommand == False:

		for event in gamepad.read_loop():
			

			if event.code == JOY_RT and 10 < event.value < 110 and Av != 1 and Ar == 0:
                Avant(25,1)  #Marche avant, Vitesse 1, 25%

            if event.code == JOY_RT and 110 < event.value < 190 and Av != 2 and Ar == 0:
                Avant(50,2)  #Marche avant, Vitesse 2, 50%

            if event.code == JOY_RT and event.value >= 190 and Av != 3 and Ar == 0:
                Avant(75,3)  #Marche avant, Vitesse 3, 75%

            elif event.code == JOY_LT and 10 < event.value < 190 and Ar == 1 and Av == 0:
                Arriere(25,1) #Marche arriere, Vitesse 1, 25%

            elif event.code == JOY_LT and event.value >= 190 and Ar != 2 and Av == 0:
                Arriere(50,2) #Marche arriere, Vitesse 2, 50%

            elif (event.code == JOY_LT or event.code == JOY_RT) and event.value < 10 and N = 0:
                ArretMoteur()


            if event.code == JOY_L_X  and event.value >= 1000 and D = 0:
                Droite()

            elif event.code == JOY_L_X and event.value <= -1000 and G = 0:
                Gauche()

            elif event.code == JOY_L_X and -1000 < event.value < 1000 and C == 0:
                Centre()

            if event.code == GAMESIR_BTN and event.value == 1:
            	print ('ARRET PROG')
            	break
            	
    print ('ARRET COMPLET')
    break

#Thread_Controle = threading.Thread(name = none,target = Controle, args = none)





######################
##### Start Prog #####
######################

InitCapteurs()

print (gamepad '\n')

#Thread_Controle.start()

Controle()
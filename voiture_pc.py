import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
StopCommand = 0
End = 0

### Sortie pins BCM ###
SERVO = 26          #Sortie Servomoteur
in1 = 23            #Sortie controller avant moteur
in2 = 24            #Sortie controller arriere moteur
ena = 18            #Sortie controller vitesse moteur

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO, GPIO.OUT) #Sortie Servo
pwm = GPIO.PWM(SERVO, 50)   # pwm au pin SERVO, fréquence de 50 Hz


GPIO.setup(in1,GPIO.OUT) #Sortie Controller, Pin avant moteur
GPIO.output(in1,GPIO.LOW)
GPIO.setup(in2,GPIO.OUT) #Sortie Controller, Pin arriere moteur
GPIO.output(in2,GPIO.LOW)
GPIO.setup(ena,GPIO.OUT) #Sortie Controller, Pin vitesse moteur
p = GPIO.PWM(ena,1000)   #set default vitesse
N = 0

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
    p.start(0)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Avant')
    global Av,Ar,N
    Av = 1
    Ar = 0
    N = 0

def Arriere(Vitesse):           #Marche arriere en fonction de la vitesse en %
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    p.start(0)
    p.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Arriere')
    global Av,Ar,N
    Av = 0
    Ar = 1
    N = 0

def ArretMoteur():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in1,GPIO.LOW)
    p.stop()
    print ('Stop Moteur')
    global Av,Ar,N
    Av = 0
    Ar = 0
    N = 1

def Arret():
    print('--- ARRET ---')
    pwm.stop
    GPIO.output(in1,GPIO.LOW) #Arret du moteur
    GPIO.output(in1,GPIO.LOW) #(Vitesse inchangée, Rotation =  NONE)
    GPIO.cleanup()  #reset des Pins GPIO
    # + Arret des Threads
    global StopCommand
    StopCommand = 1   #"Commande Stop enclenchée" Plus tard, pour le thread des leds
    #break

while True:
    x = input("> ")
    if x == "avant":
        Avant(100)
        time.sleep(3)
        ArretMoteur()
    
    elif x == "arriere":
        Arriere(60)
        time.sleep(1)
        ArretMoteur()
    elif x == "stop":
        Arret()
        break
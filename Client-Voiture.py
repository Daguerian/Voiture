import socket
import threading
import time
import RPi.GPIO as GPIO
#Client RPi zero

### Mapping GPIO ###
Direction = 25      #Sortie pwm servomoteur de direction
in1 = 23            #Sortie L298N avant
in2 = 24            #Sortie L298N arriere
ena = 18            #Sortie pwm L298N controle vitesse
AxexCamera = 7      #Sortie pwm Axe x de camera
AxeyCamera = 8      #Sortie pwm Axe y de camera
Buzzer = 12         #Sortie buzzer passif
### Leds ###
LedStatRouge = 21   #Led de statut rouge
LedStatVerte = 20   #Led de statut verte
LedStatBleue = 16   #Led de statut Bleue
LedFeuxAvant = 19    #Leds de feux avant
LedFeuxArriere = 26  #Leds de feux arriere
####################
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def initVoiture():
    global pwmena,pwmDirection,pwmAxexCamera,pwmAxeyCamera
    global C,D,G,Av,Ar,N
    GPIO.setup(Direction,GPIO.OUT)
    pwmDirection = GPIO.PWM(Direction,50)   #50Hz
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(ena,GPIO.OUT)
    pwmena = GPIO.PWM(ena,50)
    GPIO.setup(AxexCamera,GPIO.OUT)
    pwmAxexCamera = GPIO.PWM(AxexCamera,50)
    GPIO.setup(AxeyCamera,GPIO.OUT)
    pwmAxeyCamera = GPIO.PWM(AxeyCamera,50)
    GPIO.setup(Buzzer,GPIO.OUT)
    GPIO.setup(LedStatRouge,GPIO.OUT)
    GPIO.setup(LedStatVerte,GPIO.OUT)
    GPIO.setup(LedStatBleue,GPIO.OUT)
    GPIO.setup(LedFeuxAvant,GPIO.OUT)
    GPIO.setup(LedFeuxArriere,GPIO.OUT)
    C,D,G,Av,Ar,N = 0
    pwmena.start(0)


def Droite():
    pwmDirection.start(7.8)      #/!\ à re-set pour egalité gauche-droite
    print ('DROITE')
    time.sleep(0.15)    #Arret du servo sur sa position
    pwmDirection.stop()
    global C,D,G
    C = 0  #Centre, Roues centre
    D = 1  #Droite, Roues droite
    G = 0  #Gauche, Roues Gauche

def Gauche():
    pwmDirection.start(6)        #/!\ à re-set pour egalité gauche-droite
    print ('GAUCHE')
    time.sleep(0.15)
    pwmDirection.stop()            #Arret du servo sur sa position
    global C,D,G
    C = 0
    D = 0
    G = 1

def Centre():
    pwmDirection.start(6.8)
    print ('NONE')
    time.sleep(0.15)
    pwmDirection.stop()
    global C,D,G
    C = 1
    D = 0
    G = 0

def Avant(Vitesse, Mode):       #Marche avant en fonction de la vitesse en %
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    pwmena.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Avant')
    global Av,Ar,N
    Av = (Mode)
    Ar = 0
    N = 0

def Arriere(Vitesse, Mode):     #Marche arriere en fonction de la vitesse en % et du mode de vitesse
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    pwmena.ChangeDutyCycle(Vitesse)  # /!\ set la vitesse, ne pas boucler
    print ('Marche Arriere')
    global Av,Ar,N
    Av = 0
    Ar = (Mode)
    N = 0

def CommandesVoiture():
    SplitRecu = Recu.split("/")
    if SplitRecu[0].lower() == ("avant"):
        if 0 <= SplitRecu[1] =< 100 and 1 <= SplitRecu[2] <= 3:
            Avant(SplitRecu[1],SplitRecu[2])
        else:
            Print ("Erreur de syntaxe avec '{}'".format(Recu))
            #led rouge 0.5s

    elif SplitRecu[0].lower() == ("arriere"):
        if 0 <= SplitRecu[1] <= 100 and 0 <= SplitRecu[2] <= 3:
            Arriere(SplitRecu[1],SplitRecu[2])
        else:
            print ("Erreur de syntaxe avec '{}'".format(Recu))

    if SplitRecu[0].lower() == ("gauche"):
        Gauche()

    elif SplitRecu[0].lower() == ("droite"):
        Droite()

    else:
        pass

def Arret():
    print ("cleanup des GPIO")
    GPIO.cleanup()

def Reception():
    global Recu
    while True:
        Recu = client.recv(1024).decode('UTF-8')
		if not Recu:
			print ('Erreur de reception')
			Erreur += 1
			if Erreur == 5:
				print ('Fermeture de la connexion')
				client.close()
				break
		if Recu.lower() == ('!arret'): #Arret du thread apres deconnexion volontaire du serveur
			print ('Arret du serveur. Deconnexion client')
			t = ('!leaveok')
			client.send(t.encode('UTF-8'))
			client.close()
			break
		if Recu.lower() == ('!leaveok'): #Arret du Thread apres deconnexion volontaire du client
			break
		else:
			print("Reçu:",Recu)
            CommandesVoiture()
ThreadReception = threading.Thread(target=Reception)


#########   Lancement   ##########
i = 1
IPserveur =
Port =
GPIO.output(LedStatRouge,HIGH)
for i in range(5):
    print ("Connexion au serveur...")
    try:
        client.connect((IPserveur,Port))
        print ("Connecté")
        break
    except:
        print ('Impossible de se connecter au serveur.')
        print ("{}e essai sur 5 dans 3 secondes".format(i))
        if i == 5:
            Arret() # dont reset leds
            exit()
try:
    initVoiture()
except:
    print ("impossible d'initialiser le programme")
    Arret()
    exit()

# ThreadReception.start()
Reception():

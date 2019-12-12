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

def ConnexionServeur():
    IPserveur = "10.1.1.15"
    Port = 6789
    GPIO.output(LedStatRouge,GPIO.HIGH)
    print ("Connexion au serveur...")
    try:
        client.connect((IPserveur,Port))
        print ("Connecté")
        ThreadReception.start()
    except:
        print ('Impossible de se connecter au serveur.')

class ControleVoiture():
    def __init__(self):
        GPIO.setup(Direction,GPIO.OUT)
        self.pwmDirection = GPIO.PWM(Direction,50)   #50Hz
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        self.pwmena = GPIO.PWM(ena,50)
        GPIO.setup(AxexCamera,GPIO.OUT)
        self.pwmAxexCamera = GPIO.PWM(AxexCamera,50)
        GPIO.setup(AxeyCamera,GPIO.OUT)
        pwmAxeyCamera = GPIO.PWM(AxeyCamera,50)
        GPIO.setup(Buzzer,GPIO.OUT)
        GPIO.setup(LedStatRouge,GPIO.OUT)
        GPIO.setup(LedStatVerte,GPIO.OUT)
        GPIO.setup(LedStatBleue,GPIO.OUT)
        GPIO.setup(LedFeuxAvant,GPIO.OUT)
        GPIO.setup(LedFeuxArriere,GPIO.OUT)
        self.C = self.D = self.G = self.Av = self.Ar = self.N = 0
        self.pwmena.start(0) #demarre la vitesse du moteur à 0, les autres pwmena.ChangeDutyCycle


    def Avant(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        self.pwmena.ChangeDutyCycle(Vitesse)
        print ("Avant, {}%, {}e Vitesse".format(Vitesse,Mode))
        self.Av = (Mode)
        self.Ar = 0
        self.N = 0

    def Arriere(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        self.pwmena.ChangeDutyCycle(Vitesse)
        print ("Arriere, {}%, {}e Vitesse".format(Vitesse,Mode))
        self.Av = 0
        self.Ar = (Mode)
        self.N = 0

    def Neutre(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.pwmena.ChangeDutyCycle(Vitesse)
        print ("Neutre")
        self.Av = 0
        self.Ar = 0
        self.N = 0

    def Gauche(self):
        pwmDirection.start(6)
        print ("Gauche")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 0
        self.D = 0
        self.G = 1

    def Droite(self):
        pwmDirection.start(7.8)
        print("Droite")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 0
        self.D = 1
        self.G = 0

    def Centre(self):
        pwmDirection.start(6.8)
        print ("Centre")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 1
        self.D = 0
        self.G = 0

Voiture = ControleVoiture()

def CommandesVoiture():
    SplitRecu = Recu.split("/")
    if SplitRecu[0].lower() == ("avant"):
        if 0 <= SplitRecu[1] <= 100 and 1 <= SplitRecu[2] <= 3:
            Voiture.Avant(SplitRecu[1],SplitRecu[2])
        else:
            print ("Condition non respectée:", Recu)

    elif SplitRecu[0].lower() == ("arriere"):
        if 0 <= SplitRecu[1] <= 100 and 0 <= SplitRecu[2] <= 3:
            Voiture.Arriere(SplitRecu[1],SplitRecu[2])
        else:
            print ("Condition non respectée:", Recu)

    elif SplitRecu[0].lower() == ("neutre"):
        Voiture.Neutre()

    if SplitRecu[0].lower() == ("gauche"):
        Voiture.Gauche()

    elif SplitRecu[0].lower() == ("droite"):
        Voiture.Droite()

    elif SplitRecu[0].lower() == ("neutre"):
        Voiture.Centre()

    else:
        pass
        time.sleep(0.01)


ThreadVoiture = threading.Thread(target=CommandesVoiture)
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
				print ("Fermeture de la connexion\nTrop d'erreurs de reception")
				client.close()
				break
		if Recu.lower() == ('!leave'): #Arret du thread apres deconnexion volontaire du serveur
			print ('Arret du serveur. Deconnexion client')
			t = ('!leaveok')
			client.send(t.encode('UTF-8'))
			client.close()
			break
		if Recu.lower() == ('!leaveok'): #Arret du Thread apres deconnexion volontaire du client
			break
		else:
			CommandesVoiture()
ThreadReception = threading.Thread(target=Reception)

#########   Lancement   ##########
while True:
    Saisie = input ("> ")
    y = Saisie.startswith("-",0,2)
    if y:
        if Saisie.lower() == "-exit":
            break

        elif Saisie.lower() == "-init":
            try:
                initVoiture()
            except:
                print ("Impossible d'initialser la voiture")
        elif Saisie.lower() == "-join":
            ConnexionServeur()

        elif Saisie.lower() == ("-start"):
            ThreadVoiture.start()
            print ("Thread Voiture lancé")

        elif Saisie.lower() == "-disconnect":
            Envoi = ("!leave")
            client.send(Envoi.encode("UTF-8"))
        elif Saisie.lower() == "-help":
            print ("##################################################")
            print ("### -init    Lance une initialisation generale ###")
            print ("### -Join    Lance la connexion au serveur     ###")
            print ("### -exit    Quitte le programme               ###")
            print ("##################################################")

        else:
            print ("Commande non reconnue")
    else:
        print ("Saisie non traitée")

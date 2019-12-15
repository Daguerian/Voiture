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

class GestionSocket():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IPserveur = "10.1.1.15"
        self.Port = 6789

    def Connexion(self):
        print ("Connexion au serveur...")
        try:
            self.client.connect((self.IPserveur,self.Port))
            print ("Connecté")
            self.ThreadReception(target=self.Reception)
            self.ThreadReception.start()
        except:
            print ('Impossible de se connecter au serveur.')

    def Deconnexion(self):
        print ("Deconnexion du serveur...")
        Envoi = ("!leave")
        self.client.send(Envoi.encode("UTF-8"))
        time.sleep(0.5)
        self.client.close
        print ("Deconnecté.")

    def Reception(self):
        Erreur = 0
        while True:
            Envoi = ("RPi Zero Voiture")
            self.client.send(Envoi.encode("UTF-8"))
            data = self.client.recv(1024)
            self.NomServeur = data.decode("UTF-8")

        while True:
            data = self.client.recv(1024)   #Reception
            self.Recu = data.decode("UTF-8")    #Decodage
            self.SplitRecu = self.Recu.split("/")   #Separation
            y = self.Recu.startswith("!",0,2)    #Simple detection de commande
            print(self.Recu)

            if not self.Recu:
                print ("Erreur de reception")
                Erreur += 1
                if Erreur == 5:
                    print ("Deconnexion de {} \ntrop d'erreurs de reception".format(self.NomServeur))
                    break
            elif y:
                if self.Recu.lower() == ("!leaveok"):
                    print ("Deconnexion")
                    break
                elif self.Recu.lower() == ("leave"):
                    print ("Arret du serveur. Deconnexion...")
                    self.client.close()
                    print ("Deconnecté.0")

            if self.SplitRecu[0].lower() == ("avant"):
                if 0 <= self.SplitRecu[1] <= 100 and 1 <= self.SplitRecu[2] <= 3:
                    Voiture.Avant(self.SplitRecu[1],self.SplitRecu[2])
                else:
                    print ("Condition non respectée:", self.Recu)

            elif self.SplitRecu[0].lower() == ("arriere"):
                if 0 <= self.SplitRecu[1] <= 100 and 0 <= self.SplitRecu[2] <= 3:
                    Voiture.Arriere(self.SplitRecu[1],self.SplitRecu[2])
                else:
                    print ("Condition non respectée:", self.Recu)

            elif self.SplitRecu[0].lower() == ("neutre"):
                Voiture.Neutre()

            if self.SplitRecu[0].lower() == ("gauche"):
                Voiture.Gauche()

            elif self.SplitRecu[0].lower() == ("droite"):
                Voiture.Droite()

            elif self.SplitRecu[0].lower() == ("neutre"):
                Voiture.Centre()

            else:
                pass
                time.sleep(0.01)

class ControleVoiture():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Direction,GPIO.OUT)
        self.pwmDirection = GPIO.PWM(Direction,50)   #50Hz
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        self.pwmena = GPIO.PWM(ena,50)
        GPIO.setup(AxexCamera,GPIO.OUT)
        self.pwmAxexCamera = GPIO.PWM(AxexCamera,50)
        GPIO.setup(AxeyCamera,GPIO.OUT)
        self.pwmAxeyCamera = GPIO.PWM(AxeyCamera,50)
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
        self.Av = (Mode)    # eventuellement utilisé pour renvoyer
        self.Ar = 0         # à la page web
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
        self.pwmena.ChangeDutyCycle(0)
        print ("Neutre")
        self.Av = 0
        self.Ar = 0
        self.N = 0

    def Gauche(self):
        self.pwmDirection.start(6)
        print ("Gauche")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 0
        self.D = 0
        self.G = 1

    def Droite(self):
        self.pwmDirection.start(7.8)
        print("Droite")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 0
        self.D = 1
        self.G = 0

    def Centre(self):
        self.pwmDirection.start(6.8)
        print ("Centre")
        time.sleep(0.15)
        self.pwmDirection.stop()
        self.C = 1
        self.D = 0
        self.G = 0

#########   Lancement   ##########
ListeInit = []
while True:
    Saisie = input ("> ")
    y = Saisie.startswith("-",0,2)
    if y:
        if Saisie.lower() == "exit":
            GPIO.cleanup()
            break

        elif Saisie.lower() == "init":
            if not ("Voiture") in ListeInit:
                try:
                    Voiture = ControleVoiture()
                    print ("Initialisation voiture OK.")
                    ListeInit.append("Voiture")
                except:
                    print ("Impossible d'initialser la voiture")
            else:
                print ("Voiture deja initialisée")

            if not ("Socket") in ListeInit:
                try:
                    Client = GestionSocket()
                    print ("Initialisation Voiture OK.")
                    ListeInit.append("Socket")
                except:
                    print ("Impossible d'initialiser le socket")
            else:
                print ("Socket deja initialisé")

        elif Saisie.lower() == "join":
            try:
                Client.Connexion()
            except:
                print ("Client non initialisé")

        elif Saisie.lower() == ("start"):
            pass

        elif Saisie.lower() == "stop":
            Client.Deconnexion()

        elif Saisie.lower() == "help":
            print ("##################################################")
            print ("### -init    Lance une initialisation generale ###")
            print ("### -Join    Lance la connexion au serveur     ###")
            print ("### -exit    Quitte le programme               ###")
            print ("##################################################")

        else:
            print ("Commande non reconnue")
    else:
        print ("Saisie non traitée")

exit()
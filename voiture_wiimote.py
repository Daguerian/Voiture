# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import cwiid
### Mapping Wiimote ###
#2 = 1
#1 = 2
#B = 4
# A = 8
# - = 16
# home = 128
# left = 256
# right = 512
# down = 1024
# up = 2048
# + = 4096
### Mapping GPIO ###
servo_direction = 25
in1 = 23
in2 = 24
ena = 18
# servo_cam_x = 7
# servo_cam_y = 8
# buzzer = 12
# ledstat_r = 21
# ledstat_g = 20        /!\
# ledstat_b = 16      les init
# led_av = 19
# led_ar = 26
#####################
class car():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(servo_direction,GPIO.OUT)
        self.pwm_direction = GPIO.PWM(servo_direction,50)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        self.pwm_ena = GPIO.PWM(ena,50)
        self.C = self.D = self.G = 0    # axe y
        self.Av = self.Ar = self.N = 0  # axe x
        self.pwm_ena.start(0) #demarre la vitesse du moteur à 0, les autres pwmena.ChangeDutyCycle

    def Avant(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        self.pwm_ena.ChangeDutyCycle(Vitesse)
        print ("Avant, {}%, {}e Vitesse".format(Vitesse,Mode))
        self.Av = (Mode)    # eventuellement utilisé pour renvoyer
        self.Ar = 0         # à la page web
        self.N = 0

    def Arriere(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        self.pwm_ena.ChangeDutyCycle(Vitesse)
        print ("Arriere, {}%, {}e Vitesse".format(Vitesse,Mode))
        self.Av = 0
        self.Ar = (Mode)
        self.N = 0

    def Neutre(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        self.pwm_ena.ChangeDutyCycle(0)
        print ("Neutre")
        self.Av = 0
        self.Ar = 0
        self.N = 1

    def Gauche(self):
        self.pwm_direction.start(6)
        print ("Gauche")
        time.sleep(0.15)
        self.pwm_direction.stop()
        self.C = 0
        self.D = 0
        self.G = 1

    def Droite(self):
        self.pwm_direction.start(7.8)
        print("Droite")
        time.sleep(0.15)
        self.pwm_direction.stop()
        self.C = 0
        self.D = 1
        self.G = 0

    def Centre(self):
        self.pwm_direction.start(6.8)
        print ("Centre")
        time.sleep(0.15)
        self.pwm_direction.stop()
        self.C = 1
        self.D = 0
        self.G = 0

### init variables stat ###
wiimote_connected = False
nunchuk_connected = False 
program_running = False


### Lancement ###
print ("lancement du programme")
try:
    voiture = car()
    print ("Voiture initialisée")
except:
    print ("impossible d'initialiser la voiture")
    GPIO.cleanup()
    exit()

while not wiimote_connected:    #verification de connexion à la wiimote
    print ("connexion à la wiimote...")
    time.sleep(0.5)
    try:
        wm = cwiid.Wiimote()
        wiimote_connected = True
        print ("Wiimote connectée !")
    except:
        print ("wiimote non detectée")

wm.led = 15
wm.rumble = 1
time.sleep(1)
wm.led = 6
wm.rumble = 0

while not nunchuk_connected:    #Verification de connexion du nunchuk
    try:
        wm.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
        nun = wm.state["nunchuk"]
        wm_buttons = wm.state["buttons"]
        nun_button = nun["buttons"]
        nun_stick = nun["stick"]
        nun_acc = nun["acc"]
        nunchuk_connected = True
    except:
        print ("impossible d'initialiser l'aquisition de données")
        print ("verifiez la connexion du nunchuk")

print ("-- tout est prêt --")

program_running = True

while program_running:
    time.sleep(0.08)
    try: 
        nun = wm.state["nunchuk"]
        wm_buttons = wm.state["buttons"]
        nun_buttons = nun["buttons"]
        nun_stick = nun["stick"]
        nun_acc = nun["acc"]
    except:
        print ("Erreur d'aquisition des données")

    if wm_buttons == 128:   #Bouton Home wiimote
        print ("Arret du programme.")
        program_running = False

    # if wm_buttons == 8 and not voiture.Av:
    #     voiture.Avant(50,1)
    # elif wm_buttons == 4 and not voiture.Ar:
    #     voiture.Arriere(25,1)
    # elif wm_buttons != (4 or 8) and not voiture.N:
    #     voiture.Neutre()

    # if nun_buttons == 1 and not voiture.Av: #bouton nunchuk Z
    #     voiture.Avant(50,1)

    # elif nun_buttons == 2 and not voiture.Ar:   #bouton nunchuk c
    #     voiture.Arriere(25,1)

    # elif nun_button == 0 and not voiture.N:    #aucun des deux boutons nunchuk
    #     voiture.Neutre()
        
    if nun_stick[1] > 160 and not voiture.Av:
        voiture.Avant(50,1)

    elif nun_stick[1] < 90 and not voiture.Ar:
        voiture.Arriere(25,1)
    elif 50 < nun_stick[1] < 160 and not voiture.N:
        voiture.Neutre()

    if nun_stick[0] < 90 and not voiture.G: #Stick nunchuk gauche
        voiture.Gauche()

    elif nun_stick[0] > 160 and not voiture.D:  #axe x stick nunchuk droite
        voiture.Droite()

    elif 90 < nun_stick[0] < 160 and not voiture.C:   #axe x stick nunchuk centré
        voiture.Centre()


wm.rumble = 1
wm.led = 15
time.sleep(1)

GPIO.cleanup()
wm.close()

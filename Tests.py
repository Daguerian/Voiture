class Voiture():

    def Avant(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        pwmena.ChangeDutyCycle(Vitesse)
        self.Av = (Mode)
        self.Ar = 0
        self.N = 0

    def Arriere(self, Vitesse, Mode):
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        pwmena.ChangeDutyCycle(Vitesse)
        self.Av = 0
        self.Ar = (Mode)
        self.N = 0

    def Neutre():
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        pwmena.ChangeDutyCycle(Vitesse)
        self.Av = 0
        self.Ar = 0
        self.N = 0

    def Gauche():
        pwmDirection.start(6)
        print ("Gauche")
        time.sleep(0.15)
        pwmDirection.stop()
        self.C = 0
        self.D = 0
        self.G = 1

    def Droite():
        pwmDirection.start(7.8)
        print("Droite")
        time.sleep(0.15)
        pwmDirection.stop()
        self.C = 0
        self.D = 1
        self.G = 0

    def Centre():
        pwmDirection.start(6.8)
        print ("Centre")
        time.sleep(0.15)
        pwmDirection.stop()
        self.C = 1
        self.D = 0
        self.G = 0
        

Voiture.Avant(60, 2)
Voiture.Arriere(50,2)
Voiture.Neutre()

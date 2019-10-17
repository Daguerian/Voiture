import socket
import threading
import time

#Serveur sur RPi 3B+

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



####  Start Prog ####

Host, Port = input('Adresse Host: '), 6789
try:
	serveur.bind((Host, Port))
except:
	print ('Impossible d\'heberger le serveur sur {}:{}'.format(Host,Port))
	exit()

print ('Serveur hebergé sur ',Host, Port, '\n', 'Appareil', socket.gethostname())
print ('En attente de connexion...\n')

ThreadReception = threading.Thread(target=Reception)
### Connexion du client
serveur.listen(3) #3 connexions maxi
client, AdresseClient = serveur.accept()
#Blocage tant que le client n'est pas connecté

EnvoiNameServer = (socket.gethostname())			#Envoi Nom du serveur
client.send(EnvoiNameServer.encode('UTF-8'))

données = client.recv(1024)							#Reception Nom du client
NomClient = données.decode('UTF-8')
print (NomClient,'connecté')
ThreadReception.start()

while True:

	Saisie = input('Saisissez: ')

	# if Saisie.lower() == ('-arret'):
	# 	Stop()
	# 	break
	y = Saisie.startswith('-',0,2) #'-' entre 0 et 2, non inclus
	if y:
		CommandList()	#Action en fonction d'une demande syntaxée
		y = 0
	else:
		n = client.send(Saisie.encode('UTF-8'))
		if not n:
			print ('Erreur d\'envoi')
		else:
			print ('Envoyé.')
## Info sur le code 
#traduction en python 16/10/19

# Fichiers utilisés : Rocket definition (Declarations --> Environment -->)
#                     Rocket reader 

# Fonctions utilisées : std atmos (functions --> stdatmos) modèle de l'environnement
#                      drag + drag shuriken
#                      
# fonctions non utilisées : bissection, thrust

# Commande 'complexe' : polyval + 

# drv = vecteur contenant la force de trainée pour les différentes
#       vitesses (de 0 a 300) et les différents angles théta


import math
import Functions
#from Functions.drag import *
#from Functions.bisection import *
#from Functions.Thrust import *
#from Functions.drag_shuriken import *
#from Functions.rocketReader import *
#from Functions.environnementReader import *
from numpy import *
from scipy import interpolate
#from Functions.stdAtmos import *

# Communication with the CAN
from PCANBasic import *
import struct

KALMAN_BOARD_ID = 0

DATA_ID_ACCELERATION_X = 1
DATA_ID_ACCELERATION_Y = 2
DATA_ID_ACCELERATION_Z = 3
DATA_ID_GYRO_X = 4
DATA_ID_GYRO_Y = 5
DATA_ID_GYRO_Z = 6
DATA_ID_CALIB_PRESSURE = 13
DATA_ID_PRESSURE = 0

DATA_ID_KALMAN_VZ = 45
DATA_ID_KALMAN_Z = 42


def readCanData():

	readResult = objPCAN.Read(PCAN_USBBUS1);
	while (readResult[1].getID() != KALMAN_BOARD_ID): # We expect results from the KALMAN BOARD
			readResult = objPCAN.Read(PCAN_USBBUS1)

	data = 0
	for i in range(4):
		data_i = str(readResult[1].DATA[i])
		data += int(data_i) * (256**(4-1-i))
	msg_id = str(readResult[1].DATA[4])

	return data, msg_id

def SendCanData(data, msg_id):
	MessageBuffer = TPCANMsg()

	MessageBuffer.setID(0)
	# Data = {data, msg_id, timestamp}
	MessageBuffer.setData([data >> 24, data >> 16, data >> 8, data >> 0, msg_id >> 0, 0, 0, 0])

	objPCAN.Write(PCAN_USBBUS1, MessageBuffer);


# Initialize the Plug & Play Channel (PCAN-USB)
objPCAN = PCANBasic()
result = objPCAN.Initialize(PCAN_USBBUS1, PCAN_BAUD_250K)
if result != PCAN_ERROR_OK:
    # An error occurred
    result = objPCAN.GetErrorText(result)
    print(result[1])
else:
    print("PCAN-USB (Ch-1) was initialized")


# Définition des modèles/fonctions + Variables

# On défini les objets Rocket et Environment avec les propriétés provenant
# de fichier texte
Rocket = rocketReader('Rocket_Definition_Eiger_I_R03.txt');
Environment = environnementReader('Environnement_Definition_USA.txt');

dt=0.25; # Intervalle de temps pour le controle

rho=lambda alt:  -9.9814e-05*alt+1.1037; 
# Modèle de la densité fonction de l'altitude...
# ce modèle va dépendre du modèle de l'environnement...
# on va créer une fonction qui crée cette fonction ...
# en fonction du fichier texte qui définie l'environnement...
# un peu plus tard --> pour l'instant utiliser cette fonction de la densité
g=9.81;


#### TODO ####
print('TODO: Ask Thomas')
P0=Environment.Pressure_Ground;

SendCanData(int(P0), DATA_ID_CALIB_PRESSURE) # acc z


# L'avionics à besoin d'avoir la pression au sol pour le Kalman, on lui
# envoie donc P0 avant de commencer la transmission (demander précison à Thomas)

# L'avionics à besoin d'avoir la pression au sol pour le Kalman, on lui
# envoie donc P0 avant de commencer la transmission (demander précison à Thomas)

# On défini des vecteurs qui vont stocker les valeurs de x et v pour chaque pas de temps dans des
# vecteurs, ces valeurs sont très importantes, ce sont les données exactes
# de notre simulation qu'on pourra ensuite comparer aux données que nous
# renvoie le Kalman. On va jouer avec le bruit des données de sensors pour
# tester le Kalman, ces performances seront évaluer en se basant sur la
# différence entre Xvect et Vvect.


#ON LANCE UNE PREMIER PAQUET DE DONNEES POUR L'ETAT POST-POUSSEE :

theta=-190.5 # On intie théta avec la valeur de l'angle d'ouverture des airbrakes post poussée,
# Chaque itération, cette valeur prendra celle donnée par le CAN bus à
# l'itération précédente qui est calculé par l'algo de contrôle.

x=750; # On initie x avec l'altitude initiale post poussée, chaque itération x sera updater avec la valeur calculé par notre simulation
v=250; # On initie v avec l'altitude initiale post poussée, chaque itération v sera updater avec la valeur calculé par notre simulation

Xvect=[x];  
Vvect=[v];


[_, a, Pstat, _, nu] = stdAtmos(x,Environment);
CD0=drag(Rocket,0,v,nu,a);
CD_ABferm=drag_shuriken(Rocket,-190.5,0, v, nu);

#  Attention, ici c'est Pstat et non Pdyn comme dans le code de départ
Pstatb = Pstat # +... 
# 'le +...' en commentaire de la ligne précédente signifie qu'on va 
# rajouter du bruit à Pstat et stocker la nouvelle valeur bruitée dans la
# variable Pstatb, on va faire tourner plusieurs simulation avec plusieurs
# valeurs du bruit pour tester le Kalman. Prendre un bruit gaussien à
# chaque fois et faire varier l'écart type / la moyenne. Plus on a de
# donnée, mieux on pourra travailler et optimiser le controle des
# aérofreins

ax=-g-(0.5*rho(x)*(CD0+CD_ABferm)*Rocket.Sm*v**2)/Rocket.rocket_m;
axb=ax # + ...
# Pareillement, on rajoute du bruit sur l'accélération de la fusée.


# On stocke les valeures provenant des sensors
axvect=[ax];
axbvect=[axb];
Pstatvect=[Pstat];
Pstatbvect=[Pstatb]; 

# CALCULE DE LA TRAJECTOIRE  : ON CALCULE TOUT EN SUPPOSANT 
# UNE OUVERTURE INSTANTANNEE DES AIRBRAKES, ET UNE CHAINE AVIONICS
# IMMEDIATE POUR L'INSTANT

SendCanData(0, DATA_ID_ACCELERATION_X) # acc x
SendCanData(0, DATA_ID_ACCELERATION_Y) # acc y
SendCanData(int(axvect[-1]), DATA_ID_ACCELERATION_Z) # acc z
#SendCanData(0., DATA_ID_GYRO_X) # angle rate
#SendCanData(0., DATA_ID_GYRO_y) # angle rate
#SendCanData(0., DATA_ID_GYRO_z) # angle rate
SendCanData(int(Pstatvect[-1]), DATA_ID_PRESSURE) # pression statique (à cette altitude)

while (True):
    # Check the receive queue for new messages
    #
    readResult = objPCAN.Read(PCAN_USBBUS1)
    if readResult[0] != PCAN_ERROR_QRCVEMPTY:
        # Process the received message
        #
        #print("A message was received")
        count += 1
        #print("Method code", readResult[0])
        print("ID", readResult[1].getID())
       # print("MSGTYPE", readResult[1].MSGTYPE)
        print("LEN", readResult[1].LEN)
        #print("DATA", readResult[1].DATA)
        print("DATA", readResult[1].__str__())
        #print("")
        #ProcessMessage(result[1],result[2]) # Possible processing function, ProcessMessage(msg,timestamp)
    else:
        pass
	    #print("PROB") # An error occurred, get a text describing the error and show it
	    #result = objPCAN.GetErrorText(readResult[0])
	    #print(result[1])

while(v>0.01):

	Sleep(1000);


	# read theta from the CAN
	theta, msg_id = readCanData()

	if msg_id == TODO: #TODO, check msg id
		pass

	# On update le modèle du drag selon la valeur de théta
	CD0=drag(Rocket,0,v,nu,a); # Drag de la fusée à angle d'attaque 0 (1D pour l'instant)
	CD_ABferm=drag_shuriken(Rocket,theta,0, v, nu); # Drag des aérofreins à angle d'attaque 0 (1D pour l'instant)

	#  B est une constante qui dépend de l'altitude qu'on utilise pour la
	#  résolution physique des équations
	A=-9.81;
	B=-0.5*rho(x)*Rocket.Sm*(CD0+CD_ABferm)/Rocket.rocket_m;
	#  Rocket.rocket_m = masse de la fusée post poussée
	#  Rocket.Sm = surface frontale de la fusée 

	# On crée une fonction f2 qui nous permets de trouver la vitesse à un temps
	# t après les conditions initiale
	f2=lambda t:  sqrt(A/B)*tan(A*sqrt(B/A)*t+atan(v*sqrt(B/A)));
	v=f2(dt);
	Vvect.append(v);
	# Calcul de l'altitude (solution exacte) (fct de t et B qui dépend de théta)
	# Pour faire ca on procède en plusieurs étapes (trois lignes suivantes)
	f= lambda t :  (cos(A*sqrt(B/A)*t+atan(v*sqrt(B/A))));
	y=f(dt);
	C=x-log(f(0))/sqrt(A*B)*sqrt(A/B);
	x= C+log(y)/(sqrt(A*B))*sqrt(A/B);
	Xvect.append(x);

	## On recalcule les données à envoyer au CAN pour le nouvel état (état=x,v)
	[_, _, Pstat, _, nu] = stdAtmos(x, Environment);
	Pstatb=Pstat # +...; # bruit sera le meme tout le temps, on prendra une Gaussienne

	Pstatvect.append(Pstat);
	Pstatbvect.append(Pstatb);
	ax=(Vvect[-1]-Vvect[-2])/dt;
	axb=ax  # +...,
	axvect.append(ax);
	axbvect.append(axb);

	# send data to the CAN
	print("Q: --> imub[0]--> 0 à 5?")
	SendCanData(0, DATA_ID_ACCELERATION_X) # acc x
	SendCanData(0, DATA_ID_ACCELERATION_Y) # acc y
	SendCanData(int(axvect[-1]), DATA_ID_ACCELERATION_Z) # acc z
	#SendCanData(0., DATA_ID_GYRO_X) # angle rate
	#SendCanData(0., DATA_ID_GYRO_y) # angle rate
	#SendCanData(0., DATA_ID_GYRO_z) # angle rate
	SendCanData(int(Pstatvect[-1]), DATA_ID_PRESSURE) # pression statique (à cette altitude)
	#SendCanData(P0, TODO) # pression de base (à l’altitude delancement)
	#SendCanData(0., TODO) # Zdata 0
	#SendCanData(0., TODO) # Zdata 1
	#SendCanData(0., TODO) # Zdata 2
	print("Q: What to send here????")
	SendCanData(0, TODO) # Zdata.3= Alt(P) altitude en fonction de la pression

	print(x)
	print(v)



# Release the USB Channel
result = objPCAN.Uninitialize(PCAN_USBBUS1)
if result != PCAN_ERROR_OK:
    # An error occurred, get a text describing the error and show it
    
    result = objPCAN.GetErrorText(result)
    print(result[1])
else:
    print("PCAN-USB (Ch-1) was released")






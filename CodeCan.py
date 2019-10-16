## Nettoyage du Workspace
#note sure this is usefull in python
#clear all
#close all
#clc

## Info sur le code 
#traduction en python 16/10/19

# Fichiers utilisés : Rocket definition (Declarations --> Environment -->)
#                     Rocket reader 

# Fonctions utilisés : std atmos (functions --> stdatmos) modèle de l'environnement
#                      drag + drag shuriken
#                      bissection

# Commande 'complexe' : polyval + 

# drv = vecteur contenant la force de trainée pour les différentes
#       vitesses (de 0 a 300) et les différents angles théta


import math
from drag import *
from bisection import *
from Thrust import *
from drag_shuriken import *
from rocketReader import *
from environnementReader import *
import numpy as np
from numpy import *
from scipy import interpolate
from stdAtmos import *

# ## import arctangeante
# termcolor import colored

## Définition des modèles/fonctions

rho=lambda alt:  -9.9814e-05*alt+1.1037; 

## Définition des différentes Variables 

Rocket = rocketReader('Rocket_Definition_Eiger_I_R03.txt');
Environnement = environnementReader('Environnement_Definition_USA.txt');

dt=0.25; # Intervalle de temps pour le controle
x=750;
v=250;
[_, a, _, _, nu] = stdAtmos(x,Environnement);
CD0=drag(Rocket,0,v,nu,a);
CD_ABferm=drag_shuriken(Rocket,-190.5,0, v, nu);
g=9.81;

Xvect=[x];
Vvect=[v];


Pdyn=0.5*v**2*rho(x);
Pdynb = Pdyn # +...
    
ax=-g-(0.5*rho(x)*(CD0+CD_ABferm)*Rocket.Sm*v**2)/Rocket.rocket_m;
axb=ax # + ...

axvect=[ax];
axbvect=[axb];
Pdynvect=[];
Pdynbvect=[]; 

# Les valeurs de x et v vont changer à toutes les itérations de la boucle

[_, a, _, _, nu] = stdAtmos(x,Environnement);
CD0=drag(Rocket,0,v,nu,a);
CD_ABferm=drag_shuriken(Rocket,-190.5,0, v, nu);
Mdry=26.13; 
A=-9.81;
B=-0.5*rho(x)*Rocket.Sm*(CD0+CD_ABferm)/Rocket.rocket_m;

f2=lambda t:  sqrt(A/B)*tan(A*sqrt(B/A)*t+atan(v*sqrt(B/A)));
v=f2(dt);

# Calcul de l'altitude (solution exacte) (fct de t et B qui dépend de théta)
f= lambda t :  (cos(A*sqrt(B/A)*t+atan(v*sqrt(B/A))));
y=f(dt);
C=x-log(f(0))/sqrt(A*B)*sqrt(A/B);
x= C+log(y)/(sqrt(A*B))*sqrt(A/B);

Xvect=[Xvect, x];
Vvect=[Vvect, v];


Pdyn=0.5*v**2*rho(x);
Pdynb=Pdyn # +...;
Pdynvect=[Pdynvect, Pdyn];
Pdynbvect=[Pdynbvect, Pdynb];
    
ax=(Vvect[-1]-Vvect[-2])/dt;
axb=ax # +...,
axvect=[axvect, ax];
axbvect=[axbvect, axb];


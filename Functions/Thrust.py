import math
from scipy import interpolate
import numpy as np

def Thrust(t,Rocket):
#	Return the motor thrust along its axis
#   INPUT:
#   - t         Time
#   - Rocket    Structure Containing all datas
#   OUTPUT:
#   - T         Motor Thrust
# TRAD TO PYTHON 8/10/19

#   Linear Interpolation
    if t > Rocket.Burn_Time :
        return 0;
    if t < 0:
        return 0;
    else:
       return interpolate.interp1d(Rocket.Thrust_Time,Rocket.Thrust_Force)(t);



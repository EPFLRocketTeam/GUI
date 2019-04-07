# Author : Henri Faure
# Date : 20 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

# Return the motor thrust along its axis

def Thrust(t,Rocket):
#   INPUT:
#   - t         Time
#   - Rocket    Structure Containing all datas
#   OUTPUT:
#   - T         Motor Thrust
  
    from scipy.interpolate import interp1d
    
    if 0 > t > Rocket.Burn_Time:
        T = 0
    else:
        T = interp1d(Rocket.Thrust_Time, Rocket.Thrust_Force)(t)
        
    return T

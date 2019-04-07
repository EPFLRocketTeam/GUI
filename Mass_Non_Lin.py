# Author : Henri Faure
# Date : 20 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

# Return the rocket mass during burn time

def Mass_Non_Lin(t,Rocket):
#   INPUT:
#   - t         Time
#   - Rocket    Structure Containing all datas
#   OUTPUT:
#   - Mass      Rocket mass
#   - dMassdt   Rocket mass derivative over time
    
    import numpy as np
    from '*****' import Thrust
    
    if t > Rocket.Burn_Time:
        mass = Rocket.rocket_m+Rocket.motor_mass-Rocket.propellant_mass
        dmassdt = 0
    else:
        tt = np.linspace(0,t,500)
        Current_Impulse = np.trapz(Thrust(tt,Rocket),tt)
        mass = Rocket.rocket_m + Rocket.motor_mass - Rocket.Thrust2dMass_Ratio*Current_Impulse
        dmassdt = Rocket.Thrust2dMass_Ratio*Thrust(t,Rocket)
    
    return mass,dmassdt
           
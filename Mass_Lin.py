# Author : Henri Faure
# Date : 20 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

# Return the rocket mass during burn time

def Mass_Lin(t,Rocket):
#   INPUT:
#   - t         Time
#   - Rocket    Structure Containing all datas
#   OUTPUT:
#   - mass      Rocket mass
#   - dmassdt   Rocket mass derivative over time

    if t < Rocket.Burn_time:
        mass = Rocket.rocket_m + Rocket.casing_mass
        dmassdt = 0
    else:
        dmassdt = Rocket.propel_mass/Rocket.Burn_Time
        mass = Rocket.rocket_m + Rocket.motor_mass - t*dmassdt

    return mass,dmassdt

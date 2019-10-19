import math
from scipy import interpolate
import numpy as np

def stdAtmos(alt,Environnement):
# stdAtmos
#
# INPUT:    - alt   : altitude [m]
#
# OUPTUT:   - T     : local standard temperature [?K]
#           - a     : local speed of sound [m/s]
#           - p     : local standard pressure [Pa]
#           - rho   : local standard density [kg/m^3]
#	    - nu    : local viscosity [kg/(m*s)]
# ASSUMPTIONS:
# - hydrostatic approximation of atmosphere
# - linear temperature variation with altitude
# - homogenous composition
#
# LIMITATIONS:
# - troposphere: 10km
#
# AUTOR:    ERIC BRUNNER
# LAST UPDATE: 05/03/2017
# TRAD TO PYTHON 8/10/19

# CHECK ALTITUDE RANGE
    if alt > 1e4:
        raise NameError('stdAtmos:outOfRange', 'The altitude is out of range: max 10km.')
    else:
        
        # CONSTANTS
        R = 287.04; #[M^2/?K/sec^2] real gas constant of air
        gamma = 1.4; #[-] specific heat coefficient of air
        # MEAN SEA LEVEL CONDITIONS
        p0 = 101325; #[Pa]
        rho0 = 1.225; #[kg/m^3]
        T0 = 288.15; #[?K]
        a0 = 340.294; #[m/sec]
        g0 = 9.80665; #[m/sec^2
        
        # DATA
        # stations
        dTdh = -6.5; #[?K/km] temperature variation in troposphere
        
        # TEMPERATURE MODEL
        T = T0 + dTdh*alt/1000;
        
        # PRESSURE MODEL
        p = p0*(1+dTdh/1000*alt/T0)**(-g0/R/dTdh*1000);
        
        # DENSITY MODEL
        x = Environnement.Saturation_Vapor_Ratio*Environnement.Humidity_Ground;
        rho = p/R/T*(1+x)/(1+1.609*x);
        
        # SPEED OF SOUND
        a = (gamma*R*T)**(0.5)
        
        # VISCOSITY
        nu = interpolate.interp1d(Environnement.T_Nu,Environnement.Viscosity)(T)
        
        return [T, a, p, rho,nu]


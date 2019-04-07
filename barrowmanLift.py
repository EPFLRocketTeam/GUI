# Author : Henri Faure
# Date : 20 March 2019
# EPFL Rocket Team, 1015 Lausanne, Switzerland

def barrowmanLift(Rocket, alpha, M, theta):

    import math
    import warnings
    import numpy as np
    
    # reference area
    Aref = np.pi*Rocket.diameters[1]**2/4
    
    # cone
    if Rocket.cone_mode == 'on':
        if alpha == 0:
            CNa_cone = 2
        else:
            CNa_cone = 2*math.sin(alpha)/alpha
    CP_cone = 2/3*Rocket.stage_z[1]
    
    # body
    CNa_stage = np.zeros(Rocket.stages-2,'float')
    CP_stage = np.zeros(Rocket.stages-2,'float')
    for i in range((Rocket.stages-2)):
        if alpha == 0:
            CNa_stage[i] = (Rocket.diameters[i+2]**2-Rocket.diameters[i+1]**2)*np.pi/Aref/2
        else:
            CNa_stage[i] = (Rocket.diameters[i+2]**2-Rocket.diameters[i+1]**2)*np.pi/Aref/2*np.sin(alpha)/alpha
        CP_stage[i] = Rocket.stage_z[i+1]+1/3*(Rocket.stage_z[i+2]-Rocket.stage_z[i+1])*(1+(1-Rocket.diameters[i+1]/Rocket.diameters[i+2])/(1-(Rocket.diameters[i+1]/Rocket.diameters[i+2])**2))
    
    # fins 
    if M < 1:
        beta  = np.sqrt(1-M**2)
    else:
        warnings.warn("Warning: In barrowman calculations Mach number is > 1.",
                      DeprecationWarning, stacklevel=1)
        beta = np.sqrt(M**2-1)
    gamma_c = math.atan(((Rocket.fin_xs+Rocket.fin_ct)/2-Rocket.fin_cr/2)/Rocket.fin_s)
    A = 0.5*(Rocket.fin_ct+Rocket.fin_cr)*Rocket.fin_s
    R=0
    for i in range(Rocket.diameter):
        if Rocket.stage_z[i] < Rocket.fin_xt[i]:
            R = Rocket.diameter[i]/2
    KTB = 1 + R/(R+Rocket.fin_s)
    CNa1 = KTB*2*np.pi*Rocket.fin_s**2/Aref/(1+np.sqrt(1+(beta*Rocket.fin_s**2/A/math.cos(gamma_c))**2))
    CNa_fins = CNa1*np.sum(math.sin(theta+2*np.pi/Rocket.fin_n*np.arange((Rocket.fin_n)))**2+1)
    CP_fins = Rocket.fin_xt + Rocket.fin_xs/3*(Rocket.fin_cr+2*Rocket.fin_ct)/(Rocket.fin_cr+Rocket.fin_ct) + 1/6*((Rocket.fin_cr+Rocket.fin_ct)-(Rocket.fin_cr*Rocket.fin_ct)/(Rocket.fin_cr+Rocket.fin_ct))
    
    # Output
    Calpha = np.array([CNa_stage, CNa_fins])
    CP = np.array([CP_stage, CP_fins])
    if Rocket.cone_mode == 'on':
        Calpha = np.array([CNa_cone, Calpha])
        CP = np.array([CP_cone, CP])
    
    for i in range(len(CP)):
        if np.isnan(CP[i]):
            CP[i]=0
    
    return Calpha, CP
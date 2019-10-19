from termcolor import colored
import math
from scipy import interpolate
import numpy as np
from Functions.Thrust import *

def toFloat(data):
        """
        TODO
        """
        data = list(map(float, data))
        if len(data) == 1:
            data = data[0]
        return data

class Rocket():

    

    def checkStages(self):
        '''
        TODO + check with bad file
        '''
        flag = False
        if not((len(self.diameters) == int(self.stages)) and (len(self.stage_z) == int(self.stages))):
            flag = True
            print(colored('ERROR: In rocket defintion, rocket diameters and/or stage_z are not equal in length to the announced stages.', 'red') )
        elif not((self.diameters[0] == 0) and (self.stage_z[0] == 0)):
            flag = True
            print(colored('ERROR: In rocket defintion, rocket must start with a point (diameters(1) = 0, stage_z(1) = 0)', 'red') )
        return flag


    def addAttribute(self, attribute_name, data):

        if(attribute_name == 'stages'):
            self.stages = toFloat(data)
        elif(attribute_name == 'diameters'):
            self.diameters = toFloat(data)
        elif(attribute_name == 'stage_z'):
            self.stage_z = toFloat(data)
        elif(attribute_name == 'cone_mode'):
            self.cone_mode = data
        elif(attribute_name == 'fin_n'):
            self.fin_n = toFloat(data)
        elif(attribute_name == 'fin_xt'):
            self.fin_xt = toFloat(data)
        elif(attribute_name == 'fin_s'):
            self.fin_s = toFloat(data)   
        elif(attribute_name == 'fin_cr'):
            self.fin_cr = toFloat(data)
        elif(attribute_name == 'fin_ct'):
            self.fin_ct = toFloat(data)
        elif(attribute_name == 'fin_t'):
            self.fin_t = toFloat(data)
        elif(attribute_name == 'fin_xs'):
            self.fin_xs = toFloat(data)
        elif(attribute_name == 'lug_n'):
            self.lug_n = toFloat(data)
        elif(attribute_name == 'lug_S'):
            self.lug_S = toFloat(data)
        elif(attribute_name == 'rocket_m'):
            self.rocket_m = toFloat(data)
        elif(attribute_name == 'rocket_I'):
            self.rocket_I = toFloat(data)
        elif(attribute_name == 'rocket_cm'):
            self.rocket_cm = toFloat(data)
        elif(attribute_name == 'ab_x'):
            self.ab_x = toFloat(data)
        elif(attribute_name == 'ab_n'):
            self.ab_n = toFloat(data)
        elif(attribute_name == 'ab_phi'):
            self.ab_phi = toFloat(data)
        elif(attribute_name == 'motor'):
            self.motor_ID = data[0]
        elif(attribute_name == 'motor_fac'):
            self.motor_fac = toFloat(data)
        elif(attribute_name == 'pl_mass'):
            self.pl_mass = toFloat(data)
        elif(attribute_name == 'para_main_SCD'):
            self.para_main_SCD = toFloat(data)
        elif(attribute_name == 'para_drogue_SCD'):
            self.para_drogue_SCD = toFloat(data)
        elif(attribute_name == 'para_main_event'):
            self.para_main_event = toFloat(data)
        elif(attribute_name == 'cp_fac'):
            self.cp_fac = toFloat(data)
        elif(attribute_name == 'CNa_fac'):
            self.CNa_fac = toFloat(data)
        elif(attribute_name == 'CD_fac'):
            self.CD_fac = toFloat(data)
        else:
            print(colored('ERROR: In rocket definition, unknown rocket attribute: %s' %attribute_name, 'red') )



def rocketReader(rocketFilePath):

    # -------------------------------------------------------------------------
    # 1. Read Rocket
    # -------------------------------------------------------------------------
    rocket = Rocket()

    try:
        rfid = open(rocketFilePath);
    except:
        print(colored('ERROR: Rocket file name unfound.', 'red') )
        return

    line_content = rfid.readline()
    while(line_content):
        line_content = line_content.replace('\n', '').split(" ")

        line_id  = line_content[0]
        line_data = line_content[1:]

        rocket.addAttribute(line_id, line_data)

        line_content = rfid.readline()

    # -------------------------------------------------------------------------
    # 2. Read Motor
    # -------------------------------------------------------------------------

    rfid = open(rocket.motor_ID);

    # 2.1 Read Informations
    line_content = rfid.readline()
    Info = line_content.replace('\n', '').split(" ")
    
    rocket.motor_dia = float(Info[1])/1000;
    rocket.motor_length = float(Info[2])/1000;
    rocket.motor_delay = Info[3];
    rocket.propel_mass = float(Info[4]);
    rocket.motor_mass = float(Info[5]);

    rocket.casing_mass = rocket.motor_mass - rocket.propel_mass;

    # 2.2 Read Thrust Informations
    t = [0]; T = [0]; # Initialization

    line_content = rfid.readline()
    while(line_content):
        line_content = line_content.replace('\n', '').split(" ")[-2:]
        line_content = toFloat(line_content)
        t.append(line_content[0])
        T.append(line_content[1])
        line_content = rfid.readline()

    rocket.Thrust_Time = t;
    rocket.Thrust_Force = T;

    # -------------------------------------------------------------------------
    # 3. Checks
    # -------------------------------------------------------------------------

    if rocket.checkStages():
        print(colored('ERROR: Reading rocket definition file.', 'red'))

    if ((rocket.cone_mode == 'on') or (rocket.cone_mode == 'off')):
        print('ERROR: Cone mode parameter ' + rocket.cone_mode + ' unknown.')

    # -------------------------------------------------------------------------
    # 4. Intrinsic parameters
    # -------------------------------------------------------------------------

    # 4.1 Maximum body diameter
    rocket.dm = max(rocket.diameters)
    # 4.2 Fin cord
    rocket.fin_c = (rocket.fin_cr + rocket.fin_ct)/2; 
    # 4.3 Maximum cross-sectional body area
    rocket.Sm = math.pi*rocket.dm**2/4; 
    # 4.4 Exposed planform fin area
    rocket.fin_SE = (rocket.fin_cr + rocket.fin_ct )/2*rocket.fin_s; 
    # 4.5 Body diameter at middle of fin station
    f = interpolate.interp1d(rocket.stage_z, rocket.diameters, kind='linear')
    rocket.fin_df = f(rocket.fin_xt+rocket.fin_cr/2) 
    # 4.6 Virtual fin planform area
    rocket.fin_SF = rocket.fin_SE + 1/2*rocket.fin_df*rocket.fin_cr; 
    # 4.8 Rocket Length
    rocket.L = rocket.stage_z[-1];
    # 4.9 Burn Time
    rocket.Burn_Time = t[-1];

    # -------------------------------------------------------------------------
    # 5. Mass variation
    # -------------------------------------------------------------------------
    # 5.1 Total Impulse
    tt = np.linspace(0,rocket.Burn_Time,2000)
    # Interpolate thrust
    TT = interpolate.interp1d(rocket.Thrust_Time,rocket.Thrust_Force, kind='linear')(tt)
    A_T = np.trapz(TT,tt) # Area under Thrust Curve

    # 5.2 Total Mass
    rocket.Thrust2dMass_Ratio = rocket.propel_mass/A_T

    return rocket


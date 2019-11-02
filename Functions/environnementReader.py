import math
import csv

#------------------------------------------------------------------------------------
# 0. Create Environnement class
#------------------------------------------------------------------------------------

class Environnement:

    def addAttribute (self, attribute_name, data) :
        if (attribute_name == 'Temperature_Ground') :
            self.Temperature_Ground = float(data)
        elif (attribute_name == 'Pressure_Ground'):
            self.Pressure_Ground = float(data)            
        elif (attribute_name ==  'Humidity_Ground') :
            self.Humidity_Ground = float(data)
        elif  attribute_name == 'V_inf' :
            self.V_inf = float(data)
        elif  attribute_name == 'V_Azimuth':
            self.V_Azimuth = float(data)  
        elif  attribute_name == 'Turb_I':
            self.Turb_I = float(data)
        elif  attribute_name == 'Turb_model':
            self.Turb_model = data
        elif attribute_name ==  'Rail_Length':
            self.Rail_Length = float(data)
        elif  attribute_name == 'Rail_Angle':
            self.Rail_Angle =  float(data)/180*math.pi
        elif  attribute_name == 'Rail_Azimuth':
            self.Rail_Azimuth = float(data)/180*math.pi
        elif  attribute_name == 'Start_Altitude':
            self.Start_Altitude = float(data)
        elif  attribute_name == 'Start_Latitude':
            self.Start_Latitude = float(data)
        elif  attribute_name == 'Start_Longitude':
            self.Start_Longitude = float(data)
        else :
            raise ValueError('ERROR: In environnement definition, unknown line identifier: '+attribute_name)


def environnementReader(environnementFilePath) :
    environnement = Environnement()

# -------------------------------------------------------------------------
# 1. Read Environnement
#  -------------------------------------------------------------------------

    rfid = open(environnementFilePath)
    for line_content in rfid :
        line_id, line_data = line_content.split()
        environnement.addAttribute(line_id, line_data)

    
     
    
# -------------------------------------------------------------------------
# 2. Intrinsic parameters
# -------------------------------------------------------------------------
# 2.1 Environnement Viscosity


    with open('viscosity.csv') as csv_file:

        Tmp = csv.reader(csv_file, delimiter=',')

        environnement.T_Nu =[]
        environnement.Viscosity =[]

        for row in Tmp:

            environnement.T_Nu.append(float(row[0]))
            environnement.Viscosity.append(float(row[1]))
            

            
                
                
#2.2 Humidity Changes

    p_ws = math.e ** (77.345+0.0057*environnement.Temperature_Ground-7235/environnement.Temperature_Ground)/environnement.Temperature_Ground ** 8.2
    p_a = environnement.Pressure_Ground
    environnement.Saturation_Vapor_Ratio = 0.62198*p_ws/(p_a-p_ws)

# 2.3 Wind direction
    environnement.V_dir = [math.degrees(math.cos(environnement.V_Azimuth)),math.degrees(math.sin(environnement.V_Azimuth)), 0]

    return environnement

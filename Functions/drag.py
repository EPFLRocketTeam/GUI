from termcolor import colored
import math
from scipy import interpolate
import numpy as np

def drag(rocket, alpha, Uinf, nu, a):
	'''
	DRAG - Rocket drag calculation function based on Mandell's book "Topics
	 on advanced model Rocketry" (unless otherwise specified). 
	LIMITATIONS:
	 - Isn't usable for very low speeds (<0.1m/s)
	 - Input velocity must be > 0
	INPUTS:
	 - Rocket  : Rocket object
	 - alpha   : angle of attack [rad]
	 - Uinf    : Free stream velocity [m/s]
	 - nu      : Dynamic viscosity [m2/s]
	 - a       : Speed of sound [m/s]
	OUTPUTS:
	 - CD      : Drag coefficient
	REFERENCES:
	 - Gordon K. Mandell, Topics in Advanced Model Rocketry, MIT Press, 1973
	 - Hassan Arif, Identification and Control of a High Power Rocket, EPFL
	   Semester Project Report, Professor Collin Jones, June 2017.
	'''

	# -------------------------------------------------------------------------
	# 0. Divergence 
	# -------------------------------------------------------------------------
	
	if Uinf < 0.1:
	    Uinf = 0.1

	# -------------------------------------------------------------------------
	# 1. Geometrical Parameters
	# -------------------------------------------------------------------------

	dm = rocket.dm; # maximum rocket diameter 
	Sm = rocket.Sm; # maximum cross-sectional body area
	c = rocket.fin_c; # fin cord
	SE = rocket.fin_SE; # Exposed planform fin area
	df = rocket.fin_df; # body diameter at middle of fin station
	SF = rocket.fin_SF; # Virtual fin planform area

	# -------------------------------------------------------------------------
	# 2. Reynolds Numbers (eq 191, p 458)
	# -------------------------------------------------------------------------

	# 2.1 Body 
	Rl = rocket.stage_z[-1]*Uinf/nu; 
	Rl_crit = 5e5;
	# 2.2 Fins
	Rc = c*Uinf/nu; 
	Rc_crit = 5.14e6;
	# Critical values of the Reynolds number are selected as shown in Fig. 51, p.464

	# -------------------------------------------------------------------------
	# 3. Skin Friction Coefficients
	# -------------------------------------------------------------------------

	# 3.1 Body skin friction
	# 3.1.1 turbulent skin friction for a flat plate (eq 102a, p 357)
	Cf_turb_B = 0.074/(Rl)**0.2;
	# 3.1.2 laminar skin friction for a flat plate (eq 102b, p 357)
	Cf_lam_B = 1.328/math.sqrt(Rl); 
	# 3.1.3 transitional flow factor for a flat plate (eq 100, p 356)
	B_B = Rl_crit*(Cf_turb_B - Cf_lam_B);
	# 3.1.4 transitional skin friction for body (eq 101, p 356)
	Cf_turb_B = Cf_turb_B-B_B/Rl; 

	# 3.2 Fin skin friction
	# 3.2.1 turbulent skin friction for a flat plate (eq 102a, p 357)
	Cf_turb_F = 0.074/(Rc)**0.2; 
	# 3.2.2 laminar skin friction for a flat plate (eq 102b, p 357)
	Cf_lam_F = 1.328/math.sqrt(Rc);
	# 3.2.3 transitional flow factor for a flat plate (eq 100, p 356)
	B_F = Rc_crit*(Cf_turb_F - Cf_lam_F); 
	# 3.2.4 transitional skin friction for body (eq 101, p 356)
	Cf_turb_F = Cf_turb_F-B_F/Rc;

	# -------------------------------------------------------------------------
	# 4. 0?? AoA drag
	# -------------------------------------------------------------------------

	# 4.1 Wetted area ratio
	# 4.1.1 ogive cone (eq 171c, p 439)
	# 4.1.2 boattail cone (eq 172a, p 441)
	op1 = list(map(float.__add__,rocket.diameters[1:-1-1], rocket.diameters[2:-1]))[0]
	op2 = list(map(float.__sub__, rocket.stage_z[2:-1], rocket.stage_z[1:-1-1]))[0]
	op3 = list(map(float.__sub__, rocket.diameters[1:-1-1], rocket.diameters[2:-1]))[0]
	op4 = list(map(float.__sub__, rocket.stage_z[2:-1], rocket.stage_z[1:-1-1]))[0]

	SsSm = 2/dm**2*(op1*op2*math.sqrt(1+(op3/2./op4)**2))
	#SsSm = 2/dm^2*sum(a*b*math.sqrt(1+(c/2./d)**2))
	# TODO, QUESTION, op* always scalar?
	# TODO, value different from matlab: should equal 68.3278


	if (rocket.cone_mode == 'on'):
	    SsSm = SsSm + 2.67*rocket.stage_z[1]/dm

	if rocket.stage_z[1]/dm < 1.5:
	    print(colored('WARNING: In drag coefficient calculation, ogive cone ratio is out of bounds. Drag estimation cannot be trusted.','red'));

	
	# 4.2 Body drag
	# 4.2.1 (eq 161, p 431)
	CDf_B = (1+60/(rocket.stage_z[-1]/dm)**3+0.0025*(rocket.stage_z[-1]/dm))*SsSm; # partially calculated body drag
	if Rl < Rl_crit:
	    CDf_B = Cf_lam_B*CDf_B; # body drag for laminar flow
	else:
	    CDf_B = Cf_turb_B*CDf_B; # body drag for turbulent flow
	
	# 4.2.2 Base drag (eq 162, p 431)
	CDb = 0.029*(rocket.diameters[-1]/dm)**3/math.sqrt(CDf_B)
	# 4.2.3 Body drag at 0?? AoA (eq 160, p 431)
	CD0_B = CDf_B +CDb

	# 4.3 Fin drag
	# 4.3.1 Fin drag at 0?? AoA (eq 159, p 433)
	CD0_F = 2*(1+2*rocket.fin_t/c)*rocket.fin_n*SF/Sm
	if Rc < Rc_crit:
	    CD0_F = CD0_F*Cf_lam_F
	else:
	    CD0_F = CD0_F*Cf_turb_F

	# 4.4 Launch lug drag mounted on body (eq 119 p 390)
	# TODO consider launch lugs mounted near fins with a different drag
	# coefficient.
	CD_l = rocket.lug_n*5.75*rocket.lug_S/Sm

	# 4.5 Fin and Body drag at 0 AoA (eq 158, p 430) plus launch lug drag
	CD0_FB = CD0_B + CD0_F + CD_l

	# 4.6 Drag for nosecone failure
	if (rocket.cone_mode == 'off'):
	   CD0_FB = CD0_FB + 1 - CDf_B
	
    # -------------------------------------------------------------------------
	# 5. Drag at AoA
	# -------------------------------------------------------------------------

	# 5.1 Body drag at AoA
	# 5.1.1 factor tables as seen in Fig. 35 and 36 on p. 405
	alpha = abs(alpha);
	etatab=[[4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24],
			[0.6, 0.63, 0.66, 0.68, 0.71, 0.725, 0.74, 0.75, 0.758, 0.77, 0.775]]
	deltaktab=[[4, 6, 8, 10, 12, 14, 16, 18, 20],
		   	   [0.78, 0.86, 0.92, 0.94, 0.96, 0.97, 0.975, 0.98, 0.982]]
	etak = interpolate.interp1d(etatab[0],etatab[1],kind='linear',fill_value="extrapolate")(rocket.stage_z[-1]/dm)
	deltak=interpolate.interp1d(deltaktab[0],deltaktab[1],kind='linear',fill_value="extrapolate")(rocket.stage_z[-1]/dm)

	
	# 5.1.2 Compute body drag at angle of attack alpha
	# 5.1.2.1 x1 as defined by explanations of (eq 140, p 404)

	# order list of indices where diff(rocket.diameters) == 0
	indices = [i for i,x in enumerate(np.diff(rocket.diameters)) if x==0]
	x1 = rocket.stage_z[indices[0]];


	# 5.1.2.2 x0 as in (eq 140, p404)
	x0 = 0.55*x1+0.36*rocket.stage_z[-1];
	
	# 5.1.2.3 Section Area at station x0
	S0 = math.pi*(interpolate.interp1d(rocket.stage_z, rocket.diameters, kind='linear')(x0))**2/4;
	# 5.1.2.4 Body drag at low AoA (eq 139, p. 404)
	
	CDB_alpha = 2*deltak*S0/Sm*alpha*math.sin(alpha);

	# order list of indices where rocket.stage_z>x0
	indices = [i for i,x in enumerate(rocket.stage_z) if x>x0]

	tmp_stages = [x0] + [rocket.stage_z[i] for i,_ in enumerate(indices)]
	tmp_diameters = [interpolate.interp1d(rocket.stage_z, rocket.diameters, kind='linear')(x0)] + [rocket.diameters[i] for i,_ in enumerate(indices)];
	#TODO, vrifier format

	# 5.1.2.4 Body drag at high AoA (eq 142, p. 406)
	op = (tmp_diameters[0: -1-1][0]+tmp_diameters[1:-1][0])/2*(tmp_stages[1:-1][0]-tmp_stages[0:-1-1][0])
	CDB_alpha = CDB_alpha + 2*alpha**2*math.sin(alpha)/Sm*etak*1.2*op;
	# 5.2 Fin drag at AoA
	
	# 5.2.1 Fin Exposed Surface Coefficient
	# TODO: Consider rocket roll for lateral exposed fin surface
	FESC = 2;
	# 5.2.2 induced fin drag, similar to (eq 145, p 413)
	CDi = 1.2*alpha**2*SF/Sm*FESC;
	# 5.2.3 Interference coefficients as estimated by Hassan (eq 34 and 35, p
	# 12) based on Mandell Fig. 40 p 416.
	Rs = df/(2*rocket.fin_s+df); # Total fin span ratio
	KFB = 0.8065*Rs**2+1.1553*Rs; # Interference of body on fin lift
	KBF = 0.1935*Rs**2+0.8174*Rs+1; # Interference of fins on body lift
	# 5.2.4 Interference Drag Coefficient (eq 146, p 415)
	DCDi = (KFB + KBF - 1)*3.12*SE/Sm*alpha**2*FESC; # Interference drag
	CDF_alpha = CDi + DCDi;

	# 5.3 Total drag at AoA (eq 148, p 417)
	CD_alpha = CDB_alpha + CDF_alpha;
	
	# -------------------------------------------------------------------------
	# 7. Drag of tumbeling body (c.f. OpenRocket Documentation section 3.5)
	# -------------------------------------------------------------------------
	fin_efficiency = [0.5, 1, 1.5, 1.41, 1.81, 1.73, 1.9, 1.85];
	CD_t_fin = 1.42*fin_efficiency[int(rocket.fin_n)-1];
	CD_t_body = 0.56;

	CD_t = (SE*CD_t_fin+CD_t_body*dm*(rocket.stage_z[-1]-rocket.stage_z[1]))/Sm;
	
	# -------------------------------------------------------------------------
	# 6. Subsonic drag coefficient
	# -------------------------------------------------------------------------
	CD = CD0_FB + CD_alpha;
	# the calculated drag can't be more than the lateral drag of a tumbling
	# body so it is cut-off to that value if it is larger. 
	if CD > CD_t:
	    CD = CD_t

    # -------------------------------------------------------------------------
	# 7. Compressible flow correction factor (for a sharp nose) (eq 214, p 482)
	# -------------------------------------------------------------------------
	M = Uinf/a;
	if M>0.9 and M<=1.05:
	    CD = CD*(1 + 35.5*(M-0.9)**2)
	elif M > 1.05 and M <=2:
	    CD = CD*(1.27+0.53*exp(-5.2*(M-1.05)))
	elif M > 2 and not(M<=0.9):
	    print(colored('WARNING: In drag calculation, Mach number exceeds validity range.', 'red'))

	return CD
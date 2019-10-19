import math
from scipy import interpolate
import numpy as np
#inutile pour le moment (20/10/19) car utilisation du microcontrolleur à la place 
def bisection(x10,x20,x1o,x2o,Environment,Rocket):


    [useless1, a, useless2, rho, nu] = stdAtmos(x10,Environment);
    CD0=drag(Rocket,0,x20,nu,a);
    CD_ABouv=drag_shuriken(Rocket,-18.5,0, x20, nu);
    CD_ABferm=drag_shuriken(Rocket,-190.5,0, x20, nu);
    Mdry=26.13; 
    A=-9.81;
    b=-0.5*rho*Rocket.Sm*(CD0+CD_ABferm)/Mdry;
    a=-0.5*rho*Rocket.Sm*(CD0+CD_ABouv)/Mdry;
    
    f= lambda B : 0.5*(log((1+x2o**2 *(B/A))/(1+x20**2 *(B/A))))/(x1o-x10);
    #f=@(B)0.5*(log((1+x2o.^2*(B/A)*(rho(x1o)/rho(x10)))/(1+x20.^2*(B/A)*(rho(x1o)/rho(x10)))))./(x1o-x10);
    boul=1;
    true=0;
    # b=-1.3463e-04;
    # a=-1.3463e-04*(0.211635445781990+0.3394)/(0.015061977625056+0.3394);
    if ((f(a)-a)*(f(b)-b)<0):
        
      while (b-a)>1e-8:
     
        m=(a+b)*0.5;
        fm=f(m)-m;
        if f(a)<a & f(b)>b:
            if fm<0:
                a=m;
        
        if fm>0:
            b=m;
        
        
        if f(b)<b & f(a)>a:
            if fm<0:
                b=m;
            
        if fm>0:
            a=m;
         
    m=(a+b)*0.5;
    if ((f(a)-a)*(f(b)-b)>0) :
            boul=0;
            m=NaN;
    
    return [m,boul]

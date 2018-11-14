# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:43:16 2016

@author: Minghui GUAN
"""

import math
import numpy as np
#numpy._version_
import matplotlib.pyplot as plt
#matplotlib._version_
from mpl_toolkits.mplot3d import Axes3D

# Masse (10**24 kg), Diamètre (km), Densité (kg/m3), Période de rotation (heures)
# Distance au soleil (10**6 km), Périhélie (10**6 km), Aphélie (10**6 km)
# Période orbitale (jours), Inclinaison de l’orbite (degrés), Excentricité de l’orbite

dict_planetes = {}
dict_planetes['mercury'] = [0.330, 4879/2, 57.9, 88.0, 46.0, 69.8, 0.205, 7.0]
dict_planetes['venus'] = [4.87, 12104/2, 108.2, 224.7, 107.5, 108.9, 0.007, 3.4]
dict_planetes['earth'] = [5.97, 12756/2, 149.6, 365.2, 147.1, 152.1, 0.017, 0.0]
dict_planetes['mars'] = [0.642, 6792/2, 227.9, 687.0, 206.6, 249.2, 0.094, 1.9]
dict_planetes['jupiter'] = [1898, 142984/2, 778.6, 4331, 740.5, 816.6, 0.049, 1.3]
dict_planetes['saturn'] = [568, 120536/2, 1433.5, 10747, 1352.6, 1514.5, 0.057, 2.5]
dict_planetes['uranus'] = [86.8, 51118/2, 2872.5, 30589, 2741.3, 3003.6, 0.046, 0.8]
dict_planetes['neptune'] = [102, 49528/2, 4495.1, 59800, 4444.5, 4545.7, 0.011, 1.8]
dict_planetes['pluto'] = [0.0146, 2370/2, 5906.4, 90560, 4436.8, 7375.9, 0.244, 17.2]

dt = 0.01/365
M = 1
G = 39.47

N=70000

def getmass(clef):
    return dict_planetes[clef][0]
    
def getrayon(clef):
    return dict_planetes[clef][1]
    
def getdistance(clef):
    return dict_planetes[clef][2]
    
def getperiode(clef):
    return dict_planetes[clef][3]    

def getperihelie(clef):
    return dict_planetes[clef][4]

def getaphelie(clef):
    return dict_planetes[clef][5]    
    
def getexcentricite(clef):
    return dict_planetes[clef][6]    
    
def getinclinaison(clef):
    return dict_planetes[clef][7]    
    
def help():
    print 'dictionnaire de planetes'
    print 'getmass() : pour récupérer la masse de la planète'
    print 'getrayon() : pour récupérer le rayon de la planète'
    print 'getdistance() : pour récupérer la distance de la planète au soleil'

def inter_euler(dt, position, vitesse, force_grav):
    
    v_newx = vitesse[0] + dt*force_grav(position)[0]
    v_newy = vitesse[1] + dt*force_grav(position)[1]
    v_newz = vitesse[2] + dt*force_grav(position)[2]
    x_new = position[0] + dt*vitesse[0]
    y_new = position[1] + dt*vitesse[1]
    z_new = position[2] + dt*vitesse[2]

    return [x_new, y_new, z_new, v_newx, v_newy, v_newz]
    
def force_grav(position):
    
    R = (position[0]**2+position[1]**2+position[2]**2)**(0.5)
    F = -G*M/(R**2)
    Fx = F * position[0]/R
    Fy = F * position[1]/R
    Fz = F * position[2]/R
    
    return [Fx, Fy, Fz, R]
    
def calcule_orbite(clef, dt):
    
    x = [0]*(N+1)
    y = [0]*(N+1)
    z = [0]*(N+1)
    vx =[0]*(N+1)
    vy = [0]*(N+1)
    vz = [0]*(N+1)    
    
    x[0] = getdistance(clef)/149.6*(1+getexcentricite(clef))*math.cos(getinclinaison(clef))
    z[0] = getdistance(clef)/149.6*(1+getexcentricite(clef))*math.sin(getinclinaison(clef))
    vy[0] = 2.0*math.pi*math.sqrt((1-getexcentricite(clef))/(1+getexcentricite(clef)))*math.cos(getinclinaison(clef))/((getdistance(clef)/149.6)**0.5)
    vz[0] = 2.0*math.pi*math.sqrt((1-getexcentricite(clef))/(1+getexcentricite(clef)))*math.sin(getinclinaison(clef))/((getdistance(clef)/149.6)**0.5)

    for i in range (0, 70000):

        p = inter_euler(dt, [x[i],y[i],z[i]], [vx[i],vy[i],vz[i]], force_grav)    
        x[i+1] = p[0]
        y[i+1] = p[1]
        z[i+1] = p[2]
        vx[i+1] = p[3]
        vy[i+1] = p[4]
        vz[i+1] = p[5]
    
    x.pop()
    y.pop()
    z.pop()
    orbite = [x, y, z]
    
    return orbite

fig = plt.figure()
ax = fig.gca(projection='3d')

mercury = calcule_orbite('mercury', dt)
ax.plot(mercury[0], mercury[1], mercury[2], color="blue", label="mercury")
ax.legend()

venus = calcule_orbite('venus', dt)
ax.plot(venus[0], venus[1], venus[2], color="red", label="venus")
ax.legend()

earth = calcule_orbite('earth', dt)
ax.plot(earth[0], earth[1], earth[2], color="magenta", label="earth")
ax.legend()

mars = calcule_orbite('mars', dt)
ax.plot(mars[0], mars[1], mars[2], color="green", label="mars")
ax.legend()

'''jupiter = calcule_orbite('jupiter', dt)
ax.plot(jupiter[0], jupiter[1], jupiter[2], color="black", label="jupiter")
ax.legend()

saturn = calcule_orbite('saturn', dt)
ax.plot(saturn[0], saturn[1], saturn[2], color="yellow", label="saturn")
ax.legend()

uranus = calcule_orbite('uranus', dt)
ax.plot(uranus[0], uranus[1], uranus[2], color="cyan", label="uranus")
ax.legend()

neptune = calcule_orbite('neptune', dt)
ax.plot(neptune[0], neptune[1], neptune[2], color="blue", linestyle="--", label="neptune")
ax.legend()

pluto = calcule_orbite('pluto', dt)
ax.plot(pluto[0], pluto[1], pluto[2], color="red", linestyle="-.", label="pluto")
ax.legend()'''

plt.title('trace3D')
      
plt.show()
    

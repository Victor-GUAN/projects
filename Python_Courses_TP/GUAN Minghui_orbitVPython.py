# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 23:01:41 2016

@author: Minghui GUAN
"""

from visual import *
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

N=70000

Terre=sphere()
Soleil=sphere()
Orbit = [(0,0,0)]*(N+1)

Terre.radius= 6371/(149.6*(10**6))
Terre.color=color.blue

Soleil.radius= 695700/(149.6*(10**6))
Soleil.color=color.yellow
Soleil.pos = (0,0,0)

dt = 0.01/365
M = 1
G = 39.47
e = 0.017
theta=0

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
    
x = [0]*(N+1)
y = [0]*(N+1)
z = [0]*(N+1)
vx =[0]*(N+1)
vy = [0]*(N+1)
vz = [0]*(N+1)

x[0] = 1 + e

vy[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.cos(theta)
vz[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.sin(theta)

for i in range (0, 70000):

    p = inter_euler(dt, [x[i],y[i],z[i]], [vx[i],vy[i],vz[i]], force_grav)    
    x[i+1] = p[0]
    y[i+1] = p[1]
    z[i+1] = p[2]
    vx[i+1] = p[3]
    vy[i+1] = p[4]
    vz[i+1] = p[5]
    
for i in range (0, 70000):
    
    Terre.pos = (x[i],y[i],z[i])
    Terre
    Orbit[i] = (x[i],y[i],z[i])

del Orbit[70000]

curve(pos=Orbit, color=color.green)
    

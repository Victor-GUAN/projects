# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:11:24 2016

@author: Minghui GUAN
"""

import math
import numpy as np
#numpy._version_
import matplotlib.pyplot as plt
#matplotlib._version_
from mpl_toolkits.mplot3d import Axes3D

dt = 0.01/365
M = 1
G = 39.47
e = 0.017
theta=0

def inter_euler(dt, position, vitesse, force_grav):
    #t[i+1] = t[i] + dt
    v_newx = vitesse[0] + dt*force_grav(position)[0]
    v_newy = vitesse[1] + dt*force_grav(position)[1]
    v_newz = vitesse[2] + dt*force_grav(position)[2]
    x_new = position[0] + dt*vitesse[0]
    y_new = position[1] + dt*vitesse[1]
    z_new = position[2] + dt*vitesse[2]
    #E[i] = 0.5*M*(vx[i]**2+vy[i]**2+vz[i]**2)-G*M/R[i]
    return [x_new, y_new, z_new, v_newx, v_newy, v_newz]
    
def force_grav(position):
    R = (position[0]**2+position[1]**2+position[2]**2)**(0.5)
    F = -G*M/(R**2)
    Fx = F * position[0]/R
    Fy = F * position[1]/R
    Fz = F * position[2]/R
    return [Fx, Fy, Fz, R]
    
def orbit_frame_change_pos(from_namereferentiel,to_namereferentiel,from_pos):
    if from_namereferentiel=='heliocentric' and to_namereferentiel=='geocentric':
        to_pos=[-from_pos[0],-from_pos[1],-from_pos[2]]
    return to_pos        
    
def orbit_frame_change_vit(from_namereferentiel,to_namereferentiel,from_vit):
    if from_namereferentiel=='heliocentric' and to_namereferentiel=='geocentric':
        to_vit=[-from_vit[0],-from_vit[1],-from_vit[2]]
    return to_vit        
    
N=70000   
x = [0]*(N+1)
y = [0]*(N+1)
z = [0]*(N+1)
vx =[0]*(N+1)
vy = [0]*(N+1)
vz = [0]*(N+1)
D = [0]*(N+1)
E = [0]*(N+1)

x[0] = 1 + e
D[0] = x[0]

vy[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.cos(theta)
vz[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.sin(theta)

t = [0]*(N+1)

for i in range (0, 70000):

    #t[i+1] = t[i] + dt
    p = inter_euler(dt, [x[i],y[i],z[i]], [vx[i],vy[i],vz[i]], force_grav)    
    x[i+1] = p[0]
    y[i+1] = p[1]
    z[i+1] = p[2]
    vx[i+1] = p[3]
    vy[i+1] = p[4]
    vz[i+1] = p[5]
    D[i+1] = force_grav([x[i+1],y[i+1],z[i+1]])[3]
    E[i] = 0.5*M*(vx[i]**2+vy[i]**2+vz[i]**2)-G*M/force_grav([x[i],y[i],z[i]])[3]

for i in range (0,70001):
    x[i] = orbit_frame_change_pos('heliocentric', 'geocentric', [x[i],y[i],z[i]])[0]
    y[i] = orbit_frame_change_pos('heliocentric', 'geocentric', [x[i],y[i],z[i]])[1]
    z[i] = orbit_frame_change_pos('heliocentric', 'geocentric', [x[i],y[i],z[i]])[2]
    vx[i] = orbit_frame_change_vit('heliocentric', 'geocentric', [vx[i],vy[i],vz[i]])[0]
    vy[i] = orbit_frame_change_vit('heliocentric', 'geocentric', [vx[i],vy[i],vz[i]])[1]
    vz[i] = orbit_frame_change_vit('heliocentric', 'geocentric', [vx[i],vy[i],vz[i]])[2]
    
del E[70000]

fig = plt.figure()

plt.subplot(221)
plt.plot(x, y)
plt.title('trace2D')

plt.subplot(222)
p = np.arange(N)
ylim(-19.8, -19.6)
plt.plot(p,E)
plt.title('Energie')


plt.subplot(223)
p=np.append(p,N)
#p = np.arange(N+1)
plt.plot(p, z)
plt.title('Z')

'''fig = plt.figure()
p = np.arange(N+1)
plt.plot(p,z)
plt.title('Z')'''

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z)
ax.legend()
plt.title('trace3D')

fig = plt.figure()
ax = fig.gca(projection='3d')
x.pop()
y.pop()
ax.plot(x, y, E)
ax.legend()
plt.title('Energie / Trace')

D.pop()
n=D.index(min(D))
print n, D[n]

for j in range (1, 700):
    if x[j*100]>=1.0165 and y[j*100]>=-0.01 and y[j*100]<=0.01 :
        print j
        
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 15:14:56 2016

@author: Minghui GUAN
"""

import math
import numpy as np
#numpy._version_
import matplotlib.pyplot as plt
#matplotlib._version_
from mpl_toolkits.mplot3d import Axes3D

M = 1
N=70000
G = 39.47
e = 0.017
theta=0

F = [0]*(N+1)
Fx = [0]*(N+1)
Fy = [0]*(N+1)
Fz = [0]*(N+1)
x = [0]*(N+1)
y = [0]*(N+1)
z = [0]*(N+1)
vx =[0]*(N+1)
vy = [0]*(N+1)
vz = [0]*(N+1)
R = [0]*(N+1)
E = [0]*(N+1)

x[0] = 1 + e

vy[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.cos(theta)
vz[0] = 2.0*math.pi*math.sqrt((1-e)/(1+e))*math.sin(theta)

dt = 0.01/365

t = [0]*(N+1)

for i in range (0, 70000):
    (R[i]) = ((x[i])**2+(y[i])**2+(z[i])**2)**(0.5)
    F[i] = -G*M/(R[i]**2)
    Fx[i] = F[i] * x[i]/R[i]
    Fy[i] = F[i] * y[i]/R[i]
    Fz[i] = F[i] * z[i]/R[i]
    t[i+1] = t[i] + dt
    vx[i+1] = vx[i] + dt*Fx[i]
    vy[i+1] = vy[i] + dt*Fy[i]
    vz[i+1] = vz[i] + dt*Fz[i]
    x[i+1] = x[i] + dt*vx[i]
    y[i+1] = y[i] + dt*vy[i]
    z[i+1] = z[i] + dt*vz[i]
    E[i] = 0.5*M*(vx[i]**2+vy[i]**2+vz[i]**2)-G*M/R[i]

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

R.pop()
n=R.index(min(R))
print n, R[n]

for j in range (1, 700):
    if x[j*100]>=1.0165 and y[j*100]>=-0.01 and y[j*100]<=0.01 :
        print j
        
plt.show()



    


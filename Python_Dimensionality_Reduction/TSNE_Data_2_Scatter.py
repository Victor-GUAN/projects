# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:57:59 2017

@author: MGN11
"""

import numpy as np
from sklearn.manifold import TSNE
import csv
import matplotlib.pyplot as plt

#   import the initial data
with open('E:\\DerivedObjects_pixels_grey.tsv') as file:
    data = file.read().split('\n')
   
Z=[];a=[];b=[];
Z=np.delete([line.rstrip('\n').split('\t') for line in data],-1,axis=0)
Z= [[float(b) for b in a[:-1]] for a in Z]

#X=np.zeros([len(data)-1,len(data[0].split('\t'))-1])
#
#for i in range(len(data)-1):
#    Y=np.delete(data[i].split('\t'),-1,axis=0)
#    for j in range(len(Y)):
#        X[i][j]=float(Y[j])
        
        
#   reduction of dimension with TSNE      
model = TSNE(n_components=2, perplexity=5, learning_rate=100.0, n_iter=200, random_state=0)
np.set_printoptions(suppress=True)
Y=model.fit_transform(Z)

c=[];d=[];
  
plt.scatter([c[0] for c in Y],[d[1] for d in Y], c='blue',alpha=0.8, edgecolors='white' )
plt.grid(True)
plt.legend()
plt.show()

#   output the new data
#with open('E:\\reduction_Buggy.csv','wb') as file:
#   newdata = csv.writer(file, dialect='excel')
#   for i in range(len(Y)):
#       newdata.writerow(Y[i])
    

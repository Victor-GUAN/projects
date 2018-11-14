# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:57:59 2017

@author: MGN11
"""

import t_sne
import csv
import numpy as np
import json

from t_sne import *
import numpy

#   save the full numpy array without ellipsis
numpy.set_printoptions(threshold=numpy.nan)

#   import the initial data
with open('E:\\DerivedObjects_pixels_grey.tsv') as file:
    data = file.read().split('\n')  
Z=[];
Z=np.delete([line.rstrip('\n').split('\t') for line in data],-1,axis=0)
Z= [[float(b) for b in a[:-1]] for a in Z]

                
#   reduction of dimension with TSNE      
model = TSNE(n_components=2, perplexity=5, learning_rate=125.0, n_iter=1000, random_state=0, step = 25)
Y, set_TSNE, Dict_TSNE = model.fit_transform(Z)

#   the output is respectively Y - the final coordinates ; set_TSNE - the list of coordinates for different step
#   Dict_TSNE - the dictionary of coordinates for different step

#   transform the data type of dictionary for the problem of serializable output
for key in Dict_TSNE:
    Dict_TSNE[str(key)] = str(Dict_TSNE[str(key)])

#   output the new data with the type of dictionary

with open(r'E:/Dassault/3.8/json_Buggy/Dict_TSNE_LR=125_iter=1000.json', 'w') as outfile:
    json.dump(Dict_TSNE, outfile, indent=4, sort_keys=True)


#with open('E:\\reduction_Buggy_iter.csv','wb') as file:
#   newdata = csv.writer(file, dialect='excel')
#   for i in range(len(Y)):
#       newdata.writerow(Y[i])
    

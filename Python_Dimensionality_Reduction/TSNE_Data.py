# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 01:46:28 2017

@author: Minghui GUAN
"""

import numpy as np
from sklearn.manifold import TSNE
import csv
#import pandas as pd
from pandas import DataFrame

data = DataFrame.from_csv('E:\\206_pixels_grey_scat.tsv', sep='\t')

#data.split('\n')
#with open('F:\\DerivedObjects_pixels_grey.tsv') as file:
#    data = file.read().split()
#    for element in data:
#        print (element)
#        break
#X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])

#data = data.fillna(method='ffill')
#print data.isnull().any()
#print data.values

X=np.delete(data.values,-1,axis=1)

print X.max(), X.min()

print np.any(np.isnan(X))
print np.all(np.isfinite(X))

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
Y=model.fit_transform(X)
print Y

with open('E:\\optimization.csv','wb') as file:
   donnees = csv.writer(file, dialect='excel')
   for i in range(len(Y)):
       donnees.writerow(Y[i])

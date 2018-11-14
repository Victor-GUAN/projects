# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 01:10:58 2017

@author: Minghui GUAN
"""


a=[]
a=[line.rstrip('1') for line in ['123132141','285212101','5654681']]

b=[]
b=[c for c in [[1,2,3],[3,2,1],[4,5,6]]]
print b[0]

import numpy as np

#   import the initial data
with open('F:\\DerivedObjects_pixels_grey.tsv') as file:
    data = file.read().split('\n')

X=[]
X=np.delete([line.rstrip('\n').split('\t') for line in data],-1,axis=0)
a=[]
b=[]
X= [[float(b) for b in a[:-1]] for a in X]
        
Y=np.load('F:\\Buggy_TSNE.npy')
#Y=np.delete(data[i].split('\t'),-1,axis=0)
# -*- coding: utf-8 -*-
"""
@author: Minghui GUAN
"""
'''
This script is used to generate a json file after the reduction of dimension with TSNE methode.
TSNE file is modified to extract each iteration we want step by step.

'''

import json
import numpy as np
import collections
import time

import t_sne
import numpy as np
from t_sne import *
import numpy

#   save the full numpy array without ellipsis
numpy.set_printoptions(threshold=numpy.nan)

# documents paths

# 206
"""input_list=r'E:/206/list_small_icons.lst'
directory=r'E:/206'
root_path="DerivedObj/"
input_path='E:/206/206_coordoonees/206_pixels_grey_scat32_100.tsv'
output_path=r'E:/Dassault/3.10/3.10/JS_TSNE_3.10/206_PCA_graph.json_version_0.9_iter.json'"""

# Buggy
input_list=r'E:/Buggy/buggy_small_icons.lst'
directory=r'E:/Graph Visualization Tool/data'
root_path="Buggy/"
input_path=r'\\LW5-MBS3-DSY\apprentissage\Victor\experiments\embedding-projector-standalone-master\oss_data\DerivedObjects_pixels_grey_scat_100_32.tsv'
output_path=r'E:/Dassault/3.10/3.10/JS_TSNE_3.10/Buggy_PCA_graph.json_version_0.9_iter.json'


#   import the initial data
with open(input_path) as file:
    data = file.read().split('\n')  
Z=[];
Z=np.delete([line.rstrip('\n').split('\t') for line in data],-1,axis=0)
Z= [[float(b) for b in a[:-1]] for a in Z]
                
#   reduction of dimension with TSNE      
model = TSNE(n_components=2, perplexity=5, learning_rate=100, n_iter=2000, init = 'pca', random_state = 0, step = 25)
Y, set_TSNE, Dict_TSNE = model.fit_transform(Z)
print Y
#   the output is respectively Y - the final coordinates ; set_TSNE - the list of coordinates for different step
#   Dict_TSNE - the dictionary of coordinates for different step

####################################################################
#   generate the final json
             
class Node(object):
    def __init__(self, id, name, source, level, x, y):
        self.id = id
        self.name = name
        self.source = source
        self.level = level      
        self.x = x
        self.y = y
        
Nodes=[]
NodesDictionary={}
X=[[]]
    
step = int(Dict_TSNE['step'])   

data_size=len(Dict_TSNE)

#   create a list in which each element is a array of coordinates for different step
                    
X[0]=Dict_TSNE[str(step)]
for i in range (2,data_size):
    Y=[[]]
    Y[0]= Dict_TSNE[str(step*i)]
    X.extend(Y)
    
#   creat the output file json    

list_images=[]
if input_list != None:
	list_images = [line.rstrip('\n') for line in open(input_list)]
	
batch_size=len(list_images)

for i in range(batch_size):
    id=list_images[i].split('/')[1]
    name=list_images[i].split('/')[0]
    source=root_path + list_images[i]
    Nodes.append(Node(id, name, source, 0, X[0][i][0], X[0][i][1]))

for i in range(batch_size):
	D = {"level": 0, "name": Nodes[i].name, "img": Nodes[i].source}
	NodesDictionary.setdefault(Nodes[i].id, D)
    
### 	creat a ordered dictionary    
Dict = collections.OrderedDict()

#   max and min of the coordinates
List_X = [] ; List_Y = []
for j in range (1, data_size) :
    for i in range (batch_size) :
        List_X.append(X[j-1][i][0])
        List_Y.append(X[j-1][i][1])
max_X = max(List_X); min_X = min(List_X)
max_Y = max(List_Y); min_Y = min(List_Y)

#   construct the structure of "_ALL"
Dict.setdefault("_ALL", {
                          "step" : step,
                          "extreme" : [min_X*100,min_Y*100,max_X*100,max_Y*100],
                          "bbox" : {"tSNE":[min_X*100,min_Y*100, (max_X-min_X)*100, (max_Y-min_Y)*100]},
                          "nodes": NodesDictionary,
                          "dataFolder": directory,
                          "filters": ["type","linkType"]
                          })
                          
#   construct the structure of each iteration
for j in range (1, data_size) :
    
    Nodes=[]
    NodesDictionary={}
    
    for i in range(batch_size):
        id=list_images[i].split('/')[1]
        name=list_images[i].split('/')[0]
        source=root_path + list_images[i]
        Nodes.append(Node(id, name, source, 0, X[j-1][i][0], X[j-1][i][1]))

    for i in range(batch_size):
        D = {"coord": {"tSNE": [Nodes[i].x*100, Nodes[i].y*100]}}
        NodesDictionary.setdefault(Nodes[i].id, D)
    
    Dict.setdefault("iter"+str(j*step), {
                          "nodes": NodesDictionary,
                          "filters": ["type","linkType"]
                          })
 

print Dict.keys()
    
JsonFile={"date": time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())), 
          "version": 0.9,
          "graphs":  Dict
          }


#       output the file json	
with open(output_path, 'w') as outfile:
    json.dump(JsonFile, outfile, indent=4)

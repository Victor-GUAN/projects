# -*- coding: utf-8 -*-
"""
@author: Minghui GUAN
"""

import json
import numpy as np
import collections
                 
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

#   input the data of dictionary
with open(r'E:/Dassault/3.8/json_Buggy/Dict_TSNE_LR=125_iter=1000.json', 'r') as f:
     data = json.load(f)
     
step = int(data['step'])   

#   transform the data type of dictionary from string to array
for key in data :   
    if (key != 'step'):
        data1 = data[str(key)][1:-1]
        data2 =  data1.split('\n')
        for i in range(len(data2)):
            data2[i]=data2[i].strip().lstrip('[').rstrip(']').strip().split()
            data2[i][0]=float(data2[i][0])
            data2[i][1]=float(data2[i][1])
         
        data[str(key)] = np.array(data2)

data_size=len(data)

#   ceart a list in which each element is a array of coordinates for different step
                    
X[0]=data[str(step)]
for i in range (2,data_size):
    Y=[[]]
    Y[0]= data[str(step*i)]
    X.extend(Y)
    
#   creat the output file json    
input_list=r'E:/buggy_small_icons.lst'
directory=r'E:/Graph Visualization Tool/data'
list_images=[]
if input_list != None:
	list_images = [line.rstrip('\n') for line in open(input_list)]
	
batch_size=len(list_images)

for i in range(batch_size):
    id=list_images[i].split('/')[1]
    name=list_images[i].split('/')[0]
    source='Buggy/'+list_images[i]
    Nodes.append(Node(id, name, source, 0, X[0][i][0], X[0][i][1]))

for i in range(batch_size):
	D = {"level": 0, "name": Nodes[i].name, "img": Nodes[i].source}
	NodesDictionary.setdefault(Nodes[i].id, D)
    
#	creat a ordered dictionary    
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
        source='Buggy/'+list_images[i]
        Nodes.append(Node(id, name, source, 0, X[j-1][i][0], X[j-1][i][1]))

    for i in range(batch_size):
        D = {"coord": {"tSNE": [Nodes[i].x*100, Nodes[i].y*100]}}
        NodesDictionary.setdefault(Nodes[i].id, D)
    
    Dict.setdefault("iter"+str(j*step), {
                          "nodes": NodesDictionary,
                          "dataFolder": directory,
                          "filters": ["type","linkType"]
                          })
 
#def sortedDictValues(adict): 
#    keys = adict.keys()
#    keys.remove('_ALL')    
#    for j in range(len(keys)-1,0,-1):
#        for i in range(0, j):
#            if float(keys[i].lstrip("iter")) > float(keys[i+1].lstrip("iter")):
#                keys[i], keys[i+1] = keys[i+1], keys[i]
#    keys.insert(0,'_ALL')
#    return keys

print Dict.keys()
    
JsonFile={"date": "Wednesday March 7 10:03:25 2017", 
          "version": 0.9,
          "graphs":  Dict
          }


#       output the file json	
with open(r'E:/Dassault/3.8/json_Buggy/Buggy_TSNE_graph.json_version_0.9_iter_LR=125_iter=1000.json', 'w') as outfile:
    json.dump(JsonFile, outfile, indent=4)

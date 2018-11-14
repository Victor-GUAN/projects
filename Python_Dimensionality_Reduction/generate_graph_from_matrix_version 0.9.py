import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import math
                 
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
X=np.load(r'E:/Buggy_TSNE.npy')
input_list=r'E:/buggy_small_icons.lst'
directory=r'E:/Graph Visualization Tool/data'
list_images=[]
if input_list != None:
	list_images = [line.rstrip('\n') for line in open(input_list)]
else:
	list_images.append(input_image)
	
batch_size=len(list_images)

for i in range(batch_size):
    id=list_images[i].split('/')[1]
    name=list_images[i].split('/')[0]
    source='Buggy/'+list_images[i]
    Nodes.append(Node(id, name, source, 0, X[i][0], X[i][1]))

for i in range(batch_size):
	D= {"level": 0, "name": Nodes[i].name, "img": Nodes[i].source, "coord": {"tSNE": [Nodes[i].x*100, Nodes[i].y*100]}}
	NodesDictionary.setdefault(Nodes[i].id, D)


# add nodes with hirarchical clustering 
#with open('state1_tsne_scat2.json', 'r') as f:
#     data = json.load(f)
     
JsonFile={"date": "Thursday Feb 16 11:03:25 2017", 
          "version": 0.9,
          "graphs": {
                  "_ALL": {
                          "nodes": NodesDictionary,
                          "dataFolder": directory,
                          "filters": ["type","linkType"]
                          }
                     }
          }

	
with open(r'E:/Buggy_TSNE_graph.json_version_0.9.json', 'w') as outfile:
    json.dump(JsonFile, outfile, indent=4, sort_keys=True)

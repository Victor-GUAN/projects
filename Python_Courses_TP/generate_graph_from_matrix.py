import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import math
                 
class Node(object):
    def __init__(self, id, name, level, x, y):
        self.id = id
        self.name = name
        self.level = level      
        self.x = x
        self.y = y
        
Nodes=[]
NodesDictionary=[]
X=np.load('F:\\Buggy_TSNE.npy')
input_list='F:\\buggy_small_icons.lst'
#directory='/data/DerivedObj/'
list_images=[]
if input_list != None:
	list_images = [line.rstrip('\n') for line in open(input_list)]
else:
	list_images.append(input_image)
	
batch_size=len(list_images)



for i in range(batch_size):
	id=list_images[i].split('/')[1]
	name=list_images[i].split('/')[0]
	Nodes.append(Node(id, name, 0, X[i][0], X[i][1]))

for i in range(batch_size):
	D= {"level": 0, "id": Nodes[i].id, "name": Nodes[i].name,"coord": {"tSNE": [Nodes[i].x, Nodes[i].y]}}
	NodesDictionary.append(D)


# add nodes with hirarchical clustering 
#with open('state1_tsne_scat2.json', 'r') as f:
#     data = json.load(f)
     
JsonFile={"date": "Tuesday Jan 10 10:41:21 2017", "nodes": NodesDictionary}

	
with open('F:\\Buggy_pixels_grey_scat_graph.json', 'w') as outfile:
    json.dump(JsonFile, outfile)

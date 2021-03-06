# -*- coding: utf-8 -*-
"""get_features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19I23zRcjUD6KADVlgoKubWQFNbbyY1uX
"""

# -*- coding: utf-8 -*-
import os
import codecs
def readfile(filename):
	#current_path=os.path.abspath(os.curdir)
	file_path=os.path.join("/content/drive/My Drive",filename)
	if not os.path.exists(file_path):
		print("error:file not found:"+filename)
		return ""
	f=codecs.open(file_path,"r","utf-8")
	s=f.read()
	f.close()
	return s
test_data=readfile("test-public.txt")
test_data=test_data.splitlines()
print("length of testing data:"+str(len(test_data)))
train_data=readfile("train.txt")
train_data=train_data.splitlines()
print("length of training data:"+str(len(train_data)))

from google.colab import drive
drive.mount('/content/drive')

"""# Graph

## Train data
"""

import numpy as np
positive_train = np.load("/content/drive/My Drive/positive_train.npy").tolist()
negative_train = np.load("/content/drive/My Drive/negative_train.npy").tolist()

print(positive_train[0:10])

"""## Test data"""

del test_data[0]

test_edges = []
for temp_str in test_data:
  temp = temp_str.split('\t')
  temp_list=[]
  temp_list.append(int(temp[1]))
  temp_list.append(int(temp[2]))
  test_edges.append(temp_list)

print(test_edges[0:10])

"""## Get undirected graph"""

# ## unsuccessful
# import networkx as nx

# edge_list = []
# import networkx as nx
# G = nx.Graph()
# for temp_str in train_data:
#   temp=temp_str.split('\t')
#   for i in range(1, len(temp)):
#     temp_edge = (int(temp[0]), int(temp[i]))
#     edge_list.append(temp_edge)
# G.add_edges_from(edge_list)

##successful
import networkx as nx

G=nx.Graph()
for temp_str in train_data:
  temp=temp_str.split('\t')
  temp_list=[int(i) for i in temp]
  temp_edges=[(temp_list[0], temp_list[i]) for i in range(1, len(temp_list))]
  G.add_edges_from(temp_edges)

print('number of nodes',G.number_of_nodes())
print('number of edges',G.number_of_edges())

## Get undirected_graph
edge_list = []
import networkx as nx
SG = nx.Graph()
for temp_str in train_data[0:2]:
  temp=temp_str.split('\t')
  for i in range(1, len(temp)):
    temp_edge = (int(temp[0]), int(temp[i]))
    edge_list.append(temp_edge)
SG.add_edges_from(edge_list)

import matplotlib.pyplot as plt
nx.draw(SG)

"""## features"""

def get_positive_features():
    features = []
    count = 0
    print("Generating positive features......")
    for temp_data in positive_train:
      if (count % 100 == 0):
        print(count)
      count += 1
      feature = []
      try:
        preds = nx.resource_allocation_index(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
        
        preds = nx.jaccard_coefficient(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
          
               
        
        feature.append(1)  # label=1
        
      except:
        print("one error at: "+str(count))
        pass
      
      features.append(feature)
    print("positive features: "+str(len(features)))
    return features

def get_negative_features():
    features = []
    count = 0
    print("Generating negative features......")
    for temp_data in negative_train:
      if (count % 100 == 0):
        print(count)
      count += 1
      feature = []
      try:
        preds = nx.resource_allocation_index(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
        
        preds = nx.jaccard_coefficient(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
          
        
        feature.append(0)  # label=1
        
      except:
        print("one error at: "+str(count))
        pass
      
      features.append(feature)
    print("positive features: "+str(len(features)))
    return features

def get_test_features():
    features = []
    count = 0
    print("Generating test data features......")
    for temp_data in test_edges:
      if (count % 100 == 0):
        print(count)
      count += 1
      feature = []
      try:
        preds = nx.resource_allocation_index(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
        
        preds = nx.jaccard_coefficient(G, [temp_data])
        for u, v, p in preds:
          feature.append(p)
          
        
        
      except:
        print("one error at: "+str(count))
        pass
      
      features.append(feature)
    print("positive features: "+str(len(features)))
    return features

"""## Combine"""

train_features = get_positive_features() + get_negative_features()

print(train_features[0:10])
print(train_features[10000:10010])

test_features = get_test_features()

print(test_features[0:10])

"""## Save features"""

import csv

with open("train_data.csv","w",newline="") as csvfile:
  writer=csv.writer(csvfile)
  writer.writerow(["RA","JC","Label"])
  #writer.writerow(["RA","JC","AA","PA","CSH","RSH","WIC","Label"])
  writer.writerows(train_features)

with open("test.csv","w",newline="") as csvfile:
  writer=csv.writer(csvfile)
  writer.writerow(["RA","JC"])
  #writer.writerow(["RA","JC","AA","PA","CSH","RSH","WIC"])
  writer.writerows(test_features)
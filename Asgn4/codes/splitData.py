__author__ = 'Abhishek'
import numpy as np

fileNames = {'0':'balance-scale.data.txt','1':'balance-scale.data.txt','2':'nursery.data.txt'}
datasetID = 2

datasetPath = '../data/'+str(datasetID)+'/'+fileNames[str(datasetID)]
fraction = 0.8

f = open(datasetPath,'r')
numLines = len(f.readlines())
f.close()
f = open(datasetPath,'r')
f1 = open(datasetPath+'.train','w')
f2 = open(datasetPath+'.test','w')

perm = np.random.permutation(range(numLines))[0:int(numLines*fraction)]

for idx,line in enumerate(f.readlines()):
    if idx in perm:
        f1.write(line)
    else:
        f2.write(line)
f1.close()
f2.close()

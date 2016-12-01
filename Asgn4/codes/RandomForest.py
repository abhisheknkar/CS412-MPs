__author__ = 'Abhishek'

from DataReader import DataReader
from DecisionTree import *
import random

class RandomForest(DecisionTree):
    def __init__(self, data, numTrees=10, subsetSize=2):
        self.data = data
        self.numTrees = numTrees
        self.subsetSize = subsetSize

        self.rIndex = self.getReverseIndex(self.data.trainX)

        self.buildForest()

    def buildForest(self):
        self.forest = []
        self.splitSamples = self.subsetSize

        for i in range(self.numTrees):
            self.forest.append(dict())
            self.trainXtemp = []
            self.trainYtemp = []
            self.varsLeft = self.rIndex.keys()

            sampleID = self.sampleWithReplacement(self.data.trainX, len(self.data.trainX))
            for sample in sampleID:
                self.trainXtemp.append(self.data.trainX[sample])
                self.trainYtemp.append(self.data.trainY[sample])
            self.rIndextemp = self.getReverseIndex(self.trainXtemp)

            root = DecisionNode()   # Root of the tree
            varsLeft = self.getRandomSplitPoints(self.rIndextemp.keys(), self.splitSamples)
            # print 'Before:', 'root:',root.state, 'Varsleft:',varsLeft
            self.buildTree(root,varsLeft, [])

        # for idx,tree in enumerate(self.forest):
        #     print 'Tree:', idx
        #     for node in tree:
        #         print node.state, node.decision

    def sampleWithReplacement(self, data, samples):
        sampleID = []
        for i in range(samples):
            sampleID.append(random.randint(0, len(data)-1))
        return sampleID

    def getRandomSplitPoints(self, varsLeft, numSamples):
        varID = self.sampleWithReplacement(varsLeft, numSamples)
        randomVars = []
        for var in varID:
            randomVars.append(varsLeft[var])
        return list(randomVars)

    def getDecisionAtNode(self, state):
        points = list(self.getPointsAtNode(state)) # Get all the data points that satisfy the constraint
        labelDist = self.getLabelDistribution(points)
        if len(labelDist) > 0:
            decision = max(labelDist, key=labelDist.get)
        else:
            decision = None
        return (points, labelDist, decision)

    def getPointsAtNode(self, node):
        satisfied = []
        if len(node.state) == 0:
            return set(xrange(len(self.trainXtemp)))
        else:
            for constraint in node.state:
                satisfied.append(self.rIndex[constraint[0]][constraint[1]])
            return set.intersection(*satisfied)

    def buildTree(self, root, varsLeft, varsDone, depth=0):
        self.forest[-1][root] = root
        (points, labelDist, decision) = self.getDecisionAtNode(root)

        # Termination check 1: Are we out of variables to split? If so, return the dominant label
        if len(varsLeft) == 0:
            if len(labelDist) == 0:
                self.forest[-1][root].isEmpty = True
                return
            self.forest[-1][root].isTerminal = True
            self.forest[-1][root].decision = decision
            return

        # Termination check 2: Do all the data points belong to the same class? If so, assign that class to the point
        nonZeros = [key for key,val in labelDist.iteritems() if val > 0]
        if len(nonZeros) == 1:
            self.forest[-1][root].isTerminal = True
            self.forest[-1][root].decision = nonZeros[0]
            return

        nextSplitVar = self.getNextSplitVariable(points, varsLeft)
        self.forest[-1][root].nextSplitVar = nextSplitVar

        featureValDist = self.getFeatureValueDistribution(points, nextSplitVar)
        varsDone.append(nextSplitVar)

        for key in featureValDist:
            newState = list(root.state)
            newState.append((nextSplitVar,key))

            if len(list(set(self.rIndextemp.keys())-set(varsDone)))> 0:
                newVarsLeft = self.getRandomSplitPoints(list(set(self.rIndextemp.keys())-set(varsDone)), self.splitSamples)
            else:
                newVarsLeft = []

            self.buildTree(root=DecisionNode(tuple(newState)),varsLeft=list(newVarsLeft), varsDone=list(varsDone), depth=depth+1)

    def getNextSplitVariable(self, points, varsLeft):
        # Gets the next variable to split on. Calls the getInformationGain() helper function
        IG = {}
        for var in varsLeft:
            IG[var] = self.getInformationGain(points, var)
        return max(IG, key=IG.get)

    def predictPoint(self, point):
        decisions = []
        for i in range(self.numTrees):
            state = self.forest[i][()]
            while(1):
                if state.isTerminal:
                    decisions.append(state.decision)
                    break
                else:
                    nextSplitVar = state.nextSplitVar
                    value = point[nextSplitVar]

                    nextState = list(state.state)
                    nextState.append((nextSplitVar,value))
                    nextState = tuple(nextState)
                    if nextState in self.forest[i] and not self.forest[i][nextState].isEmpty:
                        state = self.forest[i][nextState]
                    else:
                        (labelDist, points, decision) = self.getDecisionAtNode(state)
                        decisions.append(decision)
                        break
        return max(set(decisions), key=decisions.count)

def testGiven():
    fileNames = {'0':'balance-scale','1':'balance-scale','2':'nursery.data', '3':'led', '4':'poker'}
    for datasetID in range(0,5):
        print 'Dataset', datasetID, ',', fileNames[str(datasetID)]
        filePrefix = '../data/'+str(datasetID)+'/'+fileNames[str(datasetID)]
        # data = DataReader(filePrefix+'.train', filePrefix+'.test')
        data = DataReader(filePrefix+'.train', filePrefix+'.test')
        forest = RandomForest(data, numTrees=20, subsetSize=2)
        forest.predict(outputFile=filePrefix+'.pred', writeFlag=True)
        # break

if __name__ == '__main__':
    testGiven()
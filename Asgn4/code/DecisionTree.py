__author__ = 'Abhishek'
# import math
import numpy
# from sklearn import tree

import sys
from DataReader import DataReader

class DecisionTree():
    def __init__(self, data):
        self.missingClass = 0
        self.data = data
        self.rIndex = self.getReverseIndex(self.data.trainX)

        varsLeft = self.rIndex.keys()   # Variables yet to be split
        root = DecisionNode()   # Root of the tree

        self.treeStates = {}    # Hashmap to store the nodes in the tree encounterd so far
        self.buildTree(root, varsLeft)

    def buildTree(self, root, varsLeft):
        self.treeStates[root] = root
        (points, labelDist, decision) = self.getDecisionAtNode(root)

        # Termination check 1: Are we out of variables to split? If so, return the dominant label
        if len(varsLeft) == 0:
            if len(labelDist) == 0:
                self.treeStates[root].isEmpty = True
                return
            self.treeStates[root].isTerminal = True
            self.treeStates[root].decision = decision
            return

        # Termination check 2: Do all the data points belong to the same class? If so, assign that class to the point
        nonZeros = [key for key,val in labelDist.iteritems() if val > 0]
        if len(nonZeros) == 1:
            self.treeStates[root].isTerminal = True
            self.treeStates[root].decision = nonZeros[0]
            return

        nextSplitVar = self.getNextSplitVariable(points, varsLeft)
        self.treeStates[root].nextSplitVar = nextSplitVar

        featureValDist = self.getFeatureValueDistribution(points, nextSplitVar)

        # for key in self.rIndex[nextSplitVar]:
        for key in featureValDist:
            newState = list(root.state)
            newState.append((nextSplitVar,key))
            newVarsLeft = list(varsLeft)
            newVarsLeft.remove(nextSplitVar)
            self.buildTree(root=DecisionNode(tuple(newState)),varsLeft=newVarsLeft)

    def getDecisionAtNode(self, state):
        points = list(self.getPointsAtNode(state)) # Get all the data points that satisfy the constraint
        labelDist = self.getLabelDistribution(points)
        if len(labelDist) > 0:
            decision = max(labelDist, key=labelDist.get)
        else:
            decision = None
        return (points, labelDist, decision)

    def getReverseIndex(self, data):
        # For each value of each attribute, get set of data points that satisfy it
        rIndex = {}
        for i in range(len(data[0])):
            rIndex[i] = {}
        for idx1,point in enumerate(data):
            for idx2,att in enumerate(point):
                if att not in rIndex[idx2]:
                    rIndex[idx2][att] = set()
                rIndex[idx2][att].add(idx1)
        return rIndex

    def getPointsAtNode(self, node):
        satisfied = []
        if len(node.state) == 0:
            return set(xrange(len(self.data.trainX)))

        else:
            for constraint in node.state:
                satisfied.append(self.rIndex[constraint[0]][constraint[1]])
            return set.intersection(*satisfied)

    def getLabelDistribution(self, points):
        dist = {}
        for point in points:
            label = self.data.trainY[point]
            if label not in dist:
                dist[label] = 0
            dist[label] += 1
        return dist

    def getNextSplitVariable(self, points, varsLeft):
        # Gets the next variable to split on. Calls the getInformationGain() helper function
        IG = {}
        for var in varsLeft:
            IG[var] = self.getInformationGain(points, var)
        return max(IG, key=IG.get)

    def getFeatureValueDistribution(self, points, feature):
        dist = {}
        for pointID in points:
            if self.data.trainX[pointID][feature] not in dist:
                dist[self.data.trainX[pointID][feature]] = 0
            dist[self.data.trainX[pointID][feature]] += 1
        return dist

    def getInformationGain(self, points, var, mode='gini'):
        labelDist = self.getLabelDistribution(points)
        gain = self.getEntropy(labelDist, mode)

        for value in self.rIndex[var]:
            newPoints = set(points).intersection(self.rIndex[var][value])
            labelDist = self.getLabelDistribution(newPoints)

            if len(points) == 0:
                continue
            gain -= self.getEntropy(labelDist, mode) * len(newPoints) / len(points)
        return gain

    def getEntropy(self, labelDist, mode='regular'):
        normalized = labelDist.values()
        total = sum(labelDist.values())
        normalized = [float(x) / total for x in normalized]

        if mode == 'regular':
            entropy = 0
            for elem in normalized:
                entropy += -math.log(elem,2)*elem

        if mode == 'gini':
            entropy = 1
            for elem in normalized:
                entropy -= elem*elem

        return entropy

    def predict(self, outputFile=None, writeFlag=False):
        self.pred = []
        if writeFlag:
            f = open(outputFile, 'w')
        correct = 0
        for idx,point in enumerate(self.data.testX):
            self.pred.append(self.predictPoint(point))
            # if pred[-1] == self.data.testY[idx]:
            #     correct += 1
            if writeFlag:
                f.write(str(self.pred[-1])+'\n')
        if writeFlag:
            f.close()

        # accuracy = float(correct) / len(self.data.testY)
        # print 'Accuracy:', accuracy
        return self.pred
        # print 'Missing node:', self.missingClass

    def predictPoint(self, point):
        state = self.treeStates[()]
        while(1):
            if state.isTerminal:
                # if len(state.state) == len(point):
                #     for i in range(len(point)):
                #         print str(i+1)+':'+point[i],
                #     print '\n'
                return state.decision
            else:
                nextSplitVar = state.nextSplitVar
                value = point[nextSplitVar]

                nextState = list(state.state)
                nextState.append((nextSplitVar,value))
                nextState = tuple(nextState)
                if nextState in self.treeStates and not self.treeStates[nextState].isEmpty:
                    state = self.treeStates[nextState]
                else:
                    (labelDist, points, decision) = self.getDecisionAtNode(state)
                    self.missingClass += 1
                    return decision

class DecisionNode():
    def __init__(self, state=()):
        self.state = state
        self.nextSplitVar = None # The variable to split on next
        self.isTerminal = False
        self.decision = None
        self.isEmpty = False

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return hash(other) == hash(self.state)

def getMeasures(tree):
    # Get CM, Overall accuracy, Sensitivity, Specificity, Precision, Recall, F-1 Score, F \beta score (\beta = 0.5 and 2)

    # Get CM
    pred = tree.pred
    true = tree.data.testY
    classes = sorted(list(set(tree.data.trainY)))
    classMap = {}
    for x in classes:
        classMap[x] = len(classMap)
    CM = [[0 for i in range(len(classes))] for j in range(len(classes))]
    for i in range(len(pred)):
        CM[classMap[true[i]]][classMap[pred[i]]] += 1.0

    # Get overall accuracy
    accuracy = sum([CM[row][row] for row in range(len(CM))]) / len(pred)

    # Initialize sensitivity, specificity, precision, recall
    sensitivity = [0.0 for i in range(len(classes))]
    specificity = [0.0 for i in range(len(classes))]
    precision = [0.0 for i in range(len(classes))]
    recall = [0.0 for i in range(len(classes))]
    f1 = [0.0 for i in range(len(classes))]
    fpoint5 = [0.0 for i in range(len(classes))]
    f2 = [0.0 for i in range(len(classes))]

    # CM = [[0.0,1.0,2.0],[3.0,4.0,5.0],[6.0,7.0,8.0]]

    # Computing the metrics
    for i in range(len(CM)):
        CM_2x2 = [[0,0],[0,0]]
        CM_2x2[0][0] = CM[i][i]
        CM_2x2[0][1] = sum(CM[i][0:i]+CM[i][i+1:])
        CM_2x2[1][0] = sum([CM[x][i] for x in range(len(CM)) if x!=i])
        CM_2x2[1][1] = sum([sum(x) for x in [[CM[p][q] for q in range(len(CM)) if q!=i] for p in range(len(CM)) if p!=i]])

        TP = CM_2x2[0][0]
        FN = CM_2x2[0][1]
        FP = CM_2x2[1][0]
        TN = CM_2x2[1][1]

        if TP+FN > 0.0:
            sensitivity[i] = (TP/(TP+FN))
            recall[i] = (TP/(TP+FN))
        if FP+TN > 0.0:
            specificity[i] = (TN/(FP+TN))
        if TP+FP > 0.0:
            precision[i] = (TP/(TP+FP))
        f1[i] = (getFbeta(precision[i],recall[i],1))
        fpoint5[i] = (getFbeta(precision[i],recall[i],0.5))
        f2[i] = (getFbeta(precision[i],recall[i],2))

    # print 'Accuracy:', accuracy
    # print 'Sensitivity:', sensitivity
    # print 'Specificity:', specificity
    # print 'Precision:', precision
    # print 'Recall:', recall
    # print 'F1:', f1
    # print 'F0.5:', fpoint5
    # print 'F2:', f2
    return (CM, accuracy, sensitivity, specificity, precision, recall, f1, fpoint5, f2)

def getFbeta(p, r, beta):
    if p==0.0 and r==0.0:
        return 0.0
    return (1+beta**2)*p*r/(p*beta**2+r)

def testGivenDatasets():
    print '\n\nWith my code:\n============'
    fileNames = {'0':'balance-scale','1':'balance-scale','2':'nursery.data', '3':'led', '4':'poker'}
    for datasetID in range(1,5):
        print 'Dataset', datasetID, ',', fileNames[str(datasetID)]
        filePrefix = '../data/'+str(datasetID)+'/'+fileNames[str(datasetID)]
        data = DataReader(filePrefix+'.train', filePrefix+'.test')
        tree = DecisionTree(data)
        tree.predict(outputFile=filePrefix+'.pred', writeFlag=True)
        (CM, accuracy, sensitivity, specificity, precision, recall, f1, fpoint5, f2) = getMeasures(tree)
        # print (accuracy, sensitivity, specificity, precision, recall, f1, fpoint5, f2)
        print 'Accuracy:', accuracy

        f = open('results/DecisionTree/dataset'+str(datasetID)+'.csv', 'w')
        f.write('Accuracy,'+str("{0:.3f}".format(accuracy))+'\n\n')
        f.write('Class,Sensitivity,Specificity,Precision,Recall,F1,F0.5,F2\n')
        for i in range(len(sensitivity)):
            f.write(str(i)+','+str("{0:.3f}".format(sensitivity[i]))+','+str("{0:.3f}".format(specificity[i]))+','+str("{0:.3f}".format(precision[i]))+','+str("{0:.3f}".format(recall[i]))+','+str("{0:.3f}".format(f1[i]))+','+str("{0:.3f}".format(fpoint5[i]))+','+str("{0:.3f}".format(f2[i]))+'\n')
        f.close()
        # break

def runDecisionTree(trainPath, testPath):
    data = DataReader(trainPath, testPath)
    tree = DecisionTree(data)
    tree.predict()
    (CM, accuracy, sensitivity, specificity, precision, recall, f1, fpoint5, f2) = getMeasures(tree)
    for row in CM:
        print ' '.join([str(int(x)) for x in row])

def testSKLearn():
    print '\n\nWith SKLearn:\n============='
    fileNames = {'0':'balance-scale','1':'balance-scale','2':'nursery.data', '3':'led', '4':'poker'}
    for datasetID in range(1,5):
        print 'Dataset', datasetID, ',', fileNames[str(datasetID)]
        filePrefix = '../data/'+str(datasetID)+'/'+fileNames[str(datasetID)]
        data = DataReader(filePrefix+'.train', filePrefix+'.test')

        clf = tree.DecisionTreeClassifier(min_samples_split=len(data.trainY))
        clf.fit(data.trainX, data.trainY)
        pred = clf.predict(data.testX)

        # for i in range(len(pred)):
        #     print pred[i], data.trainY[i]

        classes = sorted(list(set(data.trainY)))
        classMap = {}
        for x in classes:
            classMap[x] = len(classMap)
        CM = [[0 for i in range(len(classes))] for j in range(len(classes))]
        for i in range(len(pred)):
            CM[classMap[data.trainY[i]]][classMap[pred[i]]] += 1.0
        accuracy = sum([CM[row][row] for row in range(len(CM))]) / len(pred)
        print 'Accuracy:', accuracy
        # break

if __name__ == '__main__':
    # testGivenDatasets()
    # testSKLearn()
    if len(sys.argv) < 2:
        print 'Usage: python DecisionTree.py training_file test_file'
    else:
        runDecisionTree(trainPath=sys.argv[1], testPath=sys.argv[2])
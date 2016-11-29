__author__ = 'Abhishek'
import math

class DataReader():
    def __init__(self, train_file='', test_file=''):
        self.train_file = train_file
        self.test_file = test_file

        self.readMatrices()

    def readMatrices(self):
        (self.trainX, self.trainY) = self.dataset2Mat(self.train_file)
        (self.testX, self.testY) = self.dataset2Mat(self.test_file)

    def dataset2Mat(self, file):
        f = open(file, 'r')
        matX = []
        matY = []
        for line in f.readlines():
            lsplit = line.strip().split(' ')
            matY.append(lsplit[0]) # Append label to the Y matrix
            xVec = []   # To hold the feature values
            for feature in lsplit[1:]:
                if ':' in feature:
                    value = feature[feature.index(':')+1:]
                else:
                    value = feature
                xVec.append(value)
            matX.append(xVec)
        return (matX, matY)

class DecisionTree():
    def __init__(self, data):
        self.missingClass = 0
        self.data = data
        self.rIndex = self.getReverseIndex()

        varsLeft = self.rIndex.keys()   # Variables yet to be split
        root = DecisionNode()   # Root of the tree

        self.treeStates = {}    # Hashmap to store the nodes in the tree encounterd so far

        self.maxLevel = 0
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

    def getReverseIndex(self):
        # For each value of each attribute, get set of data points that satisfy it
        rIndex = {}
        for i in range(len(self.data.trainX[0])):
            rIndex[i] = {}
        for idx1,point in enumerate(self.data.trainX):
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

    def getInformationGain(self, points, var):
        labelDist = self.getLabelDistribution(points)
        gain = self.getEntropy(labelDist)

        for value in self.rIndex[var]:
            newPoints = set(points).intersection(self.rIndex[var][value])
            labelDist = self.getLabelDistribution(newPoints)

            if len(points) == 0:
                continue
            gain -= self.getEntropy(labelDist) * len(newPoints) / len(points)
        return gain

    def getEntropy(self, labelDist):
        normalized = labelDist.values()
        total = sum(labelDist.values())
        normalized = [float(x) / total for x in normalized]

        entropy = 0
        for elem in normalized:
            entropy += -math.log(elem,2)*elem
        return entropy

    def predict(self, outputFile, writeFlag='False'):
        if writeFlag:
            f = open(outputFile, 'w')
        correct = 0
        for idx,point in enumerate(self.data.testX):
            pred = self.predictPoint(point)
            if pred == self.data.testY[idx]:
                correct += 1
            if writeFlag:
                f.write(str(pred)+'\n')
        if writeFlag:
            f.close()

        accuracy = float(correct) / len(self.data.testY)
        print 'Accuracy:', accuracy, ', Missing node:', self.missingClass

    def predictPoint(self, point):
        state = self.treeStates[()]
        while(1):
            if state.isTerminal:
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

def testGiven():
    fileNames = {'0':'balance-scale','1':'balance-scale','2':'nursery.data', '3':'led', '4':'poker'}
    for datasetID in range(1,5):
        print 'Dataset', datasetID, ',', fileNames[str(datasetID)]
        filePrefix = '../data/'+str(datasetID)+'/'+fileNames[str(datasetID)]
        data = DataReader(filePrefix+'.train', filePrefix+'.test')
        tree = DecisionTree(data)
        tree.predict(outputFile=filePrefix+'.pred', writeFlag=True)

if __name__ == '__main__':
    testGiven()
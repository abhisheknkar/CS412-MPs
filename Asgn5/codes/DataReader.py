__author__ = 'Abhishek'

class DataReader():
    def __init__(self, train_file='', test_file='', floatMode=False):
        self.train_file = train_file
        self.test_file = test_file
        self.floatMode = floatMode

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
            label = lsplit[0]
            if self.floatMode:
                label = float(label)
            matY.append(label) # Append label to the Y matrix
            xVec = []   # To hold the feature values
            for feature in lsplit[1:]:
                if ':' in feature:
                    value = feature[feature.index(':')+1:]
                else:
                    value = feature
                if self.floatMode:
                    value = float(value)
                xVec.append(value)
            matX.append(xVec)
        return (matX, matY)


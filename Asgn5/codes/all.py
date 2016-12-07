__author__ = 'Abhishek'
from DataReader import DataReader
from DecisionTree import *

def Q1(data):
    # 1a(1): Information for classification
    tree = DecisionTree(data)
    points = tree.getPointsAtNode(DecisionNode())
    labelDist = tree.getLabelDistribution(points)
    entropy = tree.getEntropy(labelDist)

    print '1a(1): Average entropy=', entropy

    # 1a(2): Information gain for price
    attID = 1
    gain = tree.getInformationGain(points, attID)
    print '1a(2): Information Gain for price =', gain

    # 1b: Gini index
    points = tree.getPointsAtNode(DecisionNode())
    featureValueDist = tree.getFeatureValueDistribution(points=points, feature=2)
    giniDelivery = tree.getEntropy(featureValueDist, mode='gini')
    print '1b(1): Gini Index of attribute Delivery:', giniDelivery

    infoGain = tree.getInformationGain(points, var=2, mode='gini')
    print '1b(2): Reduction in impurity on splitting at attribute Delivery:', infoGain

    # 1c: Probabilities
    points = tree.getPointsAtNode(DecisionNode())
    labelDist = tree.getLabelDistribution(points)
    p = float(labelDist['P'])/(labelDist['P']+labelDist['NP'])
    print '1c(1,2): Priors: Pr(P)=', p, ', Pr(NP)=', 1-p

    # Likelihoods:
    target = ['Korean', '1', 'Yes']
    pointsP = Q1getAllOccurrences(data.trainY, 'P')
    pointsNP = Q1getAllOccurrences(data.trainY, 'NP')

    pointsAtt0 = tree.getPointsAtNode(DecisionNode(((0, 'Korean'),)))
    pointsAtt1 = tree.getPointsAtNode(DecisionNode(((1, '1'),)))
    pointsAtt2 = tree.getPointsAtNode(DecisionNode(((2, 'Yes'),)))

    likelihoodP = Q1getLikelihood([pointsAtt0, pointsAtt1, pointsAtt2], set(pointsP))
    likelihoodNP = Q1getLikelihood([pointsAtt0, pointsAtt1, pointsAtt2], set(pointsNP))

    print '1c(3): Likelihood given P:', likelihoodP
    print '1c(4): Likelihood given NP:', likelihoodNP

    posteriorP = likelihoodP * len(pointsP)
    posteriorNP = likelihoodNP * len(pointsNP)

    print '1d: posterior(P)=',posteriorP, ', posterior(NP)=', posteriorNP,
    if posteriorP > posteriorNP:
        print ' ==> Classified as popular'
    else:
        print ' ==> Classified as not popular'

def Q1getLikelihood(occurrenceSets, conditionalOccurrence):
    product = 1
    for idx,elem in enumerate(occurrenceSets):
        product *= float(len(elem.intersection(conditionalOccurrence)))/len(conditionalOccurrence)
    return product

def Q1getAllOccurrences(listItems, targetItem):
    occurrences = []
    for idx,item in enumerate(listItems):
        if item == targetItem:
            occurrences.append(idx)
    return occurrences

def Q2(data, k=3):
    predY = []
    accuracy = 0
    for idx, point in enumerate(data.testX):
        distVec = Q2getAllDistance(data.trainX, point)
        argSort = sorted(range(len(distVec)), key=lambda k: distVec[k])
        topK = argSort[0:k]
        closestNeighbourLabels = [data.trainY[x] for x in topK]
        decision = max(set(closestNeighbourLabels), key=closestNeighbourLabels.count)
        predY.append(decision)
        topKpp = [x+1 for x in topK]
        # closestNeighbours = [data.trainX[x] for x in topK]
        print 'For point ', idx+11, ':', point, 'closest points:', topKpp, 'decision=', decision
        if predY[idx] == data.testY[idx]:
            accuracy+=1
    print 'Accuracy=', float(accuracy)/len(data.testX)

def Q2getAllDistance(trainX, point1):
    distVec = []
    for point2 in trainX:
        distVec.append(Q2getDistance(point1, point2))
    return distVec

def Q2getDistance(point1, point2):
    dist = 0
    for idx in range(len(point1)):
        dist += (point1[idx]-point2[idx])**2
    return dist

def Q3(data, k=3, centroids=[[0,0],[1,1],[2,2]]):
    result = Q3performKNN(data.trainX, centroids)

def Q3performKNN(points, centroids):
    result = [0 for x in points]
    changeFlag = True
    iterations = 0
    while(changeFlag):
        iterations += 1
        changeFlag = False
        for idx,point in enumerate(points):
            distanceVec = Q2getAllDistance(centroids, point)
            newResult = sorted(range(len(distanceVec)), key=lambda k: distanceVec[k])[0]
            if newResult != result[idx]:
                changeFlag = True
            result[idx] = newResult
            # print 'Point:', point, 'DistanceVec:', distanceVec, 'Result:', result[idx]
        for i in range(len(centroids)):
            pointsCluster = Q1getAllOccurrences(result, i)
            if len(pointsCluster)>0:
                centroids[i] = [0.0,0.0]
                for pointID in pointsCluster:
                    centroids[i][0] += points[pointID][0]
                    centroids[i][1] += points[pointID][1]
                centroids[i][0] /=  len(pointsCluster)
                centroids[i][1] /=  len(pointsCluster)
            if iterations==1:
                print 'Initially, points assigned to cluster:', i+1, ':', [x+1 for x in pointsCluster]
        if iterations==1:
            print 'After first step of KMC, new centroids are:', centroids
        # print 'Centroids:', centroids
    print 'KMC terminates in', iterations, 'steps.'
    print 'After KMC:'
    for i in range(len(centroids)):
        pointsCluster = Q1getAllOccurrences(result, i)
        print 'Points assigned to cluster', i+1, 'are:', [x+1 for x in pointsCluster]
    return result

if __name__ == '__main__':
    attempt = [1,2,3,4]

    if 1 in attempt:
        data = DataReader('../data/restaurants.data', '../data/restaurants.data')
        print 'Q1:\n==='
        Q1(data)

    if 2 in attempt:
        data = DataReader('../data/pointsKNN.train', '../data/pointsKNN.test', floatMode=True)
        print '\nQ2:\n==='
        Q2(data, k=3)

    if 3 in attempt:
        data = DataReader('../data/pointsKMC.train', '../data/pointsKMC.train', floatMode=True)
        print '\nQ3:\n==='
        Q3(data, k=3, centroids=[[2.0,5.0], [6.0,0.5], [6.0, 5.0]])

    if 4 in attempt:
        data = DataReader('../data/pointsKMC.train', '../data/pointsKMC.train', floatMode=True)
        print '\nQ4:\n==='
        Q3(data, k=3, centroids=[[1.0,4.0], [0.2,6.0], [4.3, 2.0]])

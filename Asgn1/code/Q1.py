__author__ = 'Abhishek'
import pandas as pd
import numpy as np
from scipy import stats


def getMinMax(dataset, column):
    print 'Minimum score in column ', column, ' is ', min(dataset.ix[:,column])
    print 'Maximum score in column ', column, ' is ', max(dataset.ix[:,column])

def getQuartiles(dataset, column, quartilesToGet):
    for quartile in quartilesToGet:
        print 'Quartile ', quartile, ' is ', np.percentile(dataset.ix[:,column], quartile)

    a = np.sort(dataset.ix[:,column])
    print 'Quartiles from First Principles: ', 0.5*(a[250]+a[251]), 0.5*(a[501]+a[501]), 0.5*(a[750]+a[751])

def getSampleVariance(X):
    squaredX = np.multiply(np.array(X, dtype='float'), np.array(X, dtype='float'))
    n = len(X)
    sampleVariance = (np.sum(squaredX) - np.sum(X)**2/n) / (n - 1)
    return sampleVariance

def getOrder1Order2Stats(dataset, column, sampleMode=True, printMode=True):
    origCol = dataset.ix[:,column]
    squaredCol = np.multiply(origCol, origCol)
    n = len(origCol)
    sampleVarianceP1 = getSampleVariance(origCol)

    if printMode == True:
        print 'Mean score in column ', column, ' is ', np.mean(origCol)
        print 'Median score in column ', column, ' is ', np.median(origCol)
        print 'Mode score in column ', column, ' is ', stats.mode(origCol)[0][0]
        print 'Population Variance (!) of score in column ', column, ' is ', np.var(origCol)
        print 'Variance from first principles: ', sampleVarianceP1

    return (np.mean(origCol), np.median(origCol), stats.mode(origCol)[0][0], sampleVarianceP1)

def checkMeanMedianModeConsistency(dataset, column):
    dataMean = np.mean(dataset.ix[:,column])
    dataMedian = np.median(dataset.ix[:,column])
    dataMode = stats.mode(dataset.ix[:,column])[0][0]

    print 'Mean - Mode = ', dataMean-dataMode, '; 3*(Mean - Median) = ', 3*(dataMean - dataMedian)

if __name__ == '__main__':
    dataset = pd.read_table('../data/data.online.scores', index_col=0)
    # getMinMax(dataset, 0)
    # getQuartiles(dataset, 0, [25, 50, 75])
    getOrder1Order2Stats(dataset, 0)
    # checkMeanMedianModeConsistency(dataset, 0)
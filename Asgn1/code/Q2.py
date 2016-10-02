__author__ = 'Abhishek'

from Q1 import *

def getPrePostNormalizationStats(dataset, column):
    (dataMean, dataMedian, dataMode, dataVariance) = getOrder1Order2Stats(dataset, column, printMode=False)
    origData = dataset.ix[:,column]
    normalizedData = (origData - dataMean) / np.sqrt(dataVariance)
    normalizedVariance = getSampleVariance(normalizedData)

    # Using the population formulae: (wrong)
    # normalizedData = (origData - dataMean) / np.std(origData)
    # normalizedVariance = np.std(normalizedData)

    print 'Variance before normalization: ', dataVariance, '; variance post normalization: ', normalizedVariance
    print 'Normalized score corresponding to 90 is: ', (90-dataMean)/np.sqrt(dataVariance)


if __name__ == '__main__':
    dataset = pd.read_table('../data/data.online.scores', index_col=0)
    getPrePostNormalizationStats(dataset, 1)

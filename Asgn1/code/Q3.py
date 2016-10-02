__author__ = 'Abhishek'
from Q1 import *

def getPearson(dataset, columns):
    print 'Pearson correlation coefficient and p-value: ', stats.pearsonr(dataset.ix[:,columns[0]], dataset.ix[:,columns[1]])

def getCov(dataset, columns):
    a = dataset.ix[:,columns[0]]
    b = dataset.ix[:,columns[1]]
    covMat = np.cov(a, b)
    print 'Covariance matrix: ', covMat

if __name__ == '__main__':
    dataset = pd.read_table('../data/data.online.scores', index_col=0)
    getPearson(dataset, [0,1])
    getCov(dataset, [0,1])

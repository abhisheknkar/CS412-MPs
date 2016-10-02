__author__ = 'Abhishek'
from Q1 import *
from scipy.spatial import distance

def Q4a():
    print 'Jaccard coeff: ', 107./(19+31+107)

def getDistances(dataset):
    a = dataset.ix[:,0]
    b = dataset.ix[:,1]
    mink1 = distance.minkowski(a,b,1)
    mink2 = distance.minkowski(a,b,2)
    minkInf = max(abs(a-b))
    mink1P1 = sum(abs(a-b))
    print 'Minkowski distances for p=1, 2, infinity are: ', mink1, mink2, minkInf

    # Cosine Sim
    cosineSim = 1 - distance.cosine(a,b)
    print 'Cosine similarity is: ', cosineSim

    # KLD
    aNorm = np.array(a / sum(a), dtype='float')
    bNorm = np.array(b / sum(b), dtype='float')
    KLD_P1 = sum(aNorm * np.log2(aNorm / bNorm))
    KLD = stats.entropy(aNorm, bNorm, base=2)
    print 'KL Divergence is: ', KLD_P1

if __name__ == '__main__':
    dataset = pd.read_csv('../data/data.supermarkets.inventories', sep='\t').transpose().ix[1:,:]
    # Q4a()
    getDistances(dataset)

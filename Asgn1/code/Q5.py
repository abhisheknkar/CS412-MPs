__author__ = 'Abhishek'
from Q1 import *

def getChiSquared2x2(o):
    # o = np.array([1346, 430, 133, 32874], dtype='float')
    # o = np.array([250, 200, 50, 1000], dtype='float')
    sr0 = o[0]+o[1]
    sr1 = o[2]+o[3]
    sc0 = o[0]+o[2]
    sc1 = o[1]+o[3]
    s = sr0 + sr1
    e = np.array([sc0/s*sr0, sc1/s*sr0, sc0/s*sr1, sc1/s*sr1])
    # print sr0, sr1, sc0, sc1
    # print e
    chisquaredAns = stats.chisquare(o, e)
    print 'Chi-Squared Coefficient (First principles) is: ', sum((o-e)**2/e)
    print 'Chi-Squared Coefficient is: ', chisquaredAns

if __name__ == '__main__':
    getChiSquared2x2(np.array([1346, 430, 133, 32974], dtype='float'))
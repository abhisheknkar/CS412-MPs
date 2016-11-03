__author__ = 'Abhishek'
import time
from Rerank import getPurity
import math, operator
from PreprocessLDA import LDAInput

def getKERTRank(omega = 0.5, gamma = 0.9, numFiles=5, folderOut = '../data/EC/'):
    (purity,ftpdict,Dtfiles) = getPurity()
    phraseness = getPhraseness()
    completeness = getCompleteness()

    combined = {}
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    for i in range(numFiles):
        f1 = open(folderOut + 'pattern-'+str(i)+'.txt','w')
        f2 = open(folderOut + 'pattern-'+str(i)+'.txt.phrase','w')

        combined[i] = {}
        for pattern in ftpdict[i]:
            if completeness[i][pattern] <= gamma:
                combined[i][pattern] = 0
            else:
                combined[i][pattern] = float(ftpdict[i][pattern])/len(Dtfiles[i])*((1-omega)*purity[i][pattern] + omega*phraseness[i][pattern])
            # print 'i',i, 'PATTERN:', pattern, 'FTP:',ftpdict[i][pattern], 'PURITY:',purity[i][pattern], 'PHRASENESS:',phraseness[i][pattern],'COMBINED', combined[i][pattern]

        sortedPatterns = sorted(combined[i].items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            words = []
            if type(pattern[0]) is str:
                patternString1 = pattern[0]
                patternString2 = reverseVocab[int(pattern[0])]
            else:
                patternString1 = ' '.join(pattern[0])
                for idx in tuple(pattern[0]):
                    words.append(reverseVocab[int(idx)])
                patternString2 = ' '.join(words)

            # if completeness[i][pattern[0]] >= gamma:
            #     print i,patternString2, completeness[i][pattern[0]]

            f1.write(str(pattern[1])+ ' '+ patternString1+'\n')
            f2.write(str(pattern[1])+ ' '+ patternString2+'\n')
        f1.close()
        f2.close()

def getCompleteness(numFiles=5):
    (purity,ftpdict,Dtfiles) = getPurity()
    completeness = {}
    for i in range(numFiles):
        completeness[i] = {}
        for pattern in ftpdict[i]:
            # Find all phrases of which our phrase is a subset. Find the max out of those
            ftpCurr = pattern
            ftpMaxSuperCount = 0
            ftpMaxSuperPattern = None

            if type(ftpCurr) == str:
                ftpSet = set()
                ftpSet.add(ftpCurr)
            else:
                ftpSet = set(ftpCurr)

            for superpattern in purity[i]:
                if type(superpattern) == str:
                    continue
                elif pattern == superpattern:
                    continue
                else:
                    if ftpSet <= set(superpattern):
                        if ftpdict[i][superpattern] > ftpMaxSuperCount:
                            ftpMaxSuperCount = ftpdict[i][superpattern]
                            ftpMaxSuperPattern = superpattern
            completeness[i][pattern] = 1 - float(ftpMaxSuperCount) / ftpdict[i][pattern]
            # print i, pattern, ftpdict[i][pattern], ftpMaxSuperPattern, ftpMaxSuperCount, completeness[i][pattern]
    return completeness

def getPhraseness(numFiles=5):
    (purity,ftpdict,Dtfiles) = getPurity()
    phraseness = {}
    for i in range(numFiles):
        phraseness[i] = {}
        for pattern in purity[i]:
            if type(pattern) == str:   # If length of pattern is 1
                phraseness[i][pattern] = 0
            else:
                total = 0
                for constituent in pattern:
                    total += math.log(float(ftpdict[i][constituent])/len(Dtfiles[i]),2)
                phraseness[i][pattern] = math.log(float(ftpdict[i][pattern])/len(Dtfiles[i]),2) - total
            # print phraseness[i][pattern]
        # print len(Dtfiles[i])
    return phraseness

if __name__=='__main__':
    t0 = time.time()

    getKERTRank()

    print 'Time elapsed: ', time.time()-t0
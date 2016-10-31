__author__ = 'Abhishek'
import time
import math
from Apriori import Apriori
import operator
import numpy as np
from PreprocessLDA import LDAInput

def getPurity():
    # Get the dictionary required to get f(t,p)
    # Read the frequent pattern files, for each file make a dictionary with the key being the pattern and the value being the support
    ftpdict = {}
    Dt = []
    folderPatterns = '../data/patterns/'
    folderDocuments = '../data/transactionsByTopic/'
    numFiles = 5
    for i in range(numFiles):
        f = open(folderPatterns+'pattern-'+str(i)+'.txt','r')
        ftpdict[i] = {}
        for idx,line in enumerate(f.readlines()):
            lsplit = line.strip().split()
            value = int(lsplit[0])
            if len(lsplit) == 2:
                key = lsplit[1]
            else:
                key = tuple(lsplit[1:])
            ftpdict[i][key] = value
        f.close()

    for i in range(numFiles):
        f = open(folderDocuments+'topic-'+str(i)+'.txt','r')
        Dt.append(len(f.readlines()))
        f.close()

    # Get the value for D(t,t')
    f = open('../data/paper.txt','r')
    Dttprime = 0
    for idx,line in enumerate(f.readlines()):
        lsplit = line.strip().split()
        if len(lsplit)>1:
            Dttprime += 1
    f.close()

    purity = {}
    for i in range(numFiles):
        purity[i] = {}
        for pattern in ftpdict[i]:
            ftprimep = 0
            for j in (range(0,i)+range(i+1,numFiles)):
                if pattern in ftpdict[j]:
                    ftprimep += ftpdict[j][pattern]
            numerator = float(ftpdict[i][pattern]) / Dt[i]
            denominator = float(ftpdict[i][pattern]+ftprimep)/Dttprime
            purity[i][pattern] = math.log(numerator,2) - math.log(denominator,2)

            # print 'Doc:',i, 'Pattern:',pattern, 'ftp:', ftpdict[i][pattern], 'Dt:', Dt[i], 'ftp+ftprimep:', ftpdict[i][pattern]+ftprimep, 'Dttprime:', Dttprime, 'Purity:',purity[i][pattern]
    return (purity,ftpdict)

def rankPurity():
    print 'Ranking by purity'
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    (purity,ftpdict) = getPurity()

    outputFolder = '../data/purity/'
    outputFolderWords = '../data/purityWords/'
    # Get two dictionaries each with percentile scores for purity and support
    purityPercentile = {}
    ftpdictPercentile = {}

    aggregateScore = {}

    numFiles = 5
    for i in range(numFiles):
        f1 = open(outputFolder+'purity-'+str(i)+'.txt','w')
        f2 = open(outputFolderWords+'purity-'+str(i)+'.txt','w')
        purityPercentile[i] = {}
        ftpdictPercentile[i] = {}
        aggregateScore[i] = {}
        sortedPurity = sorted(purity[i].items(), key=operator.itemgetter(1), reverse=True)
        N = len(sortedPurity)
        for idx,element in enumerate(sortedPurity):
            purityPercentile[i][element[0]] = float((N-idx))/N*100

        sortedftpdict = sorted(ftpdict[i].items(), key=operator.itemgetter(1), reverse=True)
        for idx,element in enumerate(sortedftpdict):
            ftpdictPercentile[i][element[0]] = float((N-idx))/N*100

        for element in purityPercentile[i]:
            aggregateScore[i][element] = purityPercentile[i][element]+ftpdictPercentile[i][element]

        sortedAggregateScore = sorted(aggregateScore[i].items(), key=operator.itemgetter(1), reverse=True)
        for element in sortedAggregateScore:
            # Just the scores
            purityVal = purity[i][element[0]]
            if type(element[0]) is str:
                patternString = element[0]
            else:
                patternString = ' '.join(element[0])
            f1.write(str(purityVal)+' '+ patternString+'\n')

            words = []
            if type(element[0]) == str:
                words.append(reverseVocab[int(element[0])])
            else:
                for idx in tuple(element[0]):
                    words.append(reverseVocab[int(idx)])
            patternString = ' '.join(words)
            f2.write(str(purityVal)+ ' '+ patternString+'\n')

        f1.close()
        f2.close()

if __name__ == '__main__':
    t0 = time.time()

    rankPurity()

    print 'Time elapsed: ', time.time()-t0
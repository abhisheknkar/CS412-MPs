__author__ = 'Abhishek'
import time
import math
from Apriori import Apriori
import operator
import numpy as np
from PreprocessLDA import LDAInput

def getClosedPatterns(folderIn, folderOut, minSupPercentage=5):
    print 'Getting Closed Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'closed-'+str(i)+'.txt','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        closedPatterns = apriori.getClosedPatterns()
        print 'Closed Patterns found in file', i, ': ',len(closedPatterns)

        # Sort the frequent patterns
        sortedPatterns = sorted(closedPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            if type(pattern[0]) is str:
                patternString = pattern[0]
            else:
                patternString = ' '.join(pattern[0])
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()

def getMaxPatterns(folderIn, folderOut):
    print 'Getting Max Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'max-'+str(i)+'.txt','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        maxPatterns = apriori.getMaxPatterns()
        print 'Max Patterns found in file', i, ': ',len(maxPatterns)
        # Sort the frequent patterns
        sortedPatterns = sorted(maxPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            if type(pattern[0]) is str:
                patternString = pattern[0]
            else:
                patternString = ' '.join(pattern[0])
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()

def getClosedPatternsWords(folderIn, folderOut, minSupPercentage=5):
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    print 'Getting Closed Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'closed-'+str(i)+'.txt.phrase','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        closedPatterns = apriori.getClosedPatterns()
        print 'Closed Patterns found: ', len(closedPatterns)

        # Sort the frequent patterns
        sortedPatterns = sorted(closedPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            words = []
            if type(pattern[0]) == str:
                words.append(reverseVocab[int(pattern[0])])
            else:
                for idx in apriori.itemSet2Tuple(pattern[0]):
                    words.append(reverseVocab[int(idx)])
            patternString = ' '.join(words)
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()

def getMaxPatternsWords(folderIn, folderOut, minSupPercentage=5):
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    print 'Getting Max Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'max-'+str(i)+'.txt.phrase','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        maxPatterns = apriori.getMaxPatterns()
        print 'Max Patterns found: ', len(maxPatterns)

        # Sort the frequent patterns
        sortedPatterns = sorted(maxPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            words = []
            if type(pattern[0]) == str:
                words.append(reverseVocab[int(pattern[0])])
            else:
                for idx in apriori.itemSet2Tuple(pattern[0]):
                    words.append(reverseVocab[int(idx)])
            patternString = ' '.join(words)
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()

if __name__ == '__main__':
    t0 = time.time()
    getClosedPatterns('../data/transactionsByTopic/','../data/closed/')
    getMaxPatterns('../data/transactionsByTopic/','../data/max/')

    getClosedPatternsWords('../data/transactionsByTopic/','../data/closed/')
    getMaxPatternsWords('../data/transactionsByTopic/','../data/max/')

    print 'Time elapsed: ', time.time()-t0
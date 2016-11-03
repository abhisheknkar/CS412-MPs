__author__ = 'Abhishek'
import time
import math
from Apriori import Apriori
import operator
import numpy as np
from PreprocessLDA import LDAInput

def getFrequentPatterns(folderIn, folderOut, relativeMinSup=0.01):
    print 'Getting Frequent Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'pattern-'+str(i)+'.txt','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=relativeMinSup)
        apriori.execute()
        # Sort the frequent patterns
        if len(apriori.Lcounts)==0:
            continue
        allPatterns = apriori.Lcounts[1].copy()
        for count in range(len(apriori.Lcounts)-1):
            allPatterns.update(apriori.Lcounts[count+2])
        sortedPatterns = sorted(allPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            if type(pattern[0]) is str:
                patternString = pattern[0]
            else:
                patternString = ' '.join(pattern[0])
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()
        print 'Frequent Patterns Found:', len(allPatterns)

def getFrequentPatternsWords(folderIn, folderOut, minSupPercentage=5):
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    print 'Getting Frequent Pattern Terms'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'pattern-'+str(i)+'.txt.phrase','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        allPatterns = {}
        for count in range(len(apriori.Lcounts)):
            allPatterns.update(apriori.Lcounts[count+1])

        # maxPatterns = apriori.getMaxPatterns()
        # print 'Max Patterns found: ', len(maxPatterns)

        # Sort the frequent patterns
        sortedPatterns = sorted(allPatterns.items(), key=operator.itemgetter(1),reverse=True)
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
    getFrequentPatterns('../data/','../data/patterns/')
    getFrequentPatternsWords('../data/','../data/patterns/')

    print 'Time elapsed: ', time.time()-t0
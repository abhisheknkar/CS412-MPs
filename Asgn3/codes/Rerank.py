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

    # for i in range(numFiles):
    #     f = open(folderDocuments+'topic-'+str(i)+'.txt','r')
    #     Dt.append(len(f.readlines()))
    #     f.close()

    # f = open('../data/paper.txt','r')
    # Dttprime = {}
    # for idx,line in enumerate(f.readlines()):
    #     lsplit = line.strip().split()
        # if len(lsplit)>1:
        #     Dttprime += 1

    # Get the value for D(t,t') for all t,t' pairs
    Dtfiles = getDtfiles()

    purity = {}
    for i in range(numFiles):
        purity[i] = {}
        for pattern in ftpdict[i]:
            ftprimep = 0    # The max number of occurrencs in another class
            maxtprime = -1  # The other class with most occurrences
            for j in (range(0,i)+range(i+1,numFiles)):
                if pattern in ftpdict[j]:
                    # ftprimep += ftpdict[j][pattern]
                    if ftpdict[j][pattern] > ftprimep:
                        ftprimep = ftpdict[j][pattern]
                        maxtprime = j

            if maxtprime == -1:
                Dttprime = len(Dtfiles[i])
            else:
                Dttprime = len(Dtfiles[i].union(Dtfiles[maxtprime]))

            numerator = float(ftpdict[i][pattern]) / len(Dtfiles[i])
            denominator = float(ftpdict[i][pattern]+ftprimep)/Dttprime
            purity[i][pattern] = math.log(numerator,2) - math.log(denominator,2)
            # print i, pattern, purity[i][pattern], 'FTPRIMEP:',ftprimep
            # if pattern == '4323':
            #     print 'File:',i, 'Pattern:',pattern, 'ftp[t]:',ftpdict[i][pattern], 'ftp[t\']:', ftpdict[maxtprime][pattern], 'Dt:',len(Dtfiles[i]), 'Dtt\':', 'Dt\':',len(Dtfiles[maxtprime]), 'Dttprime:',Dttprime, 'PURITY:',purity[i][pattern]

            # print 'Doc:',i, 'Pattern:',pattern, 'ftp:', ftpdict[i][pattern], 'Dt:', Dt[i], 'ftp+ftprimep:', ftpdict[i][pattern]+ftprimep, 'Dttprime:', Dttprime, 'Purity:',purity[i][pattern]
    return (purity,ftpdict,Dtfiles)

def getDtfiles(inputFile='../data/result/word-assignments.dat', numFiles = 5):
        f0 = open(inputFile,'r')
        Dtfiles = {}
        for i in range(numFiles):
            Dtfiles[i] = set()

        for idx,line in enumerate(f0.readlines()):
            lsplit = line.strip().split(' ')
            toWrite = [[] for i in range(numFiles)]
            for assignment in lsplit[1:]:
                assignmentSplit = assignment.split(':')
                wordID = assignmentSplit[0]
                topicID = int(assignmentSplit[1])
                toWrite[topicID].append(wordID)
            for i in range(numFiles):
                if len(toWrite[i]) > 0:
                    Dtfiles[i].add(idx)

        f0.close()
        return Dtfiles

def rankPurity():
    print 'Ranking by purity'
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    (purity,ftpdict, Dtfiles) = getPurity()

    outputFolder = '../data/purity/'
    outputFolderWords = '../data/purity/'
    # Get two dictionaries each with percentile scores for purity and support
    purityPercentile = {}
    ftpdictPercentile = {}

    aggregateScore = {}

    numFiles = 5
    for i in range(numFiles):
        f1 = open(outputFolder+'purity-'+str(i)+'.txt','w')
        f2 = open(outputFolderWords+'purity-'+str(i)+'.txt.phrase','w')
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
    # getPurity()

    print 'Time elapsed: ', time.time()-t0
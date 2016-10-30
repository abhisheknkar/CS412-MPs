__author__ = 'Abhishek'
import time
# from collections import OrderedDict
from Apriori import Apriori
import operator

class LDAInput():
    def __init__(self, inputFile='../data/paper.txt', vocabFile='../data/vocab.txt', tokenizeOut='../data/title.txt', tokenizeFlag=False, createVocabFlag=False):
        # The file contains all 'transactions'
        if createVocabFlag:
            self.createVocab(inputFile, vocabFile)
        if tokenizeFlag:
            self.vocab = self.getVocab(vocabFile)
            self.tokenize(inputFile, tokenizeOut)

    def createVocab(self, inputFile, vocabFile):
        f1 = open(inputFile, 'r')
        f2 = open(vocabFile,'w')
        vocab = set()
        for idx,line in enumerate(f1.readlines()):
            lsplit = line.strip().split('\t')
            if len(lsplit) == 2:    # Ignore those lines with no title
                words = lsplit[1].split()
                for word in words:
                    vocab.add(word)

        for word in vocab:
            f2.write(word+'\n')
        f1.close()
        f2.close()

    def getVocab(self, vocabFile='../data/vocab.txt'):
        f1 = open(vocabFile, 'r')
        vocab ={}
        for idx,line in enumerate(f1.readlines()):
            vocab[line.strip()] = idx
        f1.close()
        return vocab

    def getReverseVocab(self, vocabFile='../data/vocab.txt'):
        f1 = open(vocabFile, 'r')
        reverseVocab ={}
        for idx,line in enumerate(f1.readlines()):
            reverseVocab[idx] = line.strip()
        f1.close()
        return reverseVocab


    def tokenize(self, inputFile, tokenizeOut):
        f1 = open(inputFile,'r')
        f2 = open(tokenizeOut,'w')
        for line in f1.readlines():
            lsplit = line.strip().split('\t')
            if len(lsplit) == 2:
                words = lsplit[1].split()
                tokens = {}
                for word in words:
                    if word not in tokens:
                        tokens[word] = 0
                    tokens[word] += 1
                toWrite = ''
                for uniqueWord in tokens:
                    toWrite += ' '+ str(self.vocab[uniqueWord])+':'+str(tokens[uniqueWord])
                f2.write(str(len(tokens))+toWrite+'\n')
            else:
                f2.write('0\n')

        f1.close()
        f2.close()

class PartitionByTopics():
    def __init__(self, inputFile='../data/result/word-assignments.dat', transactionFolder='../data/transactionsByTopic/',topics=5, createTransactions=False):
        self.topics = topics
        if createTransactions:
            self.createTransactionFiles(inputFile, transactionFolder)

    def createTransactionFiles(self, inputFile, transactionFolder):
        f0 = open(inputFile,'r')
        f = []
        for i in range(self.topics):
            f.append(open(transactionFolder+'topic-'+str(i)+'.txt','w'))

        for line in f0.readlines():
            lsplit = line.strip().split(' ')
            toWrite = [[] for i in range(self.topics)]
            for assignment in lsplit[1:]:
                assignmentSplit = assignment.split(':')
                wordID = assignmentSplit[0]
                topicID = int(assignmentSplit[1])
                toWrite[topicID].append(wordID)
            for i in range(self.topics):
                if len(toWrite[i]) > 0:
                    out = ' '.join(toWrite[i])
                    f[i].write(out+'\n')

        for i in range(self.topics):
            f[i].close()

def getFrequentPatterns(folderIn, folderOut, minSupPercentage=5):
    print 'Getting Frequent Patterns'
    numFiles = 1
    for i in range(numFiles):
        f1 = open(folderOut + 'pattern-'+str(i)+'.txt','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
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

def getClosedPatterns(folderIn, folderOut, minSupPercentage=5):
    print 'Getting Closed Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'closed-'+str(i)+'.txt','w')
        apriori = Apriori(folderIn+'topic-'+str(i)+'.txt', setRelative=True, relativeMinSup=0.01)
        apriori.execute()

        closedPatterns = apriori.getClosedPatterns()
        print 'Closed Patterns found: ', len(closedPatterns)

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
        print 'Max Patterns found: ', len(maxPatterns)
        # Sort the frequent patterns
        sortedPatterns = sorted(maxPatterns.items(), key=operator.itemgetter(1),reverse=True)
        for pattern in sortedPatterns:
            if type(pattern[0]) is str:
                patternString = pattern[0]
            else:
                patternString = ' '.join(pattern[0])
            f1.write(str(pattern[1])+ ' '+ patternString+'\n')
        f1.close()

def testApriori():
    apriori = Apriori('../data/test/testDB.txt', minsup=2)
    apriori.execute()
    closedP = apriori.getClosedPatterns()
    maxP = apriori.getMaxPatterns()

    print 'Counts: ', apriori.Lcounts
    print 'Closed Patterns', closedP
    print 'Max Patterns', maxP

def getClosedPatternsWords(folderIn, folderOut, minSupPercentage=5):
    ldainput = LDAInput()
    reverseVocab = ldainput.getReverseVocab()

    print 'Getting Closed Patterns'
    numFiles = 5
    for i in range(numFiles):
        f1 = open(folderOut + 'closed-'+str(i)+'.txt','w')
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
        f1 = open(folderOut + 'max-'+str(i)+'.txt','w')
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

    # f = LDAInput(createVocabFlag=True, tokenizeFlag=True)
    # f = PartitionByTopics(createTransactions=True)

    # getFrequentPatterns('../data/transactionsByTopic/','../data/patterns/')
    # getClosedPatterns('../data/transactionsByTopic/','../data/closed/')
    # getMaxPatterns('../data/transactionsByTopic/','../data/max/')

    # getClosedPatternsWords('../data/transactionsByTopic/','../data/closedWords/')
    getMaxPatternsWords('../data/transactionsByTopic/','../data/maxWords/')
    # testApriori()

    print 'Time elapsed: ', time.time()-t0
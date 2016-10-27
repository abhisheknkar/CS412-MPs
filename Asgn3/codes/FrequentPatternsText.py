__author__ = 'Abhishek'
import time
# from collections import OrderedDict

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

    def getVocab(self, vocabFile):
        f1 = open(vocabFile, 'r')
        vocab ={}
        for idx,line in enumerate(f1.readlines()):
            vocab[line.strip()] = idx
        f1.close()
        return vocab

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

class FPTopics():
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

if __name__ == '__main__':
    t0 = time.time()
    # f = LDAInput(createVocabFlag=True, tokenizeFlag=True)
    f = FPTopics(createTransactions=True)

    print 'Time elapsed: ', time.time()-t0
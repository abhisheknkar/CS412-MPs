__author__ = 'Abhishek'
import time
import math
from Apriori import Apriori
import operator
import numpy as np


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

if __name__ == '__main__':
    f = PartitionByTopics(createTransactions=True)

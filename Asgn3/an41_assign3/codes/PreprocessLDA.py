__author__ = 'Abhishek'
import time
import math
# from collections import OrderedDict
from Apriori import Apriori
import operator
import numpy as np

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

if __name__ == '__main__':
    f = LDAInput(createVocabFlag=True, tokenizeFlag=True)

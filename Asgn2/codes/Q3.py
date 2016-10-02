__author__ = 'Abhishek'
from Apriori import *

if __name__ == '__main__':
    apriori = Apriori('../data/data.transaction', 20)
    L = apriori.execute()

    # Q3.1a:
    total = 0
    for level in L:
        total += len(level)
    print '3.1a: For minsup=20, Total frequent patterns:', total

    # Q3.1b
    print '3.1b: Frequent patterns with length 3:', len(L[2])#, '. They are:', L[2]

    # Q3.1c
    maxPatterns = apriori.getMaxPatterns()
    print '3.1c: Max patterns:', len(maxPatterns)#, '. They are:', maxPatterns


    apriori = Apriori('../data/data.transaction', 10)
    L = apriori.execute()
    # Q3.2a:
    total = 0
    for level in L:
        total += len(level)
    print '3.2a: For minsup=10, Total frequent patterns:', total

    # Q3.2b
    print '3.2b: Frequent patterns with length 3:', len(L[2])#, '. They are:', L[2]

    # Q3.2c
    maxPatterns = apriori.getMaxPatterns()
    print '3.2c: Max patterns:', len(maxPatterns)#, '. They are:', maxPatterns

    # Q3.2d
    print '3.2d: Confidence for [C,E]->[A] is:\n', apriori.getConfidence(['C','E'],['A'])

    # Q3.2e
    print '3.2e: Confidence for [A,B,C]->[E] is:\n', apriori.getConfidence(['A','B','C'],['E'])
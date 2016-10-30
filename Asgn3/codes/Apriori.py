__author__ = 'Abhishek'
import time
class Apriori():
    def __init__(self, databaseFile, minsup=20, relativeMinSup=0.01, setRelative=False):
        f = open(databaseFile, 'r')
        self.database = []
        for line in f.readlines():
            items = line.split()
            self.database.append(sorted(items))
        self.reverse_index = self.make_reverse_index()
        if setRelative:
            self.minsup = relativeMinSup*len(self.database)
        else:
            self.minsup = minsup
        self.L = []
        self.Lcounts = {}

    def find_frequent1_itemsets(self):
        itemCounts = {}
        # for transaction in self.database:
        #     for item in transaction:
        #         if item not in itemCounts:
        #             itemCounts[item] = 1
        #         else:
        #             itemCounts[item] += 1

        for item in self.reverse_index:
            if len(self.reverse_index[item])>=self.minsup:
                itemCounts[item] = len(self.reverse_index[item])

        frequentOnes = []
        for item in itemCounts:
            frequentOnes.append([item])

        self.Lcounts[1] = itemCounts
        return frequentOnes

    def apriori_gen(self, Lprev):
        C = []  # New candidates
        for idx1,item1 in enumerate(Lprev):
            for idx2,item2 in enumerate(Lprev):
                if idx1 < idx2:
                    if item1[:-1] != item2[:-1]:
                        continue
                    else:
                        toAppend = sorted([item1[-1],item2[-1]])
                        newCandidate = item1[:-1]+toAppend
                        if not self.has_infrequent_subset(newCandidate):
                            C.append(newCandidate)
        return C

    def has_infrequent_subset(self, candidateK):
        for idx, element in enumerate(candidateK):
            subset = candidateK[0:idx]+candidateK[idx+1:]

    def make_reverse_index(self):
        reverse_index = {}
        for idx,tran in enumerate(self.database):
            for item in tran:
                if item not in reverse_index:
                    reverse_index[item] = set()
                reverse_index[item].add(idx)
        return reverse_index

    def execute(self):
        self.L.append(self.find_frequent1_itemsets()) # L1
        while(1):
            C = self.apriori_gen(self.L[-1])
            k = len(self.L[-1][0])+1
            self.Lcounts[k] = {}
            for idx, candidateSet in enumerate(C):
                occurence_sets = []
                for item in candidateSet:
                    occurence_sets.append(set(self.reverse_index[item]))
                common_occurence = set.intersection(*occurence_sets) # List expansion!
                self.Lcounts[k][tuple(candidateSet)] = len(common_occurence)
                # if len(self.L) == 2 and len(common_occurence) >= self.minsup:
                #     print candidateSet, common_occurence

            # for idx,transaction in enumerate(self.database):
                # for candidate in C:
                    # if set(candidate)<=set(transaction):
                    #     if tuple(candidate) not in self.Lcounts[k]:
                    #         self.Lcounts[k][tuple(candidate)] = 0
                    #     self.Lcounts[k][tuple(candidate)] += 1

            Lnew = []
            toPop = []
            for subset in self.Lcounts[k]:
                if self.Lcounts[k][subset] >= self.minsup:
                    Lnew.append(list(subset))
                else:
                    toPop.append(subset)
            for element in toPop:
                self.Lcounts[k].pop(element)
            if len(Lnew) == 0:
                break
            else:
                self.L.append(Lnew)
        return self.L

    def getConfidence(self, subset1, subset2):
        subset3 = subset1+subset2
        subset1, subset2, subset3 = sorted(subset1), sorted(subset2), sorted(subset3)

        if tuple(subset3) in self.Lcounts[len(subset3)]:
            if tuple(subset1) in self.Lcounts[len(subset1)]:
                print self.Lcounts[len(subset3)][tuple(subset3)], '/', self.Lcounts[len(subset1)][tuple(subset1)], '='
                return float(self.Lcounts[len(subset3)][tuple(subset3)]) / self.Lcounts[len(subset1)][tuple(subset1)]
        else:
            return 0

    def getClosedPatterns(self):
        self.closedPatterns = {}

        if len(self.Lcounts[len(self.Lcounts)]) == 0:
            maxLevel = len(self.Lcounts) - 1
        else:
            maxLevel = len(self.Lcounts)
        for idx in range(maxLevel):
            if idx == maxLevel-1:
                for itemset in self.Lcounts[maxLevel]:
                    self.closedPatterns[self.itemSet2Tuple(itemset)] = self.Lcounts[maxLevel][itemset]
            else:
                # Check if each subset of the current level is a member of any subset of the next level
                for itemset in self.Lcounts[idx+1]:
                    closedFlag = True
                    for bigItemset in self.Lcounts[idx+2]:
                        if set(itemset) <= set(bigItemset):
                            if self.Lcounts[idx+1][itemset] == self.Lcounts[idx+2][bigItemset]:
                                closedFlag = False
                                break
                    if closedFlag == True:
                        self.closedPatterns[self.itemSet2Tuple(itemset)] = self.Lcounts[idx+1][itemset]
        return self.closedPatterns

    def getMaxPatterns(self):
        self.maxPatterns = {}

        if len(self.Lcounts[len(self.Lcounts)]) == 0:
            maxLevel = len(self.Lcounts) - 1
        else:
            maxLevel = len(self.Lcounts)
        for idx in range(maxLevel):
            if idx == maxLevel-1:
                for itemset in self.Lcounts[maxLevel]:
                    self.maxPatterns[self.itemSet2Tuple(itemset)] = self.Lcounts[maxLevel][itemset]
            else:
                # Check if each subset of the current level is a member of any subset of the next level
                for itemset in self.Lcounts[idx+1]:
                    maxFlag = True
                    for bigItemset in self.Lcounts[idx+2]:
                        if set(itemset) <= set(bigItemset):
                            maxFlag = False
                            break
                    if maxFlag == True:
                        self.maxPatterns[self.itemSet2Tuple(itemset)] = self.Lcounts[idx+1][itemset]
        return self.maxPatterns

    def itemSet2Tuple(self, itemSet):
        if type(itemSet) == str:
            return itemSet
        else:
            return tuple(itemSet)
__author__ = 'Abhishek'

class Apriori():
    def __init__(self, databaseFile, minsup):
        f = open(databaseFile, 'r')
        self.database = []
        for line in f.readlines():
            items = line.split()
            self.database.append(sorted(items))
        self.minsup = minsup
        self.L = []
        self.Lcounts = {}

    def find_frequent1_itemsets(self):
        itemCounts = {}
        for transaction in self.database:
            for item in transaction:
                if item not in itemCounts:
                    itemCounts[item] = 1
                else:
                    itemCounts[item] += 1

        frequentOnes = []
        for item in itemCounts:
            if itemCounts[item] >= self.minsup:
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

    def execute(self):
        self.L.append(self.find_frequent1_itemsets()) # L1
        while(1):
            C = self.apriori_gen(self.L[-1])
            k = len(self.L[-1][0])+1
            self.Lcounts[k] = {}
            for transaction in self.database:
                for candidate in C:
                    if set(candidate)<=set(transaction):
                        if tuple(candidate) not in self.Lcounts[k]:
                            self.Lcounts[k][tuple(candidate)] = 0
                        self.Lcounts[k][tuple(candidate)] += 1

            Lnew = []
            for subset in self.Lcounts[k]:
                if self.Lcounts[k][subset] >= self.minsup:
                    Lnew.append(list(subset))
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

    def getMaxPatterns(self):
        maxPatterns = []
        for idx, level in enumerate(self.L):
            if idx == len(self.L)-1:
                for subset in level:
                    maxPatterns.append(subset)
            else:
                # Check if each subset of the current level is a member of any subset of the next level
                for subset in level:
                    maxFlag = True
                    for bigSubset in self.L[idx+1]:
                        if set(subset) <= set(bigSubset):
                            maxFlag = False
                            break
                    if maxFlag == True:
                        maxPatterns.append(subset)

        return maxPatterns
__author__ = 'Abhishek'
import pandas as pd

class Cube():
    aggregateCubes = {}

    def __init__(self, filePath, delimiter='\t', idCol='True'):
        # Construct base cuboid
        self.baseCuboid = pd.read_csv(filePath, sep=delimiter)
        self.columns = list(self.baseCuboid.columns.values)
        if idCol:
            self.columns = self.columns[1:]

    def createAggregate(self, dimensions):
        # Given a tuple of input dimensions, create and return an aggregate cuboid
        if dimensions not in self.aggregateCubes:
            groupByList = []
            for idx, dimension in enumerate(dimensions):
                if dimension == self.columns[idx]:
                    groupByList.append(self.columns[idx])
                elif dimension == '*':
                    continue
            self.aggregateCubes[dimensions] = self.baseCuboid.groupby(groupByList)
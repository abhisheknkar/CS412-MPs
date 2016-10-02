__author__ = 'Abhishek'

from Cube import *

if __name__ == '__main__':
    cube = Cube('../data/data.business')

    # Q2b: The result is the same even if State is _not_ *, as there is a 1-1 correspondence from city->state
    query1 = ('City', '*', 'Category', 'Rating', 'Price')
    cube.createAggregate(query1)
    print 'The number of non-empty cells for the query:', str(query1), 'is: ', len(cube.aggregateCubes[query1])

    # Q2c
    query2 = ('*', 'State', 'Category', 'Rating', 'Price')
    cube.createAggregate(query2)
    print 'The number of non-empty cells for the query:', str(query2), 'is: ', len(cube.aggregateCubes[query2])

    # Q2d
    query3 = ('*', '*', 'Category', 'Rating', 'Price')
    cube.createAggregate(query3)
    print 'The number of non-empty cells for the query:', str(query3), 'is: ', len(cube.aggregateCubes[query3])

    # Q2e
    # Count for (Location(State) = "Illinois", *, Rating = "3", Price = "moderate")
    bc = cube.baseCuboid
    print 'The count for (Location(State) = "Illinois", *, Rating = "3", Price = "moderate") is:', \
        len(bc[bc['State']=='Illinois'][bc['Rating']==3][bc['Price']=='moderate'])

    # Q2f
    # Count for (Location(City) = "Chicago", Category= "food", *, *)
    print 'The count for (Location(City) = "Chicago", Category= "food", *, *) is:', \
        len(bc[bc['City']=='Chicago'][bc['Category']=='food'])
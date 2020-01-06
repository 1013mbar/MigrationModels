import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import random
import collections
import operator
import time

def avgMove(pop1,pop1Climate,pop2Climate,movingRatio,OppClimate):
    return((movingRatio*pop1*pop1Climate*pop2Climate)/((pop1Climate+OppClimate)*(pop1Climate+pop2Climate+OppClimate)))

# calculate the intervening opportunities with var 
def IO(var,point, point2):
    dist = distance.euclidean(point,point2)
    varT = []
    for el in np.copy(var).tolist():
        if el[1] <= dist and el[0] != point and el[0] != point2:
            varT.append(el[2])
    return np.max(varT)


#calculate all distances between all points in the grid to one specific point
def calcDistGrid(point,grid):
    i = 0
    x = grid.shape[0]
    y = grid.shape[1]
    distGrid = {}
    valGrid = []
    z = 0
    while i < x:
        j = 0
        while j < y:
            distGrid.update({(i,j): distance.euclidean((i,j),point)})
            valGrid.append(((i,j),distance.euclidean((i,j),point),grid[(i,j)]))
            j +=1
            z += 1
        i += 1
    return (collections.OrderedDict(sorted(distGrid.items(),key=operator.itemgetter(1))),valGrid)


#calculate the migration from i to j for every j
def update(grid, climateGrid, point1):
    climateGridT = checkForZeroPop(np.copy(climateGrid+grid))
    #distgridAll[0] contains an ordered dict of all point and their distance to point1
    #distrgridAll[1] contains an unordered list with all points, their values and their distance to point1
    distGridAll  = calcDistGrid(point1,np.copy(climateGridT))
    distGrid = distGridAll[0]
    for el in distGrid:
        if(el != point1):
            # the migrants moving from point1 to el 
            m = avgMove(grid[point1],climateGridT[point1],climateGridT[el],movingRatio,IO(distGridAll[1],point1,el))
            if((climateGrid[el] == 0) and (grid[point1] >= m) and el != point1):
                grid[point1] -= m
                grid[el] += m
    return grid


#calculate the difference between the original population and the new population after migrants moved from one origin (point1) to all destinations
def calcDiff(grid, climateGrid, point1):
    grid1 = np.copy(grid)
    grid = update(grid, climateGrid, point1)
    return(np.copy(grid-grid1))

#ensure that there are no negative value in the population
def checkForZeroPop(gridT0):
    i = 0   
    while i < x:
        j = 0
        while j < y:
            if(gridT0[(i,j)] < 0):
                gridT0[(i,j)] = 0
            j += 1
        i += 1
    return gridT0
    



grid = np.genfromtxt('grid.csv', delimiter=' ') 
# size of the grid
x = grid.shape[0]
y = grid.shape[1]


# fraction of peope moving compared to the whole population
movingRatio = 0.25

#population = np.sum(popDistr)

climateGrid = np.zeros((x,y))

i = 0
while i < x:
    j = 0
    while j < y:
        if(i+j < 0):
            climateGrid[(i,j)] = 10
        j += 1
    i += 1

gridT0  = np.copy(grid)

def allUpdate(grid,climateGrid):
    allSum = 0
    allGrids = []
    i = 0
    print("--------")
    while i < x:
        j = 0
        while j < y:
            # calculate the number of migrants for one origin, origin = (i,j)
            gridTemp = np.copy(calcDiff(np.copy(grid),climateGrid,(i,j)))
            #sum the migrants off all origins
            allGrids.append(gridTemp)
            j += 1
        i += 1
    gridTemp = np.zeros((x,y))
    # apply the migrations changes to the previous grid
    for el in allGrids:
        grid = grid+el
        gridTemp = gridTemp + el
    print("Number of migrants: " + str(np.sum(np.absolute(gridTemp))/2))
    return grid


t1 = time.time()
gridT1 = allUpdate(np.copy(gridT0),climateGrid)
t2 = time.time()
print(str(t2-t1))
print(1)
gridT2 = allUpdate(np.copy(gridT1),climateGrid)
print(2)
gridT3 = allUpdate(np.copy(gridT2),climateGrid)
print(3)
gridT4 = allUpdate(np.copy(gridT3),climateGrid)
print(4)
gridT5 = allUpdate(np.copy(gridT4),climateGrid)
print(5)
gridT6 = allUpdate(np.copy(gridT5),climateGrid)
print(6)
gridT7 = allUpdate(np.copy(gridT6),climateGrid)
print(7)
gridT8 = allUpdate(np.copy(gridT7),climateGrid)
t3 = time.time()
print(str(t3-t1))


fig, ax = plt.subplots(nrows=3, ncols=6)

ax[0][0].matshow(grid)
ax[0][1].matshow(gridT1)
ax[0][2].matshow(gridT2)
ax[1][0].matshow(gridT3)
ax[1][1].matshow(gridT4)
ax[1][2].matshow(gridT5)
ax[2][0].matshow(gridT6)
ax[2][1].matshow(gridT7)
ax[2][2].matshow(gridT8)

ax[0][3].matshow(gridT1- grid)
ax[0][4].matshow(gridT2 - gridT1)
ax[0][5].matshow(gridT2 - gridT3)
ax[1][3].matshow(gridT3 - gridT4)
ax[1][4].matshow(gridT4 - gridT5)
ax[1][5].matshow(gridT5 - gridT6)
ax[2][3].matshow(gridT6 - gridT7)
ax[2][4].matshow(gridT7 - gridT8)
ax[2][5].matshow(climateGrid)

plt.show()

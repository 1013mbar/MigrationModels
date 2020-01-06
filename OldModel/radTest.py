import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import random
import collections
import operator
import time

def avgMove(pop1,pop1Climate,pop2Climate,movingRatio,OppClimate):
    return((movingRatio*pop1*pop1Climate*pop2Climate)/((pop1Climate+OppClimate)*(pop1Climate+pop2Climate+OppClimate)))

def intervOpp(interGrid,point1, point2):
    dist = distance.euclidean(point1,point2)
    i =  0
    interOpp = 0
    while i < x:
        j = 0
        while j < y:
            if distance.euclidean(point1,(i,j)) <= dist and (i,j)!= point1 and (i,j)!= point2 and interOpp < interGrid[(i,j)]:
                interOpp = interGrid[(i,j)]
            j+=1
        i+=1
    return interOpp

def calcDistGrid(shape,point):
    i = 0
    x = shape[0]
    y = shape[1]
    distGrid = {}
    z = 0
    while i < x:
        j = 0
        while j < y:
            distGrid.update({(i,j): distance.euclidean((i,j),point)})
            j +=1
            z += 1
        i += 1
    return collections.OrderedDict(sorted(distGrid.items(),key=operator.itemgetter(1)))

def update(grid, climateGrid, distGrid, point1):
    climateGridT = checkForZeroPop(np.copy(climateGrid+grid))
    #climateGrid = climateGrid + grid
    t1 = time.time()
    for el in distGrid:
        m = avgMove(grid[point1],climateGridT[point1],climateGridT[el],movingRatio,intervOpp(climateGridT,point1,el))
        if((climateGrid[el] == 0) and (grid[point1] >= m) and el != point1):
            grid[point1] -= m
            grid[el] += m
    return grid

def calcDiff(grid, climateGrid, distGrid, point1):
    grid1 = np.copy(grid)
    grid = update(grid, climateGrid, distGrid, point1)
    return(np.copy(grid-grid1))

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
        if(i+j <= 8):
            climateGrid[(i,j)] = 0
        j += 1
    i += 1

#point1 = (1,3)
#grid[point1] = 1000

gridT0  = np.copy(grid)

def allUpdate(grid,climateGrid):
    allSum = 0
    allGrids = []
    i = 0
    print("--------")
    while i < x:
        j = 0
        while j < y:
            distGrid = calcDistGrid(grid.shape, (i,j)).keys()
            gridTemp = np.copy(calcDiff(np.copy(grid),climateGrid,distGrid,(i,j)))
            allGrids.append(gridTemp)
            #allSum += np.sum(np.absolute(gridTemp))
            j += 1
        i += 1
    gridTemp = np.zeros((x,y))
    for el in allGrids:
        grid = grid+el
        gridTemp = gridTemp + el
    print("Number of migrants: " + str(np.sum(np.absolute(gridTemp))/2))
    return grid

#point1 = (4,4)
#point2 = (3,2)
#print(intervOpp(grid,point1,point2))
#print(np.round(grid - update(np.copy(grid), climateGrid, calcDistGrid((x,y),point1), point1)))
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

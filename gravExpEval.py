import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import random
import collections
import operator
import time
import multiprocessing as mp

def avgMove(pop1,pop2,distance):
    return((pop1*pop2)/np.exp(distance*.01))

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


def update(grid,distGrid,point1):
    grid[point1] += 21000
    for el in distGrid:
        m = avgMove(grid[point1],grid[el],distance.euclidean(point1,el))
        if((grid[point1] >= m) and el != point1):
            grid[point1] -= m
            grid[el] += m
    return grid


def combUpdate(x,y,i,j,grid):
    distGrid = calcDistGrid((x,y),(i,j))
    gridTemp = np.copy(update(np.copy(grid),distGrid,(i,j))- grid)
    return_list.append(gridTemp)

def allUpdate(grid):
    allSum = 0
    allGrids = []
    i = 0
    print("--------")
    procs = []
    while i < x:
        j = 0
        while j < y:
            proc = mp.Process(target=combUpdate, args=(x,y,i,j,grid,))
            procs.append(proc)
            proc.start()
            j += 1
        i += 1
    for el in procs:
        el.join()
    allGrids = return_list
    gridTemp = np.zeros((x,y))
    for el in allGrids:
        grid = grid+el
        gridTemp += el
    print("Number of migrants: " + str(np.sum(np.absolute(gridTemp))/2))
    return grid

if __name__ == '__main__':
    
    manager = mp.Manager()
    return_list = manager.list()
    
    grid = np.genfromtxt('test_data/test_2000.csv', delimiter=' ') 
    ind2005 = np.genfromtxt('test_data/test_2005.csv', delimiter=' ') 
    ind2010 = np.genfromtxt('test_data/test_2010.csv', delimiter=' ') 
    ind2015 = np.genfromtxt('test_data/test_2015.csv', delimiter=' ') 
    ind2020 = np.genfromtxt('test_data/test_2020.csv', delimiter=' ') 
    # size of the grid
    x = grid.shape[0]
    y = grid.shape[1]


    print("Population for t = 0: " + str(np.sum(np.absolute(grid))))
    print("--------Population Change----------")
    print(str(np.sum(np.absolute(grid)-np.absolute(ind2005))))
    print(str(np.sum(np.absolute(ind2005)-np.absolute(ind2010))))
    print(str(np.sum(np.absolute(ind2010)-np.absolute(ind2015))))
    print(str(np.sum(np.absolute(ind2015)-np.absolute(ind2020))))
    print("-----------------------------------")
    print("--------Migration Change Data----------")
    print(str(np.sum(np.absolute(grid-ind2005))))
    print(str(np.sum(np.absolute(ind2005-ind2010))))
    print(str(np.sum(np.absolute(ind2010-ind2015))))
    print(str(np.sum(np.absolute(ind2015-ind2020))))
    print("-----------------------------------")



    errors = []
    gridT0  = np.copy(grid)
    t1 = time.time()
    gridT1 = allUpdate(np.copy(gridT0))
    t2 = time.time()
    print(str(t2-t1))
    print("Population: " + str(np.sum(np.absolute(gridT1))))
    errors.append(np.sum(np.absolute(gridT1-ind2005)))
    print("Deviation: "+ str(np.sum(np.abs(gridT1-ind2005))))
    return_list = manager.list()
    gridT2 = allUpdate(np.copy(gridT1))
    print("Population: " + str(np.sum(np.absolute(gridT2))))
    errors.append(np.sum(np.absolute(gridT2-ind2010)))
    print("Deviation: "+str(np.sum(np.abs(gridT2-ind2010))))
    return_list = manager.list()
    gridT3 = allUpdate(np.copy(gridT2))
    print("Population: " + str(np.sum(np.absolute(gridT3))))
    errors.append(np.sum(np.absolute(gridT3-ind2015)))
    print("Deviation: "+str(np.sum(np.abs(gridT3-ind2015))))
    return_list = manager.list()
    gridT4 = allUpdate(np.copy(gridT3))
    print("Population: " + str(np.sum(np.absolute(gridT4))))
    errors.append(np.sum(np.absolute(gridT4-ind2020)))
    print("Deviation: "+str(np.sum(np.abs(gridT4-ind2020))))

    print("--------------")
    print("Mean error: " + str(np.mean(errors)))
    
    
    print("--------Migration Change Simulation----------")
    print(str(np.sum(np.absolute(grid-gridT1))))
    print(str(np.sum(np.absolute(gridT1-gridT2))))
    print(str(np.sum(np.absolute(gridT2-gridT3))))
    print(str(np.sum(np.absolute(gridT3-gridT4))))
    print("-----------------------------------")
    
    fig, ax = plt.subplots(nrows=2, ncols=6)
    ax[0][0].matshow(grid)
    ax[0][1].matshow(gridT1)
    ax[0][2].matshow(gridT2)
    ax[1][0].matshow(gridT3)
    ax[1][1].matshow(gridT4)
    ax[1][2].matshow([[0,0],[0,0]])


    ax[0][3].matshow(grid)
    ax[0][4].matshow(ind2005)
    ax[0][5].matshow(ind2010)
    ax[1][3].matshow(ind2015)
    ax[1][4].matshow(ind2020)
    ax[1][5].matshow([[0,0],[0,0]])

    plt.show()

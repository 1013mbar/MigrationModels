import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import random
import collections
import operator
import time
import multiprocessing as mp
import matplotlib

def avgMove(pop1,pop2,distance):
    coeff = 2
    return((pop1*pop2)/(distance**coeff))


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
    for el in distGrid:
        m = 0
        if(el != point1):
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
    migrantsT = 0
    for el in allGrids:
        grid = grid+el
        migrantsT += np.sum(np.absolute(el))/2
    print("Number of migrants: " + str(migrantsT))
    migrants.append(migrantsT)
    return grid

if __name__ == '__main__':
    grids = []
    grids.append(np.genfromtxt('decreasingUrban.csv', delimiter=' '))
    grids.append(np.genfromtxt('randDecreasingUrban.csv', delimiter=' ')) 
    grids.append(np.genfromtxt('randOneCity.csv', delimiter=' ')) 
    grids.append(np.genfromtxt('twoCities.csv', delimiter=' '))
    grids.append(np.genfromtxt('randRural.csv', delimiter=' '))
    grids.append(np.genfromtxt('urban.csv', delimiter=' ')) 
    # size of the grid 

    k = 0
    for grid in grids:
    
        manager = mp.Manager()
        return_list = manager.list()
        coeff = 0
        # size of the grid
        x = grid.shape[0]
        y = grid.shape[1]
        migrants = []


        gridT0  = np.copy(grid)
        t1 = time.time()
        gridT1 = allUpdate(np.copy(gridT0))
        t2 = time.time()
        print(str(t2-t1))
        print("Population: " + str(np.sum(np.absolute(gridT1))))
        return_list = manager.list()
        gridT2 = allUpdate(np.copy(gridT1))
        print("Population: " + str(np.sum(np.absolute(gridT2))))
        return_list = manager.list()
        gridT3 = allUpdate(np.copy(gridT2))
        print("Population: " + str(np.sum(np.absolute(gridT3))))
        return_list = manager.list()
        gridT4 = allUpdate(np.copy(gridT3))
        print("Population: " + str(np.sum(np.absolute(gridT4))))
        return_list = manager.list()
        gridT5 = allUpdate(np.copy(gridT4))
        print("Population: " + str(np.sum(np.absolute(gridT5))))
        return_list = manager.list()
        gridT6 = allUpdate(np.copy(gridT5))
        print("Population: " + str(np.sum(np.absolute(gridT6))))
        return_list = manager.list()
        gridT7 = allUpdate(np.copy(gridT6))
        print("Population: " + str(np.sum(np.absolute(gridT7))))
        return_list = manager.list()
        gridT8 = allUpdate(np.copy(gridT7))
        t3 = time.time()
        print(str(t3-t1))
    
        fig, ax = plt.subplots(nrows=3, ncols=6)
        fig.set_size_inches(18.5, 10.5)
    
        ax[0][0].matshow(grid,cmap='ocean',vmin = 25,vmax = 2500)
        ax[0][1].matshow(gridT1,cmap='ocean',vmin = 25,vmax = 2500)
        ax[0][2].matshow(gridT2,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][0].matshow(gridT3,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][1].matshow(gridT4,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][2].matshow(gridT5,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][0].matshow(gridT6,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][1].matshow(gridT7,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][2].matshow(gridT8,cmap='ocean',vmin = 25,vmax = 2500)
        
        #ax[0][0].matshow(grid,cmap='ocean')
        #ax[0][1].matshow(gridT1,cmap='ocean')
        #ax[0][2].matshow(gridT2,cmap='ocean')
        #ax[1][0].matshow(gridT3,cmap='ocean')
        #ax[1][1].matshow(gridT4,cmap='ocean')
        #ax[1][2].matshow(gridT5,cmap='ocean')
        #ax[2][0].matshow(gridT6,cmap='ocean')
        #ax[2][1].matshow(gridT7,cmap='ocean')
        #ax[2][2].matshow(gridT8,cmap='ocean')
    
        ax[0][3].matshow(-grid+ gridT1,cmap='ocean',vmin = 25,vmax = 2500)
        ax[0][4].matshow(-gridT1 + gridT2,cmap='ocean',vmin = 25,vmax = 2500)
        ax[0][5].matshow(-gridT2 + gridT3,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][3].matshow(-gridT3 + gridT4,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][4].matshow(-gridT4 + gridT5,cmap='ocean',vmin = 25,vmax = 2500)
        ax[1][5].matshow(-gridT5 + gridT6,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][3].matshow(-gridT6 + gridT7,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][4].matshow(-gridT7 + gridT8,cmap='ocean',vmin = 25,vmax = 2500)
        ax[2][5].matshow(np.zeros((x,y)))
        plt.savefig("grav/grav_"+ str(k) +  "_coeff"+str(coeff)+ "_avgMig" + str(np.round(np.mean(migrants))) + "_pop"+ str(np.round(np.sum(np.absolute(gridT7))))+ ".png",dpi=fig.dpi)
        #plt.show()
        k +=1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random
from scipy.spatial import distance



x = y = 15
city1 = (3,3)
city2 = (11,11)
urbanSize = 2.5

grid = np.ones((x,y))

def twoCities(grid,city1, city2,urbanSize):
    x = grid.shape[0]
    y = grid.shape[1]
    i = 0
    while i < x:
        j = 0
        while j < y:
            if(distance.euclidean(city1, (i,j)) <= urbanSize or distance.euclidean(city2, (i,j)) <= urbanSize):
                grid[(i,j)] = 2500
            j += 1
        i += 1
    grid[city1] = 25000
    grid[city2] = 25000
    return grid

def randOneCity(grid,city1,urbanSize):
    x = grid.shape[0]
    y = grid.shape[1]
    i = 0
    while i < x:
        j = 0
        while j < y:
            grid[(i,j)] = random.randint(1,200)
            j += 1
        i += 1
    i = 0
    while i < x:
        j = 0
        while j < y:
            if(distance.euclidean(city1, (i,j)) <= urbanSize):
                grid[(i,j)] = 250
            j += 1
        i += 1
    grid[city1] = 2500
    return grid

def randRural(grid):
    x = grid.shape[0]
    y = grid.shape[1]
    i = 0
    while i < x:
        j = 0
        while j < y:
            grid[(i,j)] = random.randint(1,200)
            j += 1
        i += 1
    i = 0
    return grid

def decreasingUrban(grid):
    x = grid.shape[0]
    y = grid.shape[1]
    city1 = (np.round(x/2),np.round(y/2))
    urbanSize = x/2-1
    i = 0
    while i < x:
        j = 0
        while j < y:
            dist = distance.euclidean(city1, (i,j)) 
            if(dist <= urbanSize):
                grid[(i,j)] = 2500/(10*dist)
            j += 1
        i += 1
    grid[city1] = 2500
    return grid

def randDecreasingUrban(grid):
    grid = randRural(grid)
    x = grid.shape[0]
    y = grid.shape[1]
    city1 = (np.round(x/2),np.round(y/2))
    urbanSize = x/2-2
    i = 0
    while i < x:
        j = 0
        while j < y:
            dist = distance.euclidean(city1, (i,j)) 
            if(dist <= urbanSize):
                grid[(i,j)] = 2500/(10*dist)
            j += 1
        i += 1
    grid[city1] = 2500
    return grid

def urbanDistr(grid):
    x = grid.shape[0]
    y = grid.shape[1]
    city1 = (np.round(x/2),np.round(y/2))
    urbanSize = x/2
    i = 0
    while i < x:
        j = 0
        while j < y:
            dist = distance.euclidean(city1, (i,j)) 
            if(dist <= urbanSize):
                grid[(i,j)] = 2500/(10*dist)
            j += 1
        i += 1
    grid[city1] = 250
    grid[(4,6)] = 2500
    grid[(7,4)] = 2500
    grid[(7,9)] = 2500
    grid[(10,7)] = 2500
    #grid[city1 + np.array([0,2])] = 2500
    #grid[city1 + np.array([-2,0])] = 2500
    #grid[city1 + np.array([0,-2])] = 2500
    return grid

#grid = twoCities(grid,city1,city2,urbanSize)
#grid = randOneCity(grid,city1,urbanSize)
#grid = randRural(grid)
#grid = decreasingUrban(grid)
#grid = randDecreasingUrban(grid)
grid = urbanDistr(grid)


np.savetxt("urbanDistr.csv",grid)
plt.matshow(grid,cmap='ocean',vmin = 25,vmax = 2500)
plt.show()

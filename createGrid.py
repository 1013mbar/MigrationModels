import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random



x = y = 15
population = 100000

def decomp(population,districts):
    districtPop = []
    while population > 100:
        n = random.randint(1,population/100)
        if(n > population):
             n = population
        districtPop.append(n)
        population -= n
    districtPop.append(population)
    if(districts > len(districtPop)):
        districtPop.extend([10]*(districts-len(districtPop)))
    random.shuffle(districtPop)
    return(districtPop)

def implementGrid(gridT, popDistr):
    x = grid.shape[0]
    y = grid.shape[1]
    i = 0
    while i < x:
        j = 0
        while j < y:
            grid[(i,j)] = popDistr[x*i+j]
            j+=1
        i+=1
    return grid         
        

popDistr = decomp(population,(x*y))
grid = np.zeros((x,y))
grid = implementGrid(grid,popDistr)

np.savetxt("grid.csv",grid)
plt.matshow(grid)
plt.show()

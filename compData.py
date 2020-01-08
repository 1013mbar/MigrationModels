import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import random
import collections
import operator
import time


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
print("--------Migration Change----------")
print(str(np.sum(np.absolute(grid-ind2005))))
print(str(np.sum(np.absolute(ind2005-ind2010))))
print(str(np.sum(np.absolute(ind2010-ind2015))))
print(str(np.sum(np.absolute(ind2015-ind2020))))
print("-----------------------------------")



fig, ax = plt.subplots(nrows=2, ncols=4)
ax[0][0].matshow(grid)
ax[0][1].matshow(ind2005)
ax[0][2].matshow(ind2010)
ax[0][3].matshow(ind2015)
ax[1][0].matshow(ind2005-grid)
ax[1][1].matshow(ind2010-ind2005)
ax[1][2].matshow(ind2015-ind2010)
ax[1][3].matshow(ind2020-ind2015)


plt.show()

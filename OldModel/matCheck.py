import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random



x = y = 5

grid = np.zeros((x,y))

grid[(4,4)] = 1
grid[(3,2)] = 2
 
plt.matshow(grid)
plt.show()

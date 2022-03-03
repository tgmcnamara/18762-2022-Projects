import numpy as np

def initialize(devices, size_Y):
    #Initialize the entire V vector to have values of 0.1
    V_init = np.ones((size_Y,1),dtype=np.float)/10
    return V_init

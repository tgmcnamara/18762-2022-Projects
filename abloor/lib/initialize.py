import numpy as np

def initialize(devices, size_Y):
    V_init = np.ones((size_Y,1),dtype=np.float)/10
    #print(V_init)
    return V_init

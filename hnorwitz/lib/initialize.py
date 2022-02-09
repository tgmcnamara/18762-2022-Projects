#may need to import numpy here and some other things
import numpy as np
def initialize(devices, size_Y):
    

    V_init = np.zeros((size_Y,1))
    for i in range(size_Y):
        v = 0.1
        V_init[i,0] = v
    

    #should creat the J vector based off number of nodes
    #V_init = None #think we are supposred to set this to 0.1 (ORIGINAL)
    return V_init
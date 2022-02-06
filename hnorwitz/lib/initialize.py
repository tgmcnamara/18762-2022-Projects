#may need to import numpy here and some other things
import numpy as np
def initialize(devices, size_Y):
    #Yv = J this is construc intial v at t=-0? 
    row = []
    for i in range(size_Y):
        v = 0.1
        row.append(v)
    V_init = row

    #should creat the J vector based off number of nodes
    #V_init = None #think we are supposred to set this to 0.1 (ORIGINAL)
    return V_init
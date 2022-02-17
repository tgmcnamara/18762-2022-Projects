#may need to import numpy here and some other things
import numpy as np
def initialize(devices, size_Y):
    
    #Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
    #J = np.zeros((size_Y,1))
    V_init = np.zeros((size_Y,1))
    
    for i in range(size_Y):
        v = 0.0001
        V_init[i,0] = v
    
    #####CAN DO THE BELOW FOR DC ANALYSIS intial conditions
    #for resistor in devices['resistors']:
    #    resistor.stamp_dense(Y)
                #print(Y)
    #for capacitors in devices['capacitors']:
    #    capacitors.stamp_open(Y)
                #capacitors.stamp_dense(Y,J,d_t,V_init,t)
    #for inductors in devices['inductors']:
    #    inductors.stamp_short(Y)
    #should creat the J vector based off number of nodes
    #V_init = None #think we are supposred to set this to 0.1 (ORIGINAL)
    return V_init
#may need to import numpy here and some other things
import numpy as np
def initialize(devices, size_Y):
    #Yv = J this is construc intial v at t=-0? 
    row = []
    for i in range(size_Y):
        v = 0.1
        row.append(v)
    V_init = row
###Posssible idea (maybe this belongs in run time domain simulation)
    #THis constructs the overall y and J matrixes
    Y= np.zeros((size_Y,size_Y)) #creates the Y matrix of 0s
    J = np.zeros((1,size_Y))
    for resistor in devices['resistors']:
        Y = Y + resistor.stamp_dense(size_Y)#call dense stamp fucntion create Y matrix with stamp and addes it to y

    for capacitors in devices['capacitors']:
        Y = Y + capacitors.stamp_dense()#not sure what things it need to take in

    for inductors in devices['inductors']:
        Y = Y +  inductors.stamp_dense()

    for voltage_sources in devices['voltage_sources']:
        Y = voltage_sources.stamp_dense(size_Y)
######

    #should creat the J vector based off number of nodes
    #V_init = None #think we are supposred to set this to 0.1 (ORIGINAL)
    return V_init
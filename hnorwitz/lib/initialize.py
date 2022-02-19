#may need to import numpy here and some other things
import numpy as np
from classes.Nodes import Nodes
def initialize(devices, size_Y):
    
    #####INITIALIZEING V_INIT AS VECTOR OF 0 SET EACH ENTRY TO .0001
    V_init = np.zeros((size_Y,1))
    
    for i in range(size_Y):
        v = 0.0001
        V_init[i,0] = v
    
    #####ATTEMPTING TO DO DC ANALYSIS TO GET INITIAL CONDITIONS FOR TIME 0-##########
    #Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
    #J = np.zeros((size_Y,1))
    #for resistor in devices['resistors']:
    #    resistor.stamp_dense(Y)
                #print(Y)
    #for capacitors in devices['capacitors']:
    #    capacitors.stamp_open(Y)
                #capacitors.stamp_dense(Y,J,d_t,V_init,t)
    #for inductors in devices['inductors']:
    #    inductors.stamp_short(Y)
    #should creat the J vector based off number of nodes
    #for voltage_sources in devices['voltage_sources']:
        #voltage_sources.stamp_dense(Y,J, t)
                #print(Y)
                #print(J)
    #Y[Nodes.node_index_dict['gnd'],:] = 0
    #Y[:,Nodes.node_index_dict['gnd']] = 0
    #Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
    #J[Nodes.node_index_dict['gnd'],:] = 0
    #v = np.linalg.solve(Y,J)
    #V_init =v.reshape[-1]
    ####################################################
    return V_init
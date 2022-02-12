from platform import node
import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)
import scipy as sp
from classes.Capacitors import Capacitors #tried importning scipy but said it was already installed
from classes.Nodes import Nodes
from matplotlib import pyplot as plt

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    d_t = .00001# detlat t time step
    #time = np.linspace((0,SETTINGS['Simulation Time'],d_t))
    time = np.arange(0,SETTINGS['Simulation Time'],d_t)
    size_t = len(time)
    V_waveform =np.zeros((size_Y, size_t)) #None #Should this be a matrix
    t_init = 0
    #waveform should contain voltages and currents at every node over set time
    #ie matrix where if plotted heach colum vector shows voltage or current waveform of that node

    #FIRST CONSTRUCT INITIAL Y AND J matrix
    #THis constructs the overall y and J matrixes
    Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
    J = np.zeros((size_Y,1))
    
    #for resistor in devices['resistors']:
       # resistor.stamp_dense(Y)

    #for capacitors in devices['capacitors']:
     #   capacitors.stamp_dense(Y, J, d_t, V_init, t_init)
        #should I be calling stamp_op 

    #for inductors in devices['inductors']:
        #inductors.stamp_dense(Y,J, d_t, V_init, t_init)

    #for voltage_sources in devices['voltage_sources']:
        #voltage_sources.stamp_dense(Y,J, t_init)
######

    #SECOND begin iterating over time
    #for look to iterate over time from
    #J = J*V_init #matrix mupliplication
    for t_ind in range(len(time)): #np.arange(0,SETTINGS['Simulation Time'],d_t,dtype=int): #going over the entire time
        t = time[t_ind]
        #J = Y*V_init #matrix mupliplication
        #for iter in range(SETTINGS.max_iters): #something feels off here
        if t == 0:#ALOT HAPPENS HERE
            for resistor in devices['resistors']:
                resistor.stamp_dense(Y)
                #print(Y)
            for capacitors in devices['capacitors']:
                capacitors.stamp_open(Y)
            for inductors in devices['inductors']:
                inductors.stamp_short(Y)
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y,J, t)
            Y[Nodes.node_index_dict['gnd'],:] = 0
            Y[:,Nodes.node_index_dict['gnd']] = 0
            Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
            v = np.linalg.solve(Y,J)
            print(type(v))
            #V_waveform.append(v)
            V_waveform[:,t_ind] = v.reshape(-1)#V_waveform[v,t_ind] #This does not want to work
            #print(V_waveform)
            Prevs_v = v
            #####(reset Y and Z)
            Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
            J = np.zeros((size_Y,1))
            ##restap it Y and jmatrix 
            for resistor in devices['resistors']:
                resistor.stamp_dense(Y)
            for capacitors in devices['capacitors']:
                capacitors.stamp_dense(Y, J, d_t, Prevs_v, t)
            for inductors in devices['inductors']:
                inductors.stamp_dense(Y,J, d_t, Prevs_v, t)
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y,J, t)

        else:
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y,J, t)
            for capacitors in devices['capacitors']:
                capacitors.stamp_dense(Y, J, d_t, Prevs_v, t)
            for inductors in devices['inductors']:
                inductors.stamp_dense(Y,J, d_t, Prevs_v, t)
            Y[Nodes.node_index_dict['gnd'],:] = 0
            Y[:,Nodes.node_index_dict['gnd']] = 0
            Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
            v = np.linalg.solve(Y,J)
            #V_waveform.append(v)
            V_waveform[:,t_ind] = v.reshape(-1)
            #print(V_waveform)
            Prevs_v = v
        
    #print(V_waveform)
    #need to get labeling and be able to distinguish lines
    V_waveform_T = np.transpose(V_waveform)
    #time = np.transpose(time)
    #plt.plot(time,V_waveform_T[:,4])#capacitor current
    #plt.plot(time,V_waveform_T[:,3])
    #plt.plot(time,V_waveform_T[:,1])#capacitor voltage
    plt.plot(time,V_waveform_T)
    plt.show()
    
    return V_waveform
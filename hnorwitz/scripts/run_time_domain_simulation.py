from platform import node
import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)
import scipy as sp
from classes.Capacitors import Capacitors #tried importning scipy but said it was already installed
from classes.Inductors import Inductors
from classes.Nodes import Nodes
from matplotlib import pyplot as plt

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    d_t = .0001# detlat t time step
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
                #print(J)
            for capacitors in devices['capacitors']:
                #capacitors.stamp_open(Y)
                capacitors.stamp_dense(Y,J,d_t,V_init,t)
                #print(Y)
                #print(J)
            for inductors in devices['inductors']:
                #inductors.stamp_short(Y)#,J,d_t,V_init, t)
                inductors.stamp_dense(Y,J,d_t,V_init,t)
                #print(Y)
                #print(J)
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y,J, t)#feel like i am messing up something here
                #print(Y)
                #print(J)


            Y[Nodes.node_index_dict['gnd'],:] = 0
            Y[:,Nodes.node_index_dict['gnd']] = 0
            Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1 
            J[Nodes.node_index_dict['gnd'],:] = 0 #not sure if I need this
            #print(Y)
            #From what I can tell it seems my last to columbs are zersos if I use cap_open and ind_short commands
            v = np.linalg.solve(Y,J)
            print(type(v))
            #V_waveform.append(v)
            V_waveform[:,t_ind] = v.reshape(-1)#V_waveform[v,t_ind] #This does not want to work
            #print(V_waveform)
            Prevs_v = v
            print(v)
            #####(reset Y and Z)
            #Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
            #J = np.zeros((size_Y,1))
            ##restap it Y and jmatrix 
            #for resistor in devices['resistors']:
            #    resistor.stamp_dense(Y)
            #for capacitors in devices['capacitors']:
            #    capacitors.stamp_dense(Y, J, d_t, Prevs_v, t)
            #for inductors in devices['inductors']:
            #    inductors.stamp_dense(Y,J, d_t, Prevs_v, t)
            #for voltage_sources in devices['voltage_sources']:
            #    voltage_sources.stamp_dense(Y,J, t)

        else:
            Y= np.zeros((size_Y,size_Y),dtype=float) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
            J = np.zeros((size_Y,1))
            for resistor in devices['resistors']:
                resistor.stamp_dense(Y)
                #print(Y)
                #print(J)
            for capacitors in devices['capacitors']:
                capacitors.stamp_dense(Y, J, d_t, Prevs_v, t)
                #print(Y)
                #print(J)
            for inductors in devices['inductors']:
                inductors.stamp_dense(Y,J, d_t, Prevs_v, t)
                #print(Y)
                #print(J)
            for voltage_sources in devices['voltage_sources']:
                voltage_sources.stamp_dense(Y,J, t)
                #print(Y)
                #print(J)
            Y[Nodes.node_index_dict['gnd'],:] = 0
            Y[:,Nodes.node_index_dict['gnd']] = 0
            Y[Nodes.node_index_dict['gnd'], Nodes.node_index_dict['gnd']] = 1
            J[Nodes.node_index_dict['gnd'],:] = 0
            v = np.linalg.solve(Y,J)
            #V_waveform.append(v)
            V_waveform[:,t_ind] = v.reshape(-1)
            #print(V_waveform)
            Prevs_v = v
            #print(v)
        
    #print(V_waveform)
    #need to get labeling and be able to distinguish lines
    #EVERYTHING BELOW THIS POINT COULD BE PUT IN PROCESSING
    V_waveform_T = np.transpose(V_waveform)
    #plt.plot(time,V_waveform_T)
    #plt.plot(time,V_waveform_T[:,4])
    #plt.show()
    
    #figure, axis = plt.subplots(1,
    V_load_2a = V_waveform_T[:,6] #- V_waveform_T[:,9] #V_waveform_T[:,12] #- V_waveform_T[:,6] 
    V_load_2b = V_waveform_T[:,7] #- V_waveform_T[:,10]#V_waveform_T[:,12] #- V_waveform_T[:,7]  
    V_load_2c = V_waveform_T[:,8] #- V_waveform_T[:,11]#V_waveform_T[:,12] #- V_waveform_T[:,8]
    plt.plot(time,V_load_2a)#,label="Va_load")
    plt.plot(time,V_load_2b,)#label="Vb_load")
    plt.plot(time,V_load_2c)#,label="Vc_load")
    plt.plot(time,V_waveform_T[:,12])
    #plt.set_title("load voltages")
    #plt.tight_layout()
    #plt.legend()
    plt.show()#This seems to give the same current plot as simulink even though expecting voltages

    plt.plot(time,V_waveform_T[:,20])
    plt.plot(time,V_waveform_T[:,22])
    plt.plot(time,V_waveform_T[:,24])
    plt.show()


    #plt.plot(time,V_waveform_T[:,1],label="1")
    #plt.plot(time,V_waveform_T[:,4], label="2")#current
    #plt.legend()
    #plt.show()
    figure, axis = plt.subplots(2,1)
    #note only need on set of labels
    ##l1 inductor voltages phase a b c
    axis[1,1].plot(time,V_waveform_T[:,6])#, label='l1_a')
    axis[1,1].plot(time,V_waveform_T[:,7])#, label='l1_b')
    axis[1,1].plot(time,V_waveform_T[:,8])#, label='l1_c')
    #axis[1,0].set_title("v_load voltages")
    ##l1 inductor current phase a b c
    axis[2,1].plot(time,V_waveform_T[:,20])#, label='l1_a')
    axis[2,1].plot(time,V_waveform_T[:,22])#, label='l1_b')
    axis[2,1].plot(time,V_waveform_T[:,24])#, label='l1_c')
    #axis[1,1].set_title("load currents")
    ##l2 inductor voltages phase a b c
    #axis[1,0].plot(time,V_waveform_T[:,6], label='l2_a')
    #axis[1,0].plot(time,V_waveform_T[:,7], label='l2_b')
    #axis[1,0].plot(time,V_waveform_T[:,8], label='l2_c')
    #axis[1,0].set_title("load voltages")
    ##l2 inductor currents phase a b c
    #axis[1,1].plot(time,V_waveform_T[:,9], label='l2_a')
    #axis[1,1].plot(time,V_waveform_T[:,10], label='l2_b')
    #axis[1,1].plot(time,V_waveform_T[:,11], label='l2_c')
    #axis[1,1].set_title("inductor 2 currents")
    ##voltage source voltages phase a b c
    #axis[2,0].plot(time,V_waveform_T[:,12], label='v_a')
    #axis[2,0].plot(time,V_waveform_T[:,13], label='v_b')
    #axis[2,0].plot(time,V_waveform_T[:,14], label='v_c')
    #axis[2,0].set_title("voltage sources voltages")
    ##voltage source currents phase a b c
    #axis[2,1].plot(time,V_waveform_T[:,25], label='phase_a')
    #axis[2,1].plot(time,V_waveform_T[:,26], label='phase_b')
    #axis[2,1].plot(time,V_waveform_T[:,27], label='phase_c')
    #axis[2,1].set_title("voltage sources currents")
    ##load voltages
    #axis[3,0].plot(time,V_waveform_T[:,6], label='phase_a')
    #axis[3,0].plot(time,V_waveform_T[:,7], label='phase_b')
    #axis[3,0].plot(time,V_waveform_T[:,8], label='phase_c')
    #axis[3,0].set_title("load voltages")
    ##Load currents
    #L_curra = V_waveform_T[:,20] + V_waveform_T[:,14] + V_waveform_T[:,25]
    #L_currb = V_waveform_T[:,22] + V_waveform_T[:,16] + V_waveform_T[:,26]
    #L_currc = V_waveform_T[:,24] + V_waveform_T[:,18] + V_waveform_T[:,27]
    #axis[3,1].plot(time,V_load_2a, label='phase_a')
    #axis[3,1].plot(time,, label='phase_b')
    #axis[3,1].plot(time,L_currc, label='phase_c')
    #axis[3,1].set_title("load currents")
    #plt.tight_layout()
    #plt.legend()
    plt.show()
    
    #don't really need to return anything
    return V_waveform
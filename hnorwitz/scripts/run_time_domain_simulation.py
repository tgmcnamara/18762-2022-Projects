import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)
import scipy as sp #tried importning scipy but said it was already installed

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    V_waveform = []#None #Should this be a matrix
    #waveform should contain voltages and currents at every node over set time
    #ie matrix where if plotted heach colum vector shows voltage or current waveform of that node

    #FIRST CONSTRUCT INITIAL Y AND J matrix
    ###Posssible idea (maybe this belongs in run time domain simulation)
    #THis constructs the overall y and J matrixes
    Y= np.zeros((size_Y,size_Y)) #creates the Y matrix of 0s Matrix seems incorrect several rows and columbs of 0
    J = np.zeros((size_Y,1))
    d_t = .01# detlat t time step
    for resistor in devices['resistors']:
        
        resistor.stamp_dense(Y, J)

    for capacitors in devices['capacitors']:
        capacitors.stamp_dense(Y, J, d_t)#not sure what things it need to take in

    for inductors in devices['inductors']:
        inductors.stamp_dense(Y,J, d_t)

    for voltage_sources in devices['voltage_sources']:
        voltage_sources.stamp_dense(Y,J)
######
    #print(Y)
    #print(J)

    #SECOND begin iterating over time
    #for look to iterate over time from
    #J = J*V_init #matrix mupliplication
    for t in np.arange(0,SETTINGS['Simulation Time'],d_t): #going over the entire time
        #J = Y*V_init #matrix mupliplication
        #for iter in range(SETTINGS.max_iters): #something feels off here
        if t == 0:
            v = np.linalg.solve(Y,J)
            print(type(v))
            V_waveform.append(v)
            #print(V_waveform)
            J = v
        else:
            v = np.linalg.solve(Y,J)
            V_waveform.append(v)
            #print(V_waveform)
            J = v
    #V_waveform = np.matrix(V_waveform)
    V_form = []
    for ind in range(size_Y):
        for arr in range(len(V_waveform)):
            V_form.append(V_waveform[arr][ind])
        print(V_form)
    return V_waveform
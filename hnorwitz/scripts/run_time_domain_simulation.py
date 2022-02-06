import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)
import scipy as sp #tried importning scipy but said it was already installed

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    V_waveform = []#None #Should this be a matrix
    #waveform should contain voltages and currents at every node over set time
    #ie matrix where if plotted heach colum vector shows voltage or current waveform of that node

    #FIRST CONSTRUCT INITIAL Y AND J matrix
    ###Posssible idea (maybe this belongs in run time domain simulation)
    #THis constructs the overall y and J matrixes
    Y= np.zeros((size_Y,size_Y)) #creates the Y matrix of 0s
    J = np.zeros((1,size_Y))
    for resistor in devices['resistors']:
        Y = Y + resistor.stamp_dense(size_Y)#call dense stamp fucntion create Y matrix with stamp and addes it to y
    
    for capacitors in devices['capacitors']:
        Y = Y + capacitors.stamp_dense(size_Y, SETTINGS.tol)#not sure what things it need to take in

    for inductors in devices['inductors']:
        Y = Y +  inductors.stamp_dense(size_Y, SETTINGS.tol)

    for voltage_sources in devices['voltage_sources']:
        Y = voltage_sources.stamp_dense(size_Y)
######
    print(Y)
    print(J)

    #SECOND begin iterating over time
    #for look to iterate over time from
    for t in range(0,SETTINGS.t_final, SETTINGS.tol): #going over the entire time
        J = J + Y*V_init #matrix mupliplication
        for iter in range(SETTINGS.max_iters): #something feels off here
            v = np.linalg.solve(Y,J)

        V_int = v
        V_waveform.append[V_int]

    return V_waveform
import numpy as np #think need to call np.linalg.solve(Y_mtx,J_mtx)

def run_time_domain_simulation(devices, V_init, size_Y, SETTINGS):
    V_waveform = None
    #waveform should contain voltages and currents at every node over set time
    #ie matrix where if plotted heach colum vector shows voltage or current waveform of that node

    #FIRST CONSTRUCT INITIAL Y AND J matrix


    #SECOND begin iterating over time
    #for look to iterate over time from
    for t in range(0,SETTINGS.t_final, SETTINGS.tol): #going over the entire time

        for iter in range(SETTINGS.max_iters):


    

    return V_waveform
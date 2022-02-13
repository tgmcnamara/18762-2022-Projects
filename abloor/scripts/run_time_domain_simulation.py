import numpy as np

def run_time_domain_simulation(devices, V_init, size_Y,  SETTINGS):
    V_waveform = None
    voltage_sources = devices['voltage_sources']
    resistors = devices['resistors']

    Y_matrix = np.zeros((size_Y,size_Y),dtype=np.float)
    J_time = np.zeros((1,size_Y),dtype=np.float)

    for res in resistors:
        res.stamp_dense(devices, Y_matrix)

    for vs in voltage_sources:
        vs.stamp_dense(devices, Y_matrix)

    #Things that will need to happen each loop/build loop around

    time = 0

    J_time = np.zeros((size_Y,1),dtype=np.float)

    for vs in voltage_sources:
        vs.stamp_J(J_time, time)

    print(J_time)

    V_init = np.linalg.solve(Y_matrix, J_time)

    print(V_init)


    return V_waveform

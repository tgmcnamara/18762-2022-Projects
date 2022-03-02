import numpy as np

def run_time_domain_simulation(devices, V_init, size_Y,  SETTINGS, step):
    voltage_sources = devices['voltage_sources']
    resistors = devices['resistors']
    inductors = devices['inductors']
    imotors = devices['induction_motors']
    t_final = SETTINGS['Simulation Time']
    iters = SETTINGS['Max Iters']


    V_waveform = np.zeros((int(t_final/step),size_Y), dtype = np.float)


    Y_matrix = np.zeros((size_Y,size_Y),dtype=np.float)
    J_time = np.zeros((1,size_Y),dtype=np.float)

    for res in resistors:
        res.stamp_dense(devices, Y_matrix)

    for vs in voltage_sources:
        vs.stamp_dense(devices, Y_matrix)

    for ind in inductors:
        ind.stamp_dense(devices, Y_matrix, step)

    for im in imotors:
        im.stamp_dq(devices, Y_matrix)

    #Things that will need to happen each loop/build loop around
    #print(V_waveform.shape)
    for time in np.linspace(0.0, t_final, V_waveform.shape[0]):

        J_time = np.zeros((size_Y,1),dtype=np.float)

        for vs in voltage_sources:
            vs.stamp_J(J_time, time)

        for ind in inductors:
            ind.stamp_time(devices, V_init, J_time, step)

        for im in imotors:
            im.stamp_time(devices, V_init, J_time, step)

        Y_iter = np.copy(Y_matrix)
        J_iter = np.copy(J_time)

        for k in range(0, iters):
            #NewtonRhapson Iterations for IMS
            Y_iter = np.copy(Y_matrix)
            J_iter = np.copy(J_time)
            for im in imotors:
                im.stamp_dense(devices, Y_iter, J_iter, V_init, step)
            V_init = np.linalg.solve(Y_iter, J_iter)

        V_init = np.linalg.solve(Y_iter, J_iter)

        if(int(time/step) < int(t_final/step)):
            V_waveform[int(time/step)][:] = np.transpose(V_init)

    #print(V_waveform)
    return V_waveform

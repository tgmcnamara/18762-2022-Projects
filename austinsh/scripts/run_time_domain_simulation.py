import numpy as np
# Initializing Y and J matrix in here and initialize stamps

def run_time_domain_simulation(devices, V_init, SETTINGS, Y_size):
    V_waveform = None
    # Initialize a matrix full of zeroes for matrix Y
    Y_matrix = np.zeros((Y_size, Y_size))
    return V_waveform
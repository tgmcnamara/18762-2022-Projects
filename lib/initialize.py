import numpy as np

from classes.Devices import Devices

def initialize(devices: Devices, Y_size):
    v_init = np.zeros(Y_size)

    #Through extremely rigorous DC analysis, we set all the nodes to an initial 0.1v
    #Assume things like state of charge for capacitors is 0.
    for i in range(Y_size):
        v_init[i] = 0.01

    return v_init
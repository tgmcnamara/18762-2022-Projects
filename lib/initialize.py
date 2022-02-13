import numpy as np

def initialize(devices, node_size, total_size):
    v_init = np.zeros(total_size)

    #Through extremely rigorous DC analysis, we set all the nodes to an initial 0.1v
    #Assume things like state of charge for capacitors is 0.
    for i in range(node_size):
        v_init[i] = 0.1

    return v_init
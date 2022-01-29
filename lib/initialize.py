import numpy as np

from classes.CircuitFrame import CircuitFrame

def initialize(devices, nodeLookup):
    v_init = np.zeros(len(nodeLookup))
    j_init = np.zeros(len(nodeLookup))

    return CircuitFrame(v=v_init, j=j_init, timestep=0)
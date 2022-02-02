import numpy as np
from scipy.sparse import csr_matrix
from classes.Devices import Devices

def stamp(devices: Devices, isSparse: bool):
    Ysize = len(nodeLookup)
    if (isSparse):
        J = csr_matrix((Ysize, Ysize))
    else:
        J = np.empty((Ysize, Ysize))

    
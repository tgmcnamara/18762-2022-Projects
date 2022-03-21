from typing import List
import numpy as np
from lib.settings import Settings
from models.Buses import Bus
from models.Generators import Generators


def initialize(Y_size, buses: List[Bus], generators: List[Generators], settings: Settings):
    Y = np.zeros(Y_size)

    if settings.v_init == None:
        for bus in buses:
            (vr_idx, vr_init) = bus.get_Vr_init()
            Y[vr_idx] = vr_init

            (vi_idx, vi_init) = bus.get_Vi_init()
            Y[vi_idx] = vi_init
    else:
        for idx in range(Y_size):
            Y[idx] = settings.v_init

    for generator in generators:
        Y[generator.bus.node_Q] = generator.Qinit

    return Y


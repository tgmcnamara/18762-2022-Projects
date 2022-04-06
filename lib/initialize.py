from typing import List
import numpy as np
from lib.settings import Settings
from models.Buses import Bus
from models.Generators import Generators
from models.Slack import Slack

V_R_FLAT_STARt = 1
V_I_FLAT_START = 0
Q_FLAT_START = 1

def initialize(Y_size, buses: List[Bus], generators: List[Generators], slacks: List[Slack], settings: Settings):
    Y = np.zeros(Y_size)

    for bus in buses:
        (vr_idx, vr_init) = bus.get_Vr_init()
        Y[vr_idx] = 1 if settings.flat_start else vr_init

        (vi_idx, vi_init) = bus.get_Vi_init()
        Y[vi_idx] = 0 if settings.flat_start else vi_init

    for generator in generators:
        Y[generator.bus.node_Q] = 1 if settings.flat_start else generator.Qinit / 100

    for slack in slacks:
        Y[slack.slack_Ir] = 0 if settings.flat_start else slack.Pinit / 100
        Y[slack.slack_Ii] = 0 if settings.flat_start else slack.Qinit / 100

    return Y


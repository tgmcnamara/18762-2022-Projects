from typing import List
import numpy as np
from lib.settings import Settings
from models.Buses import Bus
from models.Generators import Generators
from models.Slack import Slack

Vr_FLAT_START = 1
Vi_FLAT_START = 0
Q_FLAT_START = -1

def initialize(Y_size, buses: List[Bus], generators: List[Generators], slacks: List[Slack], settings: Settings):
    v_init = np.zeros(Y_size)

    for bus in buses:
        (vr_idx, vr_init) = bus.get_Vr_init()
        v_init[vr_idx] = Vr_FLAT_START if settings.flat_start else vr_init

        (vi_idx, vi_init) = bus.get_Vi_init()
        v_init[vi_idx] = Vi_FLAT_START if settings.flat_start else vi_init

    for generator in generators:
        v_init[generator.bus.node_Q] = Q_FLAT_START if settings.flat_start else generator.Qinit

    for slack in slacks:
        v_init[slack.slack_Ir] = 0 if settings.flat_start else slack.Pinit
        v_init[slack.slack_Ii] = 0 if settings.flat_start else slack.Qinit

    return v_init


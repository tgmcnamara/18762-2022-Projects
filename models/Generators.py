from __future__ import division
from itertools import count
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key

class Generators:
    _ids = count(0)
    RemoteBusGens = dict()
    RemoteBusRMPCT = dict()
    gen_bus_key_ = {}
    total_P = 0

    def __init__(self,
                 bus,
                 P,
                 Vset,
                 Qmax,
                 Qmin,
                 Pmax,
                 Pmin,
                 Qinit,
                 RemoteBus,
                 RMPCT,
                 gen_type):
        """Initialize an instance of a generator in the power grid.

        Args:
            Bus (int): the bus number where the generator is located.
            P (float): the current amount of active power the generator is providing.
            Vset (float): the voltage setpoint that the generator must remain fixed at.
            Qmax (float): maximum reactive power
            Qmin (float): minimum reactive power
            Pmax (float): maximum active power
            Pmin (float): minimum active power
            Qinit (float): the initial amount of reactive power that the generator is supplying or absorbing.
            RemoteBus (int): the remote bus that the generator is controlling
            RMPCT (float): the percent of total MVAR required to hand the voltage at the controlled bus
            gen_type (str): the type of generator
        """

        self.id = self._ids.__next__()

        self.bus = _all_bus_key[bus]
        self.P = P
        self.Vset = Vset

        self.Qinit = Qinit

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        Q_k = v_previous[self.bus.node_Q]
        VR_k = v_previous[self.bus.node_Vr]
        VI_k = v_previous[self.bus.node_Vi]

        IG_denominator = (VR_k ** 2 + VI_k ** 2)
        dIG_denominator = IG_denominator ** 2

        #Real current
        dIR_dQ_k = -VI_k / IG_denominator
        dIR_dVR_k = (self.P * (VR_k ** 2 - VI_k ** 2) + 2 * Q_k * VR_k * VI_k) / dIG_denominator
        dIR_dVI_k = (Q_k * (VI_k ** 2 - VR_k ** 2) + 2 * self.P * VR_k * VI_k) / dIG_denominator

        Y.stamp(self.bus.node_Vr, self.bus.node_Q, dIR_dQ_k)
        Y.stamp(self.bus.node_Vr, self.bus.node_Vr, dIR_dVR_k)
        Y.stamp(self.bus.node_Vr, self.bus.node_Vi, dIR_dVI_k)

        IR_k = (-self.P * VR_k - Q_k * VI_k) / IG_denominator

        J[self.bus.node_Vr] += -IR_k + dIR_dQ_k * Q_k + dIR_dVR_k * VR_k + dIR_dVI_k * VI_k

        #Imaginary current
        dII_dQ_k = VR_k / IG_denominator
        dII_dVR_k = (Q_k * (VI_k ** 2 - VR_k ** 2) + 2 * self.P * VR_k * VI_k) / dIG_denominator
        dII_dVI_k = (self.P * (VI_k ** 2 - VR_k ** 2) - 2 * Q_k * VR_k * VI_k) / dIG_denominator

        Y.stamp(self.bus.node_Vi, self.bus.node_Q, dII_dQ_k)
        Y.stamp(self.bus.node_Vi, self.bus.node_Vr, dII_dVR_k)
        Y.stamp(self.bus.node_Vi, self.bus.node_Vi, dII_dVI_k)

        II_k = (- self.P * VI_k + Q_k * VR_k) / IG_denominator

        J[self.bus.node_Vi] += -II_k + dII_dQ_k * Q_k + dII_dVR_k * VR_k + dII_dVI_k * VI_k

        #Vset equation
        Y.stamp(self.bus.node_Q, self.bus.node_Vr, 2 * VR_k)
        Y.stamp(self.bus.node_Q, self.bus.node_Vi, 2 * VI_k)
        J[self.bus.node_Q] += self.Vset ** 2



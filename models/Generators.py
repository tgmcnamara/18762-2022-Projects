from __future__ import division
from itertools import count
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key
from models.Loads import calculate_PQ_dIr_dVi, calculate_PQ_dIr_dVr

class Generators:
    _ids = count(0)

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
        self.P = -P / 100
        self.Vset = Vset

        self.Qinit = -Qinit / 100

        self.Qmax = Qmax
        self.Qmin = Qmin

    def stamp_nonlinear(self, Y: MatrixBuilder, J, v_previous):
        Q_k = v_previous[self.bus.node_Q]
        Vr_k = v_previous[self.bus.node_Vr]
        Vi_k = v_previous[self.bus.node_Vi]

        #Real current
        dIr_dQ_k = Vi_k / (Vr_k ** 2 + Vi_k ** 2)
        dIr_dVr_k = calculate_PQ_dIr_dVr(Vr_k, Vi_k, self.P, Q_k)
        dIr_dVi_k = calculate_PQ_dIr_dVi(Vr_k, Vi_k, self.P, Q_k)

        Y.stamp(self.bus.node_Vr, self.bus.node_Q, dIr_dQ_k)
        Y.stamp(self.bus.node_Vr, self.bus.node_Vr, dIr_dVr_k)
        Y.stamp(self.bus.node_Vr, self.bus.node_Vi, dIr_dVi_k)

        Ir_k = (self.P * Vr_k + Q_k * Vi_k) / (Vr_k ** 2 + Vi_k ** 2)

        J[self.bus.node_Vr] += -Ir_k + dIr_dQ_k * Q_k + dIr_dVr_k * Vr_k + dIr_dVi_k * Vi_k

        #Imaginary current
        dIi_dQ_k = -Vr_k / (Vr_k ** 2 + Vi_k ** 2)
        dIi_dVr_k = dIr_dVi_k
        dIi_dVi_k = -dIr_dVr_k

        Y.stamp(self.bus.node_Vi, self.bus.node_Q, dIi_dQ_k)
        Y.stamp(self.bus.node_Vi, self.bus.node_Vr, dIi_dVr_k)
        Y.stamp(self.bus.node_Vi, self.bus.node_Vi, dIi_dVi_k)

        Ii_k = (self.P * Vi_k - Q_k * Vr_k) / (Vr_k ** 2 + Vi_k ** 2)

        J[self.bus.node_Vi] += -Ii_k + dIi_dQ_k * Q_k + dIi_dVr_k * Vr_k + dIi_dVi_k * Vi_k

        #Vset equation
        dVset_dVr = -2 * Vr_k
        dVset_dVi = -2 * Vi_k

        Y.stamp(self.bus.node_Q, self.bus.node_Vr, dVset_dVr)
        Y.stamp(self.bus.node_Q, self.bus.node_Vi, dVset_dVi)

        VSet_k = self.Vset ** 2 - Vr_k ** 2 - Vi_k ** 2

        J[self.bus.node_Q] += -VSet_k + dVset_dVr * Vr_k + dVset_dVi * Vi_k

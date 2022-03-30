from __future__ import division
from itertools import count
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key

class Loads:
    _ids = count(0)

    def __init__(self,
                 bus,
                 P,
                 Q,
                 IP,
                 IQ,
                 ZP,
                 ZQ,
                 area,
                 status):
        """Initialize an instance of a PQ or ZIP load in the power grid.

        Args:
            Bus (int): the bus where the load is located
            P (float): the active power of a constant power (PQ) load.
            Q (float): the reactive power of a constant power (PQ) load.
            IP (float): the active power component of a constant current load.
            IQ (float): the reactive power component of a constant current load.
            ZP (float): the active power component of a constant admittance load.
            ZQ (float): the reactive power component of a constant admittance load.
            area (int): location where the load is assigned to.
            status (bool): indicates if the load is in-service or out-of-service.
        """
        self.id = Loads._ids.__next__()

        self.bus = _all_bus_key[bus]
        self.P = P / 100
        self.Q = Q / 100
    
    def stamp(self, Y: MatrixBuilder, J, v_previous):
        VR_k = v_previous[self.bus.node_Vr]
        VI_k = v_previous[self.bus.node_Vi]

        dI_denominator = (VR_k ** 2 + VI_k ** 2) ** 2

        # Real current
        dIR_dVR_k = (self.P * (VI_k ** 2 - VR_k ** 2) - 2 * self.Q * VR_k * VI_k) / dI_denominator
        dIR_dVI_k = (self.Q * (VR_k ** 2 - VI_k ** 2) - 2 * self.P * VR_k * VI_k) / dI_denominator

        Y.stamp(self.bus.node_Vr, self.bus.node_Vr, dIR_dVR_k)
        Y.stamp(self.bus.node_Vr, self.bus.node_Vi, dIR_dVI_k)

        IR_k = (self.P * VR_k + self.Q * VI_k) / (VR_k ** 2 + VI_k ** 2)

        J[self.bus.node_Vr] += -IR_k + dIR_dVR_k * VR_k + dIR_dVI_k * VI_k

        #Imaginary current
        dII_dVR_k = (self.P * (VI_k ** 2 - VR_k ** 2) + 2 * self.Q * VR_k * VI_k) / dI_denominator
        dII_dVI_k = (self.Q * (VI_k ** 2 - VR_k ** 2) - 2 * self.P * VR_k * VI_k) / dI_denominator

        II_k = (self.P * VI_k - self.Q * VR_k) / (VR_k ** 2 + VI_k ** 2)

        Y.stamp(self.bus.node_Vi, self.bus.node_Vr, dII_dVR_k)
        Y.stamp(self.bus.node_Vi, self.bus.node_Vi, dII_dVI_k)

        J[self.bus.node_Vi] += -II_k + dII_dVR_k * VR_k + dII_dVI_k * VI_k




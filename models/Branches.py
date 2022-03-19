from __future__ import division
from itertools import count

from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key


class Branches:
    _ids = count(0)

    def __init__(self,
                 from_bus,
                 to_bus,
                 r,
                 x,
                 b,
                 status,
                 rateA,
                 rateB,
                 rateC):
        """Initialize a branch in the power grid.

        Args:
            from_bus (int): the bus number at the sending end of the branch.
            to_bus (int): the bus number at the receiving end of the branch.
            r (float): the branch resistance
            x (float): the branch reactance
            b (float): the branch susceptance
            status (bool): indicates if the branch is online or offline
            rateA (float): The 1st rating of the line.
            rateB (float): The 2nd rating of the line
            rateC (float): The 3rd rating of the line.
        """
        self.id = self._ids.__next__()

        self.from_bus = _all_bus_key[from_bus]
        self.to_bus = _all_bus_key[to_bus]

        self.r = r
        self.x = x
        self.b = b

        self.R_factor = r / (x ** 2 + r ** 2)
        self.X_factor = x / (x ** 2 + r ** 2)

        self.b_half_shunt = b / 2

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        
        ###Series Current

        #Real series current - from bus
        Y.stamp(self.from_bus.node_Vr, self.from_bus.node_Vr, -self.R_factor)
        Y.stamp(self.from_bus.node_Vr, self.to_bus.node_Vr, self.R_factor)

        Y.stamp(self.from_bus.node_Vr, self.from_bus.node_Vi, -self.X_factor)
        Y.stamp(self.from_bus.node_Vr, self.to_bus.node_Vi, self.X_factor)

        #Real series current - to bus
        Y.stamp(self.to_bus.node_Vr, self.from_bus.node_Vr, self.R_factor)
        Y.stamp(self.to_bus.node_Vr, self.to_bus.node_Vr, -self.R_factor)

        Y.stamp(self.to_bus.node_Vr, self.from_bus.node_Vi, self.X_factor)
        Y.stamp(self.to_bus.node_Vr, self.to_bus.node_Vi, -self.X_factor)

        #Imaginary series current - from bus
        Y.stamp(self.from_bus.node_Vi, self.from_bus.node_Vr, -self.X_factor)
        Y.stamp(self.from_bus.node_Vi, self.to_bus.node_Vr, self.X_factor)

        Y.stamp(self.from_bus.node_Vi, self.from_bus.node_Vi, self.R_factor)
        Y.stamp(self.from_bus.node_Vi, self.to_bus.node_Vi, -self.R_factor)

        #Imaginary series current - to bus
        Y.stamp(self.to_bus.node_Vi, self.from_bus.node_Vr, self.X_factor)
        Y.stamp(self.to_bus.node_Vi, self.to_bus.node_Vr, -self.X_factor)

        Y.stamp(self.to_bus.node_Vi, self.from_bus.node_Vi, -self.R_factor)
        Y.stamp(self.to_bus.node_Vi, self.to_bus.node_Vi, self.R_factor)

        ###Shunt Current

        #Real/Imaginary shunt current - from bus
        Y.stamp(self.from_bus.node_Vr, self.from_bus.node_Vr, -self.b_half_shunt)
        Y.stamp(self.from_bus.node_Vi, self.from_bus.node_Vi, self.b_half_shunt)

        #Real/Imaginary shunt current - to bus
        Y.stamp(self.to_bus.node_Vr, self.to_bus.node_Vr, -self.b_half_shunt)
        Y.stamp(self.to_bus.node_Vi, self.to_bus.node_Vi, self.b_half_shunt)



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

        self.G = r / (x ** 2 + r ** 2)
        self.B = x / (x ** 2 + r ** 2)

        self.B_line = b / 2

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        
        ###Series Current
        #I_r = G * (Vrn - Vrm) + B * (Vin - Vim)
        #I_i = G * (Vin - Vim) - B * (Vrn - Vrm)
        
        Vrn = self.from_bus.node_Vr
        Vin = self.from_bus.node_Vi

        Vrm = self.to_bus.node_Vr
        Vim = self.to_bus.node_Vi

        #From Bus - Real
        Y.stamp(Vrn, Vrn, self.G)
        Y.stamp(Vrn, Vrm, -self.G)
        Y.stamp(Vrn, Vin, self.B)
        Y.stamp(Vrn, Vim, -self.B)

        #From Bus - Imaginary
        Y.stamp(Vin, Vin, self.G)
        Y.stamp(Vin, Vim, -self.G)
        Y.stamp(Vin, Vrn, -self.B)
        Y.stamp(Vin, Vrm, self.B)

        #To Bus - Real
        Y.stamp(Vrm, Vrn, -self.G)
        Y.stamp(Vrm, Vrm, self.G)
        Y.stamp(Vrm, Vin, -self.B)
        Y.stamp(Vrm, Vim, self.B)

        #To Bus - Imaginary
        Y.stamp(Vim, Vin, -self.G)
        Y.stamp(Vim, Vim, self.G)
        Y.stamp(Vim, Vrn, self.B)
        Y.stamp(Vim, Vrm, -self.B)

        ###Shunt Current

        #Real/Imaginary shunt current - from bus
        Y.stamp(Vrn, Vin, -self.B_line)
        Y.stamp(Vin, Vrn, self.B_line)

        #Real/Imaginary shunt current - to bus
        Y.stamp(Vrm, Vim, -self.B_line)
        Y.stamp(Vim, Vrm, self.B_line)



from __future__ import division
from itertools import count

from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key

TX_LARGE_G = 1000
TX_LARGE_B = 1000

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

    def stamp(self, Y: MatrixBuilder, J, v_previous, tx_factor):
        scaled_G = TX_LARGE_G * tx_factor + self.G * (1 - tx_factor)
        scaled_B = TX_LARGE_B * tx_factor + self.B * (1 - tx_factor)
        scaled_B_line = self.B_line * (1 - tx_factor)
        
        Vrn = self.from_bus.node_Vr
        Vin = self.from_bus.node_Vi

        Vrm = self.to_bus.node_Vr
        Vim = self.to_bus.node_Vi

        #From Bus - Real
        Y.stamp(Vrn, Vrn, scaled_G)
        Y.stamp(Vrn, Vrm, -scaled_G)
        Y.stamp(Vrn, Vin, scaled_B)
        Y.stamp(Vrn, Vim, -scaled_B)

        #From Bus - Imaginary
        Y.stamp(Vin, Vin, scaled_G)
        Y.stamp(Vin, Vim, -scaled_G)
        Y.stamp(Vin, Vrn, -scaled_B)
        Y.stamp(Vin, Vrm, scaled_B)

        #To Bus - Real
        Y.stamp(Vrm, Vrn, -scaled_G)
        Y.stamp(Vrm, Vrm, scaled_G)
        Y.stamp(Vrm, Vin, -scaled_B)
        Y.stamp(Vrm, Vim, scaled_B)

        #To Bus - Imaginary
        Y.stamp(Vim, Vin, -scaled_G)
        Y.stamp(Vim, Vim, scaled_G)
        Y.stamp(Vim, Vrn, scaled_B)
        Y.stamp(Vim, Vrm, -scaled_B)

        ###Shunt Current

        #From Bus - Real/Imaginary
        Y.stamp(Vrn, Vin, -scaled_B_line)
        Y.stamp(Vin, Vrn, scaled_B_line)

        #To Bus - Real/Imaginary
        Y.stamp(Vrm, Vim, -scaled_B_line)
        Y.stamp(Vim, Vrm, scaled_B_line)



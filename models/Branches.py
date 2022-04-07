from __future__ import division
from itertools import count

from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key
from models.shared import stamp_line

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
        scaled_G = TX_LARGE_G * self.G * tx_factor + self.G
        scaled_B = TX_LARGE_B * self.B * tx_factor + self.B
        scaled_B_line = self.B_line * (1 - tx_factor)
        
        Vr_from = self.from_bus.node_Vr
        Vi_from = self.from_bus.node_Vi

        Vr_to = self.to_bus.node_Vr
        Vi_to = self.to_bus.node_Vi

        stamp_line(Y, Vr_from, Vr_to, Vi_from, Vi_to, scaled_G, scaled_B)

        ###Shunt Current

        #From Bus - Real/Imaginary
        Y.stamp(Vr_from, Vi_from, -scaled_B_line)
        Y.stamp(Vi_from, Vr_from, scaled_B_line)

        #To Bus - Real/Imaginary
        Y.stamp(Vr_to, Vi_to, -scaled_B_line)
        Y.stamp(Vi_to, Vr_to, scaled_B_line)



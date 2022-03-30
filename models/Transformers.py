from __future__ import division
from itertools import count
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key, _node_index
import math


class Transformers:
    _ids = count(0)

    def __init__(self,
                 from_bus,
                 to_bus,
                 r,
                 x,
                 status,
                 tr,
                 ang,
                 Gsh_raw,
                 Bsh_raw,
                 rating):
        """Initialize a transformer instance

        Args:
            from_bus (int): the primary or sending end bus of the transformer.
            to_bus (int): the secondary or receiving end bus of the transformer
            r (float): the line resitance of the transformer in
            x (float): the line reactance of the transformer
            status (int): indicates if the transformer is active or not
            tr (float): transformer turns ratio
            ang (float): the phase shift angle of the transformer
            Gsh_raw (float): the shunt conductance of the transformer
            Bsh_raw (float): the shunt admittance of the transformer
            rating (float): the rating in MVA of the transformer
        """
        self.id = self._ids.__next__()

        self.from_bus = _all_bus_key[from_bus]
        self.to_bus = _all_bus_key[to_bus]

        self.r = r
        self.x = x

        self.tr = tr
        self.ang = ang * math.pi / 180.

        self.G_loss = r / (r ** 2 + x ** 2)
        self.B_loss = x / (r ** 2 + x ** 2)

    def assign_nodes(self):
        self.node_primary_Ir = _node_index.__next__()
        self.node_primary_Ii = _node_index.__next__()
        self.node_secondary_Vr = _node_index.__next__()
        self.node_secondary_Vi = _node_index.__next__()

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        
        ###Primary winding

        #Real
        Y.stamp(self.from_bus.node_Vr, self.node_primary_Ir, -1)
        Y.stamp(self.node_primary_Ir, self.from_bus.node_Vr, -1)
        Y.stamp(self.node_primary_Ir, self.node_secondary_Vr, -self.tr * math.cos(self.ang))
        Y.stamp(self.node_primary_Ir, self.node_secondary_Vi, self.tr * math.sin(self.ang))

        #Imaginary
        Y.stamp(self.from_bus.node_Vi, self.node_primary_Ii, -1)
        Y.stamp(self.node_primary_Ii, self.from_bus.node_Vi, -1)
        Y.stamp(self.node_primary_Ii, self.node_secondary_Vr, -self.tr * math.sin(self.ang))
        Y.stamp(self.node_primary_Ii, self.node_secondary_Vi, -self.tr * math.cos(self.ang))

        ###Secondary winding

        #Real
        Y.stamp(self.node_secondary_Vr, self.node_primary_Ir, -self.tr * math.cos(self.ang))
        Y.stamp(self.node_secondary_Vr, self.node_primary_Ii, -self.tr * math.sin(self.ang))

        #Imaginary
        Y.stamp(self.node_secondary_Vi, self.node_primary_Ir, self.tr * math.sin(self.ang))
        Y.stamp(self.node_secondary_Vi, self.node_primary_Ii, -self.tr * math.cos(self.ang))

        ###Secondary losses

        Vrn = self.node_secondary_Vr
        Vin = self.node_secondary_Vi
        Vrm = self.to_bus.node_Vr
        Vim = self.to_bus.node_Vi

        #From Bus - Real
        Y.stamp(Vrn, Vrn, self.G_loss)
        Y.stamp(Vrn, Vrm, -self.G_loss)
        Y.stamp(Vrn, Vin, self.B_loss)
        Y.stamp(Vrn, Vim, -self.B_loss)

        #From Bus - Imaginary
        Y.stamp(Vin, Vin, self.G_loss)
        Y.stamp(Vin, Vim, -self.G_loss)
        Y.stamp(Vin, Vrn, -self.B_loss)
        Y.stamp(Vin, Vrm, self.B_loss)

        #To Bus - Real
        Y.stamp(Vrm, Vrn, -self.G_loss)
        Y.stamp(Vrm, Vrm, self.G_loss)
        Y.stamp(Vrm, Vin, -self.B_loss)
        Y.stamp(Vrm, Vim, self.B_loss)

        #To Bus - Imaginary
        Y.stamp(Vim, Vin, -self.G_loss)
        Y.stamp(Vim, Vim, self.G_loss)
        Y.stamp(Vim, Vrn, self.B_loss)
        Y.stamp(Vim, Vrm, -self.B_loss)


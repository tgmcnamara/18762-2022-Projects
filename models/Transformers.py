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
        self.ang = ang

    def assign_nodes(self):
        self.node_Vr_primary_Xfmr = _node_index.__next__()
        self.node_Vi_primary_Xfmr = _node_index.__next__()

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        
        #Primary winding - Real
        Y.stamp(self.from_bus.node_Vr, self.node_Vr_primary_Xfmr, 1)
        Y.stamp(self.node_Vr_primary_Xfmr, self.from_bus.node_Vr, 1)
        Y.stamp(self.node_Vr_primary_Xfmr, self.to_bus.node_Vr, -self.tr * math.cos(self.ang))
        Y.stamp(self.node_Vr_primary_Xfmr, self.to_bus.node_Vi, self.tr * math.sin(self.ang))

        #Primary winding - Imaginary
        Y.stamp(self.from_bus.node_Vi, self.node_Vi_primary_Xfmr, 1)
        Y.stamp(self.node_Vi_primary_Xfmr, self.from_bus.node_Vr, 1)
        Y.stamp(self.node_Vi_primary_Xfmr, self.to_bus.node_Vr, -self.tr * math.sin(self.ang))
        Y.stamp(self.node_Vi_primary_Xfmr, self.to_bus.node_Vi, -self.tr * math.cos(self.ang))

        #Secondary winding - Real


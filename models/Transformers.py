from __future__ import division
from itertools import count
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import _all_bus_key


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

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        raise Exception("Not implemented")

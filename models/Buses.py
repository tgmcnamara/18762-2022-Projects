from __future__ import division
from itertools import count
import math

_idsAllBuses = count(1)
_node_index = count(0)
_all_bus_key = {}

class Bus:
    def __init__(self,
                 Bus,
                 Type,
                 Vm_init,
                 Va_init,
                 Area):
        """Initialize an instance of the Buses class.

        Args:
            Bus (int): The bus number.
            Type (int): The type of bus (e.g., PV, PQ, of Slack)
            Vm_init (float): The initial voltage magnitude at the bus.
            Va_init (float): The initial voltage angle at the bus.
            Area (int): The zone that the bus is in.
        """

        self.Bus = Bus
        self.Type = Type

        # initialize all nodes
        self.node_Vr = None  # real voltage node at a bus
        self.node_Vi = None  # imaginary voltage node at a bus
        self.node_Q = None  # reactive power or voltage contstraint node at a bus

        self.Vr_init = Vm_init * math.cos(Va_init)
        self.Vi_init = Vm_init * math.sin(Va_init)

        # initialize the bus key
        self.idAllBuses = _idsAllBuses.__next__()
        _all_bus_key[self.Bus] = self

    def __str__(self):
        return_string = 'The bus number is : {} with Vr node as: {} and Vi node as {} '.format(self.Bus,
                                                                                               self.node_Vr,
                                                                                               self.node_Vi)
        return return_string

    def get_Vr_init(self):
        return (self.node_Vr, self.Vr_init)

    def get_Vi_init(self):
        return (self.node_Vi, self.Vi_init)

    def assign_nodes(self):
        """Assign nodes based on the bus type.

        Returns:
            None
        """
        # If Slack or PQ Bus
        if self.Type == 1 or self.Type == 3:
            self.node_Vr = _node_index.__next__()
            self.node_Vi = _node_index.__next__()

        # If PV Bus
        elif self.Type == 2:
            self.node_Vr = _node_index.__next__()
            self.node_Vi = _node_index.__next__()
            self.node_Q = _node_index.__next__()

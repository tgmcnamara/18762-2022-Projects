from __future__ import division
from lib.MatrixBuilder import MatrixBuilder
from models.Buses import Bus
import math

class Slack:

    def __init__(self,
                 bus: Bus,
                 Vset,
                 ang,
                 Pinit,
                 Qinit):
        """Initialize slack bus in the power grid.

        Args:
            Bus (int): the bus number corresponding to the slack bus.
            Vset (float): the voltage setpoint that the slack bus must remain fixed at.
            ang (float): the slack bus voltage angle that it remains fixed at.
            Pinit (float): the initial active power that the slack bus is supplying
            Qinit (float): the initial reactive power that the slack bus is supplying
        """

        self.bus = bus
        self.Vset = Vset
        self.ang = ang

    def assign_nodes(self):
        self.node_Vr_Slack = Bus._node_index.__next__()
        self.node_Vi_Slack = Bus._node_index.__next__()

    def stamp(self, Y: MatrixBuilder, J, v_previous):
        Vr_angle = self.Vset * math.cos(self.ang)

        Y.stamp(self.node_Vr_Slack, self.bus.node_Vr, 1)
        J[self.node_Vr_Slack] = Vr_angle

        Vi_angle = self.Vset * math.sin(self.ang)

        Y.stamp(self.node_Vi_Slack, self.bus.node_Vi, 1)
        J[self.node_Vi_Slack] = Vi_angle


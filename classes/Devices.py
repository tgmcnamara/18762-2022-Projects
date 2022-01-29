from Nodes import Nodes
from Resistors import Resistors
from Capacitors import Capacitors
from Inductors import Inductors
from Switches import Switches
from VoltageSources import VoltageSources
from InductionMotors import InductionMotors

class Devices:
    def __init__(self):
        self.nodes = [Nodes]
        self.resistors = [Resistors]
        self.capacitors = [Capacitors]
        self.inductors = [Inductors]
        self.switches = [Switches]
        self.voltage_sources = [VoltageSources]
        self.induction_motors = [InductionMotors]
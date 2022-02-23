from classes.CurrentSources import CurrentSources
from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.Capacitors import Capacitors
from classes.Inductors import Inductors
from classes.Switches import Switches
from classes.VoltageSources import VoltageSources
from classes.InductionMotors import InductionMotors

class Devices:
    def __init__(self, devices=[]):

        self.nodes = [x for x in devices if isinstance(x, Nodes)]
        self.resistors = [x for x in devices if isinstance(x, Resistors)]
        self.capacitors = [x for x in devices if isinstance(x, Capacitors)]
        self.inductors = [x for x in devices if isinstance(x, Inductors)]
        self.switches = [x for x in devices if isinstance(x, Switches)]
        self.voltage_sources = [x for x in devices if isinstance(x, VoltageSources)]
        self.induction_motors = [x for x in devices if isinstance(x, InductionMotors)]
        self.current_sources = [x for x in devices if isinstance(x, CurrentSources)]

    def all_devices_but_nodes(self):
        return [] \
            + self.resistors \
            + self.capacitors \
            + self.inductors \
            + self.switches \
            + self.voltage_sources \
            + self.induction_motors \
            + self.current_sources

    def all_NR_invariant_devices(self):
        return [] \
            + self.resistors \
            + self.capacitors \
            + self.inductors \
            + self.switches \
            + self.voltage_sources \
            + self.induction_motors \
            + self.current_sources
    
    def all_NR_dependent_devices(self):
        return self.induction_motors
        
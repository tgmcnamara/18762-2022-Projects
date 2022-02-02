from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.Capacitors import Capacitors
from classes.Inductors import Inductors
from classes.Switches import Switches
from classes.VoltageSources import VoltageSources
from classes.InductionMotors import InductionMotors

class Devices:
    def __init__(self):
        self.nodes = []
        self.resistors = []
        self.capacitors = []
        self.inductors = []
        self.switches = []
        self.voltage_sources = []
        self.induction_motors = []
        self.current_sources = []

    def all_devices_but_nodes(self):
        return [] \
            + self.resistors \
            + self.capacitors \
            + self.inductors \
            + self.switches \
            + self.voltage_sources \
            + self.induction_motors \
            + self.current_sources
        
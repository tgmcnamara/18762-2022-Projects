import unittest
from classes.CurrentSource import CurrentSources
from classes.Devices import Devices
from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.VoltageSources import VoltageSources
from scripts.solve import solve

class CircuitSimulatorTests(unittest.TestCase):
    def test_resistor(self):
        devices = Devices()
        devices.nodes = [
            Nodes("gnd", "A"),
            Nodes("a", "A"),
            Nodes("b", "A")
        ]
        devices.current_sources = [
            CurrentSources("cs-gnd-a", "gnd", "a", 5)
        ]
        devices.resistors = [
            Resistors("r-a-b", "a", "b", 5),
            Resistors("r-a-b", "b", "gnd", 4)
        ]

        results = solve(devices)

        a_waveform = results.get_node_voltage("a")
        self.assertEqual(a_waveform[-1], 45)

        a_waveform = results.get_node_voltage("b")
        self.assertEqual(a_waveform[-1], 20)

    def test_voltage_source(self):
        devices = Devices()
        devices.nodes = [
            Nodes("gnd", "A"),
            Nodes("a", "A"),
            Nodes("b", "A")
        ]
        devices.voltage_sources = [
            VoltageSources("v-gnd-a", "a", "gnd", 120, 0, 60)
        ]
        devices.resistors = [
            Resistors("r-a-b", "a", "b", 5),
            Resistors("r-a-b", "b", "gnd", 4)
        ]

        results = solve(devices)

if __name__ == '__main__':
    unittest.main()
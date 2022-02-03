import unittest
from classes.CurrentSource import CurrentSources
from classes.Devices import Devices
from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.Settings import Settings
from classes.VoltageSources import CurrentSensor, VoltageSources
from scripts.solve import solve

class CircuitSimulatorTests(unittest.TestCase):
    def test_resistor(self):
        devices = Devices([
            Nodes("gnd", "A"),
            Nodes("a", "A"),
            Nodes("b", "A"),
            CurrentSources("cs-gnd-a", "gnd", "a", 5),
            Resistors("r-a-b", "a", "b", 5),
            Resistors("r-a-b", "b", "gnd", 4)
        ])

        results = solve(devices)

        a_waveform = results.get_node_voltage("a")
        self.assertEqual(a_waveform[-1], 45)

        a_waveform = results.get_node_voltage("b")
        self.assertEqual(a_waveform[-1], 20)

    def test_voltage_source(self):
        devices = Devices([
            Nodes("gnd", "A"),
            Nodes("a", "A"),
            Nodes("b", "A"),
            VoltageSources("v-gnd-a", "a", "gnd", 120, 0, 60),
            Resistors("r-a-b", "a", "b", 5),
            Resistors("r-a-b", "b", "gnd", 4)
        ])

        results = solve(devices)

        v_waveform_a = results.get_node_voltage("a")
        v_waveform_b = results.get_node_voltage("b")

        self.assertAlmostEqual(169, max(v_waveform_a), delta=1)
        self.assertAlmostEqual(75, max(v_waveform_b), delta=1)




if __name__ == '__main__':
    unittest.main()
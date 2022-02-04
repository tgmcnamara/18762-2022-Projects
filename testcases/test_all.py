import unittest
from classes.CurrentSources import CurrentSources
from classes.Devices import Devices
from classes.Inductors import Inductors
from classes.Nodes import Nodes
from classes.Resistors import Resistors
from classes.Settings import Settings
from classes.VoltageSources import CurrentSensors, VoltageSources
from scripts.solve import solve

class CircuitSimulatorTests(unittest.TestCase):
    def test_resistor(self):
        devices = Devices([
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
            VoltageSources("v-gnd-a", "a", "gnd", 120, 0, 60),
            Resistors("r-a-b", "a", "b", 5),
            Resistors("r-a-b", "b", "gnd", 4)
        ])

        results = solve(devices)

        v_waveform_a = results.get_node_voltage("a")
        v_waveform_b = results.get_node_voltage("b")

        self.assertAlmostEqual(169, max(v_waveform_a), delta=1)
        self.assertAlmostEqual(75, max(v_waveform_b), delta=1)

    def test_inductor(self):
        devices = Devices([
            VoltageSources("vs-gnd-a", "a", "gnd", 120, 0, 15),
            Resistors("r-1", "a", "b", 5),
            Inductors("i-1", "b", "c", 0.1),
            Resistors("r-2", "c", "gnd", 5)
        ])

        results = solve(devices, Settings(simulationTime=0.1))

        v_waveform_b = results.get_node_voltage("b")
        v_waveform_c = results.get_node_voltage("c")

        self.assertAlmostEqual(115, max(v_waveform_b), delta=1)
        self.assertAlmostEqual(61, max(v_waveform_c), delta=1)


if __name__ == '__main__':
    unittest.main()
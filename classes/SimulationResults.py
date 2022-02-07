from typing import List
import numpy as np
from classes.Devices import Devices
from classes.Settings import Settings

class SimulationResults:
    def __init__(self, node_voltage_dict, v_waveform, devices: Devices, settings: Settings):
        self.node_voltage_dict = node_voltage_dict
        self.v_waveform = v_waveform
        self.devices = devices
        self.settings = settings
    
    def get_timesteps(self):
        count = len(self.v_waveform)

        timesteps = range(count)

        def translate_timestep(x):
            return x * self.settings.timestep
        
        return list(map(translate_timestep, timesteps))

    def get_node_voltage(self, node_name):
        if node_name == "gnd":
            return [0] * len(self.v_waveform)
        return self.node_voltage_dict[node_name]

    def get_voltage_drop(self, from_node, to_node):
        from_v = self.get_node_voltage(from_node)
        to_v = self.get_node_voltage(to_node)

        return [(x[0] - x[1]) for x in zip(from_v, to_v)]

    def get_voltage_source_current(self, vs_name):
        voltagesource = next(vs for vs in self.devices.voltage_sources if vs.name == vs_name)

        current_waveform = []
        for v in self.v_waveform:
            current_waveform.append(v[voltagesource.current_index])
        
        return current_waveform
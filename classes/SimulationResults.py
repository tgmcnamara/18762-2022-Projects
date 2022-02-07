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
        return np.arange(0, len(self.v_waveform) * self.settings.timestep, self.settings.timestep)

    def get_node_voltage(self, node_name):
        return self.node_voltage_dict[node_name]

    def get_voltage_source_current(self, vs_name):
        voltagesource = next(vs for vs in self.devices.voltage_sources if vs.name == vs_name)

        current_waveform = []
        for v in self.v_waveform:
            current_waveform.append(v[voltagesource.current_index])
        
        return current_waveform
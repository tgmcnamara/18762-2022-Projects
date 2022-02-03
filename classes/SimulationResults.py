from typing import List

from classes.Devices import Devices

class SimulationResults:
    def __init__(self, node_voltage_dict, v_waveform, devices: Devices):
        self.node_voltage_dict = node_voltage_dict
        self.v_waveform = v_waveform
        self.devices = devices
    
    def get_node_voltage(self, node_name):
        return self.node_voltage_dict[node_name]

    def get_voltage_source_current(self, vs_name):
        voltagesource = next(vs for vs in self.devices.voltage_sources if vs.name == vs_name)

        current_waveform = []
        for v in self.v_waveform:
            current_waveform.append(v[voltagesource.current_index])
        
        return current_waveform
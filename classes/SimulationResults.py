from typing import List
import numpy as np
from classes.Devices import Devices
from classes.InductionMotors import InductionMotors
from classes.Inductors import Inductors
from classes.Resistors import Resistors
from classes.Settings import Settings

class SimulationResults:
    def __init__(self, node_voltage_dict, v_waveform, J_waveform, devices: Devices, settings: Settings):
        self.node_voltage_dict = node_voltage_dict
        self.v_waveform = v_waveform
        self.J_waveform = J_waveform
        self.devices = devices
        self.settings = settings
        self.count = len(self.v_waveform)
    
    def get_timesteps(self):
        timesteps = range(self.count)

        def translate_timestep(x):
            return x * self.settings.timestep
        
        return list(map(translate_timestep, timesteps))

    def get_node_voltage(self, node_name):
        if node_name == "gnd":
            return [0] * self.count
        return self.node_voltage_dict[node_name]

    def get_voltage_drop(self, from_node, to_node):
        from_v = self.get_node_voltage(from_node)
        to_v = self.get_node_voltage(to_node)

        return [(x[0] - x[1]) for x in zip(from_v, to_v)]

    def get_current_flow(self, from_node, to_node):
        #assumes one or more elements are in parallel in between the two nodes.
        parallel_devices = []
        for device in self.devices.all_devices_but_nodes():
            if not isinstance(device, Resistors) and not isinstance(device, Inductors):
                continue
            elif device.from_node == from_node and device.to_node == to_node:
                parallel_devices.append(device)

        current_waveform = []

        for (v, J) in zip(self.v_waveform, self.J_waveform):
            current = 0
            for device in parallel_devices:
                current += device.calculate_current(v, J, self.settings.timestep)
            current_waveform.append(current)

        return current_waveform
    
    def get_IM_waveforms(self, im_name):
        for device in self.devices.all_devices_but_nodes():
            if isinstance(device, InductionMotors) and device.name == im_name:
                return device.get_IM_waveforms(self.v_waveform)

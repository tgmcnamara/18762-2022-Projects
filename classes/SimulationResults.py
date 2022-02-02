from typing import List

class SimulationResults:
    def __init__(self, node_voltage_dict):
        self.node_voltage_dict = node_voltage_dict
    
    def get_node_voltage(self, node_name):
        return self.node_voltage_dict[node_name]
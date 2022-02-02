
from classes.Devices import Devices
from classes.SimulationResults import SimulationResults


def process_results(v_waveform, devices: Devices):
    node_voltage_dict = {}

    for node in devices.nodes:
        if node.name != "gnd":
            node_voltage_dict[node.index] = []

    for v in v_waveform:
        for i in range(len(v)):
            if i != 0:
                node_voltage_dict[i].append(v[i])

    for node in devices.nodes:
        if node.name != "gnd":
            node_voltage_dict[node.name] = node_voltage_dict[node.index]
            del node_voltage_dict[node.index]

    return SimulationResults(node_voltage_dict)
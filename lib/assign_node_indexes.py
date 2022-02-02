
from classes.Devices import Devices
from classes.Nodes import Nodes

def assign_node_indexes(devices: Devices):
    nodeLookup = {}
    count = 1
    
    for node in devices.nodes:
        if node.name == "gnd":
            nodeLookup[node.name] = 0
            node.assign_index(0)
        else:
            nodeLookup[node.name] = count
            node.assign_index(count)
            count += 1

    for device in devices.all_devices_but_nodes():
        device.assign_node_indexes(nodeLookup)

    return len(nodeLookup)
    
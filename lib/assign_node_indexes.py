
from classes.Capacitors import Capacitors
from classes.Devices import Devices
from classes.Inductors import Inductors
from classes.Nodes import Nodes
from classes.VoltageSources import CurrentSensors, VoltageSources

def assign_node_indexes(devices: Devices):
    if len(devices.nodes) == 0:
        devices.nodes = autogenerate_nodes(devices)

    enforce_element_isolation(devices)

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

#For when I'm lazy and don't want to specify node names.
def autogenerate_nodes(devices: Devices):
    nodes = {}
    for device in devices.all_devices_but_nodes():
        for nodeName in device.get_nodes_connections():
            nodes[nodeName] = 0
    
    def mapNode(nodeName):
        return Nodes(nodeName)

    return list(map(mapNode, nodes.keys()))

#Inductors and capacitors need their own space on the J vector to track their current.
#We create an extra node specifically for these elments, which gives them the 
#state space they need. This method assumes that these elements use their 'to' node for this.
def enforce_element_isolation(devices: Devices):
    for device in devices.all_devices_but_nodes():
        if not isinstance(device, Inductors) and not isinstance(device, Capacitors):
            continue

        original_node = device.to_node
        new_node_name = device.name + "-extension-" + original_node

        new_node = Nodes(new_node_name)
        device.to_node = new_node_name

        #current sensors implicitly act as a short between nodes.
        node_branch = CurrentSensors(device.name + "-extension", original_node, new_node_name)

        devices.voltage_sources.append(node_branch)

        devices.nodes.append(new_node)
        
        
    
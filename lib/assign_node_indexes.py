
from classes.Devices import Devices
from classes.Nodes import Nodes

def assign_node_indexes(devices: Devices):
    if len(devices.nodes) == 0:
        devices.nodes = autogenerate_nodes(devices)

    node_size = len(devices.nodes)

    print(f'Circuit has {node_size} nodes')

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

    Y_size = len(nodeLookup)

    print(f'Total Y matrix size for circuit will be {Y_size}')

    return Y_size

#For when I'm lazy and don't want to specify node names.
def autogenerate_nodes(devices: Devices):
    print("Autogenerating nodes...")

    nodeDict = {}
    for device in devices.all_devices_but_nodes():
        for nodeName in device.get_nodes_connections():
            nodeDict[nodeName] = 0
    
    def create_node(nodeName):
        return Nodes(nodeName)

    return list(map(create_node, nodeDict.keys()))
        
        
    
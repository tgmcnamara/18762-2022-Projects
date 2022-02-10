
from classes.Nodes import Nodes #Not needed 


def assign_node_indexes(devices): #not sure how to use his or where this is being called
    for node in devices['nodes']:
        node.assign_node_indexes() #need to make these functions in classes

    for resistor in devices['resistors']:
        resistor.assign_node_indexes()#is the node index counter all it really needs

    for capacitors in devices['capacitors']:
        capacitors.assign_node_indexes()

    for inductors in devices['inductors']:
        inductors.assign_node_indexes()

    for voltage_sources in devices['voltage_sources']:
        voltage_sources.assign_node_indexes()

    size_Y = int(Nodes.index_counter)
    return size_Y
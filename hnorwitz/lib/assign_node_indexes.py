
from classes.Nodes import Nodes #Not needed 


def assign_node_indexes(devices): #not sure how to use his or where this is being called
    node_index_counter = 0
    for node in devices['nodes']:
        index_counter = node.assign_node_indexes(node_index_counter) #need to make these functions in classes

    for resistor in devices['resistors']:
        index_counter = resistor.assign_node_indexes(node_index_counter)#is the node index counter all it really needs

    for capacitors in devices['capacitors']:
        index_counter = capacitors.assign_node_indexes(node_index_counter)

    for inductors in devices['inductors']:
        index_counter = inductors.assign_node_indexes(node_index_counter)

    for voltage_sources in devices['voltage_sources']:
        index_counter = voltage_sources.assign_node_indexes(node_index_counter)

    
    return node_index_counter

from classes.Nodes import Nodes #Not needed 

#####PARSEING THROUGH EACH OBJECT AND ASSIGNING NODE INDEX
def assign_node_indexes(devices): 
    for node in devices['nodes']:
        node.assign_node_indexes() 

    for resistor in devices['resistors']:
        resistor.assign_node_indexes()

    for capacitors in devices['capacitors']:
        capacitors.assign_node_indexes()

    for inductors in devices['inductors']:
        inductors.assign_node_indexes()

    for voltage_sources in devices['voltage_sources']:
        voltage_sources.assign_node_indexes()

    for InductionMotors in devices['induction_motors']:
        InductionMotors.assign_node_indexes()

    size_Y = int(Nodes.index_counter)
    return size_Y
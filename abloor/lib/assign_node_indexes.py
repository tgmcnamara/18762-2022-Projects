
def assign_node_indexes(devices):
    node_index_counter = 0
    nodes = devices['nodes']
    voltage_sources = devices['voltage_sources']
    resistors = devices['resistors']

    for node in nodes:
        node_index_counter += node.assign_node_indexes(node_index_counter);

    for voltage_source in voltage_sources:
        node_index_counter += voltage_source.assign_node_indexes(node_index_counter);

    print(node_index_counter)
    print(nodes[2].index)
    print(voltage_sources[0].index)

    return node_index_counter

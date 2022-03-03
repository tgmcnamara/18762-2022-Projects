
def assign_node_indexes(devices):
    node_index_counter = 0
    nodes = devices['nodes']
    voltage_sources = devices['voltage_sources']
    resistors = devices['resistors']
    inductors = devices['inductors']
    imotors = devices['induction_motors']

    #allocates appropriate number of indexes/new eqs/new variables for
    #each component and adds to index counter which gives the first
    #index to each component

    for node in nodes:
        node_index_counter += node.assign_node_indexes(node_index_counter)

    for voltage_source in voltage_sources:
        node_index_counter += voltage_source.assign_node_indexes(node_index_counter)

    for ind in inductors:
        node_index_counter += ind.assign_node_indexes(node_index_counter)

    for im in imotors:
        node_index_counter += im.assign_node_indexes(node_index_counter)

    return node_index_counter

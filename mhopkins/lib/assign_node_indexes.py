
def assign_node_indexes(devices):
    node_index_counter = 0
    node_label_list = []
    node_mapping = {}
    
    # TODO
    for i in devices['nodes']:
        node_mapping[devices['nodes'][node_index_counter].name] = node_index_counter
        node_index_counter += 1
    
    return node_mapping, node_index_counter

from classes.Nodes import Nodes

def assign_node_indexes(nodes: Nodes):
    nodeLookup = {}

    count = 0
    for node in nodes:
        nodeLookup[node.name] = count
        count += 1

    return nodeLookup
    
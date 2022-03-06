import sys
sys.path.append("..")
import numpy as np

node_index_counter = 1
node_index_dict = dict()

class Nodes:
    def __init__(self, name, phase):
        self.name = name
        self.phase = phase
        global node_index_counter
        if self.name == 'gnd':
            # Ground will always been row/column zero
            node_index_dict[self.name] = 0
        else:
            # Assigning nodes an index number based on the order of their appearance in
            # the .json file
            node_index_dict[self.name] = node_index_counter
            node_index_counter += 1
    
    def assign_node_indexes(self,):
        pass
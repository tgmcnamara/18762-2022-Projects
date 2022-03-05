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
            node_index_dict[self.name] = 0
        else:
            node_index_dict[self.name] = node_index_counter
            node_index_counter += 1
    
    def assign_node_indexes(self,):
        pass
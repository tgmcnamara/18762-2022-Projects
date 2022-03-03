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
        # You are welcome to / may be required to add additional class variables
    
    # Some suggested functions to implement,
    def assign_node_indexes(self,):
        pass

# node_1 = Nodes("1a", "b")
# node_2 = Nodes("2a", "b")
# node_3 = Nodes("3a", "b")
# node_4 = Nodes("4a", "b")
# node_5 = Nodes("gnd", "c")

# print()
# print(node_index_dict["4a"])
# print()

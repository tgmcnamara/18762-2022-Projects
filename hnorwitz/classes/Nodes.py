import sys
sys.path.append("..")
import numpy as np
from itertools import count

class Nodes(object):    
    index_counter = 0
    node_index_dict = dict()

    def __init__(self, name, phase):
        self.name = name
        self.phase = phase
          

    # Some suggested functions to implement, 
    def assign_node_indexes(self,): #calls function assign_node_indexes
        self.node_index_dict[self.name] = Nodes.index_counter
        Nodes.index_counter += 1
        print(self.node_index_dict)

        #####HOW ORIGANALLY WAS NOT INDEXING GROUND NODE
        #if self.name != 'gnd':
        #    self.node_index_dict[self.name] = Nodes.index_counter
        #    Nodes.index_counter += 1
        #    print(self.node_index_dict)
        #else:
        #    pass
              

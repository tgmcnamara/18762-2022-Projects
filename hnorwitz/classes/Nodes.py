import sys
sys.path.append("..")
import numpy as np
from itertools import count
#First: does it matter if it is nodes or Nodes?
#do i need to import ass_node_indexes.py from lib
class Nodes:    
    
    def __init__(self, name, phase):
        self.name = name
        self.phase = phase
        self.index = 0 #unassigned index
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self, val): #calls function assign_node_indexes
        self.index =  val
        val += 1 #will this make me index [0,1,2] or [1,2,3] ie do I add 1 before or after I set index to val
        return val       

import sys
sys.path.append("..")
import numpy as np
from itertools import count

class Nodes:    
	# These variables are global to the Node objects
	index_counter = 0
	node_index_dict = dict()
	def __init__(self, name, phase):
		self.name = name
		self.phase = phase

	def assign_node_indexes(self,):
		if self.name == "gnd":
			self.node_index_dict[self.name] = 0
		else:
			# The nodes assign themselves indexes as they are instantiated
			self.node_index_dict[self.name] = Nodes.index_counter + 1
			Nodes.index_counter += 1

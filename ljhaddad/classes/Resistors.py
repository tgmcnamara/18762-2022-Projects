
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse


class Resistors:
	def __init__(self, name, from_node, to_node, r):
		self.name = name
		self.from_node = from_node
		self.to_node = to_node
		self.r = r
		# You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
	def assign_node_indexes(self,):
		self.f_index = Nodes.node_index_dict[self.from_node]
		self.t_index = Nodes.node_index_dict[self.to_node]
    
	def stamp_sparse(self,):
		pass

	def stamp_dense(self,Y):
		f = self.f_index - 1
		t = self.t_index - 1
		r = self.r
		# Stamp diagonal
		if self.f_index != 0:
			Y[f, f] += 1/r
			if self.t_index != 0:
				Y[f, t] += -1/r
				Y[t, f] += -1/r
				Y[t, t] += 1/r
		else:
			if self.t_index != 0:
				Y[t, t] += 1/r
				



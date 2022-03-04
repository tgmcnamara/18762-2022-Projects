import sys
sys.path.append("..")
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Inductors:
	def __init__(self, name, from_node, to_node, l):
		self.name = name
		# Below holds intermediate and dummy node for series ammeter
		self.v_node = name + "_v"
		self.i_node = name + "_i"
		# "from" node connected to positive of voltage source
		self.from_node = from_node
		self.to_node = to_node
		self.l = l  

	def assign_node_indexes(self):
		# v_node at negative of ammeter
		Nodes.node_index_dict[self.v_node] = Nodes.index_counter + 1
		# i_node serves as dummy for current measurement
		Nodes.node_index_dict[self.i_node] = Nodes.index_counter + 2
		
		# indexes assigned here, in order from top to bottom
		self.f_index = Nodes.node_index_dict[self.from_node]
		self.v_index = Nodes.index_counter + 1
		self.t_index = Nodes.node_index_dict[self.to_node]
		self.i_index = Nodes.index_counter + 2
		# Increment index counter
		Nodes.index_counter += 2

	
	def set_current_index(self, i):
		self.temp_i_index = i

	def set_initial_state(self, v):
		self.last_V = 0
		self.last_I = v[self.temp_i_index, 0]
	
	def set_current_state(self, v, J):
		# Index into state and solution vector
		# to update last_I and last_V
		f = self.v_index - 1
		t = self.t_index - 1
		i = self.i_index - 1
		self.last_I = v[i, 0]
		if self.v_index != 0:
			if self.t_index != 0:
				self.last_V = v[f, 0] - v[t, 0]
			else:
				self.last_V = v[f, 0]
		else:
			self.last_V = -v[t, 0]


	def stamp_sparse(self,):
		pass

	def stamp_dense(self, Y, J):
		# Calculate current source value
		g = 0.001 / (2 * self.l)
		i = self.last_I + g*self.last_V
		# Stamp the inductor
		f = self.v_index - 1
		t = self.t_index - 1
		Y[f, f] += g
		J[f, 0] += -i
		if self.t_index != 0:
			Y[f, t] += -g
			Y[t, f] += -g
			Y[t, t] += g
			J[t, 0] += i

		# Stamp the voltage source
		v = self.f_index - 1
		dummy = self.i_index - 1

		# Conditionals for stamping Y and J
		if v != -1:
			Y[v, dummy] += 1
			Y[dummy, v] += 1
		if f != -1:
			Y[f, dummy] += -1
			Y[dummy, f] += -1
		J[dummy, 0] += 0

	# Stamp a 0V source across the terminals
	def stamp_short(self, Y, J):
		v = self.f_index - 1
		f = self.v_index - 1
		t = self.t_index - 1
		i = self.i_index - 1
		it = self.temp_i_index
		# Conditionals for stamping normal shorted VS
		if v != -1:
			Y[v, i] += 1
			Y[i, v] += 1
		if f != -1:
			Y[f, i] += -1
			Y[i, f] += -1
		J[i, 0] += 0

		# Conditionals for stamping shorted inductor
		if f != -1:
			Y[f, it] += 1
			Y[it, f] += 1
		if t != -1:
			Y[t, it] += -1
			Y[it, t] += -1
		J[it, 0] += 0

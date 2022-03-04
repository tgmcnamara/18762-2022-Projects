import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class VoltageSources:
	def __init__(self, name, vp_node, vn_node, amp_ph_ph_rms, phase_deg, frequency_hz):
		self.name = name
		self.vp_node = vp_node
		self.vn_node = vn_node
		self.amp_ph_ph_rms = amp_ph_ph_rms
		self.phase_deg = phase_deg
		self.frequency_hz = frequency_hz
		# You are welcome to / may be required to add additional class variables   
		# Considering adding a current measurement variable here

	# Some suggested functions to implement, 
	def assign_node_indexes(self,):
		self.f_index = Nodes.node_index_dict[self.vp_node]
		self.t_index = Nodes.node_index_dict[self.vn_node]
		# Add an additional node index to the node dictionary
		# for a dummy node
		Nodes.node_index_dict[self.name] = Nodes.index_counter + 1
		Nodes.index_counter += 1
	
	def stamp_sparse(self,):
		pass

	def stamp_dense(self, Y, J, curr_t):
		# Characterize sine wave
		V = np.sqrt(2/3)*self.amp_ph_ph_rms
		phase = self.phase_deg * np.pi / 180
		w = 2 * np.pi * self.frequency_hz
		t = curr_t
		Vt = V*np.sin((w*t) + phase)

		# Get indexes from node dictionary
		dummy = Nodes.node_index_dict[self.name] - 1
		f = self.f_index - 1
		t = self.t_index - 1

		# Conditionals for stamping Y and J
		if f != -1:
			Y[f, dummy] += 1
			Y[dummy, f] += 1
		if t != -1:
			Y[t, dummy] += -1
			Y[dummy, t] += -1
		J[dummy, 0] += Vt

	def stamp_open(self,):
		pass
        

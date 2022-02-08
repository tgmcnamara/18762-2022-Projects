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
        self.vp_index = -1
        self.np_index = -1
        self.current_index = -1
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,val):
        self.vp_index = Nodes.node_index_dict[self.vp_node]
        self.np_index = Nodes.node_index_dict[self.vn_node]
        
        #for i in range(val):
         #   if Nodes.index[i].name == self.vp_node:
          #      self.vp_index = Nodes.index[i]
           # if Nodes.index[i].name == self.vn_node:
            #    self.np_index = Nodes.index[i]
        #val = val + 1
        self.current_index = val
        val = val + 1
        return val
        
        
        
    def stamp_sparse(self,):#not worring about how to make sparse yet
        pass

    def stamp_dense(self,Y_dim):
        Y_mtx = np.zeros((Y_dim,Y_dim))
        if self.vn_node == 'gnd': #only one groud index so need to make sure accounting for which end is connected to ground
            Y_mtx[self.current_index, self.vp_index] += 1 #voltage (extra row) (should this be stamped into Jmatrix)
            Y_mtx[self.vp_index, self.current_index] += -1 #current(extra columb)
            return Y_mtx
        if self.vp_index == 'gnd':
            Y_mtx[self.current_index, self.np_index] += -1 #voltage 
            Y_mtx[self.np_index, self.current_index] += 1 #current
            return Y_mtx

        else: #voltage source not connected to a ground (struggling to figure this out)


        
            return Y_mtx 
        

    def stamp_open(self,): #not sure what this one is about
        pass
        

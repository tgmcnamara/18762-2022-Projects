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
        self.V_current_index = -1
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        self.vp_index = Nodes.node_index_dict[self.vp_node]
        self.np_index = Nodes.node_index_dict[self.vn_node]
        self.V_current_index = Nodes.index_counter
        Nodes.index_counter += 1
        print(self.name + '_voltage' + str(self.vp_index) + '_current' + str(self.V_current_index))        
        
    def stamp_sparse(self,):#not worring about how to make sparse yet
        pass

    def stamp_dense(self,Y_mtx, J_mtx, time): #(THIS WORKS)
        if time != 0:
            Y_mtx[self.vp_index,self.V_current_index] += 1
            Y_mtx[self.np_index,self.V_current_index] += -1
            Y_mtx[self.V_current_index,self.vp_index] += 1
            Y_mtx[self.V_current_index,self.np_index] += -1
            J_mtx[self.V_current_index,0] = np.sqrt(2/3)*self.amp_ph_ph_rms*np.sin(2*(np.pi)*self.frequency_hz*time + np.radians(self.phase_deg))
        else:
            Y_mtx[self.V_current_index,self.V_current_index] += 1
            J_mtx[self.V_current_index,0] = np.sqrt(2/3)*self.amp_ph_ph_rms*np.sin(2*(np.pi)*self.frequency_hz*time + np.radians(self.phase_deg))
        
        

        

    def stamp_open(self,): #not sure what this one is about
        pass
        

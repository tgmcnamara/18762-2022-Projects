import numpy as np
from itertools import count
from classes.Nodes import Nodes
#from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse
#third
class Capacitors:
    def __init__(self, name, from_node, to_node, c):
        self.name = name
        self.c = c
        self.from_node = from_node
        self.to_node = to_node
        self.from_index = -1
        self.to_index = -1
        self.comp_index = -1
        self.Vcp_index = -1
        self.Vcn_index = -1
        self.c_curr_index =-1
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,val):
        val +=1
        self.comp_index = val
        self.from_index = Nodes.node_index_dict[self.from_node]
        self.to_index = self.comp_index

        if self.to_node == 'gnd': #this accounts for the voltage source from the companion model
            self.Vpc_index = self.comp_index
        else:
            self.Vcp_index = self.comp_index
            self.Cvn_index = Nodes.node_index_dict[self.to_index]    

        self.c_curr_index = val
        val += 1 #accounts for the addition of voltage source from companion model
        return val
         
         
        #not sure If I should add to counter and insert a voltage source for a capacitor

        
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,Y_mtx, J_mtx, d_t):#do we need to include delta t
        Y_mtx[self.from_index,self.from_index] += d_t/(2*self.c) #Yii index
        Y_mtx[self.from_index,self.comp_index] += -d_t/(2*self.c) #Yij index
        Y_mtx[self.comp_index,self.from_index] += -d_t/(2*self.c) #Yji index
        Y_mtx[self.comp_index,self.comp_index] += d_t/(2*self.c) #Yjj index
        
        if self.to_node == 'gnd': #only one groud index so need to make sure accounting for which end is connected to ground
            Y_mtx[self.c_curr_index, self.Vcp_index] += 1 #voltage (extra row) (should this be stamped into Jmatrix)
            Y_mtx[self.Vcp_index, self.c_curr_index] += -1 #current(extra columb)
            J_mtx[self.Vcp_index,0] += 0
            J_mtx[self.c_curr_index,0] += Vn + (d_t/(2*self.c))*In #(I think these come from Vinit)
            #how am I supposed to know how to accuratly sellect Vn and In, do the corrospond to Vcp and c_curr

        else: #voltage source not connected to a ground (struggling to figure this out)
            Y_mtx[self.Vcp_index,self.Vcp_index] = 1 #Yii index
            Y_mtx[self.Vcp_index,self.Vcp_index] = -1 #Yij index
            Y_mtx[self.Vcn_index,self.Vcp_index] = -1 #Yji index
            Y_mtx[self.Vcn_index,self.Vcn_index] = 1 #Yjj index
        
        
        

    def stamp_open(self,):#not sure what to do
        pass
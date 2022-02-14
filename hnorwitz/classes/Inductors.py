import sys
sys.path.append("..")
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class Inductors:
    def __init__(self, name, from_node, to_node, l):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.l = l
        self.from_index = -1
        self.to_index = -1  
        self.l_comp_index = -1
        self.l_curr_index =-1
        #self.Vlp_index = -1
        #self.Vln_index = -1
        
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        self.from_index = Nodes.node_index_dict[self.from_node]
        self.to_index = Nodes.node_index_dict[self.to_node]
        self.l_comp_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.l_curr_index = Nodes.index_counter
        Nodes.index_counter += 1
        print(self.name + '_voltage' + str(self.l_comp_index) +'_current'+ str(self.l_curr_index))
    #####    
      
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_mtx, J_mtx, d_t, prev, time): 
        #need and inf at time ==0 here
        if time == 0:
            Y_mtx[self.from_index,self.from_index] += (d_t/(2*self.l)) #Yii index
            Y_mtx[self.from_index,self.l_comp_index] += -(d_t/(2*self.l)) #Yij index
            Y_mtx[self.l_comp_index,self.from_index] += -(d_t/(2*self.l)) #Yji index
            Y_mtx[self.l_comp_index,self.l_comp_index] += (d_t/(2*self.l)) #Yjj index
            Y_mtx[self.to_index,self.l_curr_index] += -1 #(THIS WORKS)
            Y_mtx[self.l_comp_index, self.l_curr_index] += 1#Yab
            Y_mtx[self.l_curr_index, self.to_index] += -1#Ybj
            Y_mtx[self.l_curr_index, self.l_comp_index] += 1#Yba
            ####(EVERYTHING is now correct)
            J_mtx[self.l_curr_index,0] = prev[self.l_comp_index] + (d_t/(2*self.l))*prev[self.l_curr_index]
            J_mtx[self.from_index,0] = -(prev[self.l_curr_index]+ (d_t/(2*self.l))*prev[self.l_comp_index])#from_index also seems to work
            J_mtx[self.l_comp_index,0] = (prev[self.l_curr_index]+ (d_t/(2*self.l))*prev[self.l_comp_index])#same
        else:
            J_mtx[self.l_curr_index,0] = prev[self.l_comp_index] + (d_t/(2*self.l))*prev[self.l_curr_index]
            J_mtx[self.from_index,0] = -(prev[self.l_curr_index]+ (d_t/(2*self.l))*prev[self.l_comp_index])#from_index also seems to work
            J_mtx[self.l_comp_index,0] = (prev[self.l_curr_index]+ (d_t/(2*self.l))*prev[self.l_comp_index])
        
         

    def stamp_short(self,Y_mtx):#not sure what to do withi this
        Y_mtx[self.l_comp_index, self.to_index] = -1
        Y_mtx[self.l_comp_index, self.l_comp_index] = 1
        Y_mtx[self.l_curr_index,self.l_curr_index] = 1
        #if it is a sort then the from_node and to_node have the same voltage
        #[1, 1; 1, 1]
        
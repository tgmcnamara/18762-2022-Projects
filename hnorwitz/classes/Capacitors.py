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
        self.c_curr_index =-1
        #self.Vcp_index = -1
        #self.Vcn_index = -1
        
        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):#in this methode we do count the gnd
        self.from_index = Nodes.node_index_dict[self.from_node]
        self.to_index = Nodes.node_index_dict[self.to_node]
        self.comp_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.c_curr_index = Nodes.index_counter
        Nodes.index_counter += 1
        print(self.name + '_voltage' + str(self.comp_index) + '_current'+str(self.c_curr_index))
        
        ##
        #self.from_index = Nodes.node_index_dict[self.from_node]
        #self.to_index = self.comp_index

        #if self.to_node == 'gnd': #this accounts for the voltage source from the companion model
        #    self.Vpc_index = self.comp_index
        #else:
         #   self.Vcp_index = self.comp_index
          #   self.Vcn_index = Nodes.node_index_dict[self.to_index]    

        #Nodes.index_counter += 1 #accounts for the addition of voltage source from companion model
        #self.c_curr_index = Nodes.index_counter
         ##
         
        #not sure If I should add to counter and insert a voltage source for a capacitor

        
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,Y_mtx, J_mtx, d_t,prev,time):#do we need to include delta t 
        if time == 0:
            Y_mtx[self.from_index,self.from_index] += d_t/(2*self.c) #Yii index
            Y_mtx[self.from_index,self.comp_index] += -d_t/(2*self.c) #Yia index
            Y_mtx[self.comp_index,self.from_index] += -d_t/(2*self.c) #Yai index
            Y_mtx[self.comp_index,self.comp_index] += d_t/(2*self.c) #Yaa index
            Y_mtx[self.to_index, self.c_curr_index] += -1#Yjb (+)may need to swap all of these
            Y_mtx[self.comp_index, self.c_curr_index] += 1#Yab (-)
            Y_mtx[self.c_curr_index, self.to_index] += -1#Ybj(+)
            Y_mtx[self.c_curr_index, self.comp_index] += 1#Yba(-)
            J_mtx[self.c_curr_index,0] = prev[self.from_index] + (d_t/(2*self.c))*prev[self.c_curr_index]#for v(tn) need to use from index
        else:
            J_mtx[self.c_curr_index,0] = prev[self.from_index] + (d_t/(2*self.c))*prev[self.c_curr_index]
        
        
        
    #KEEP THIS
    def stamp_open(self,Y_mtx):#not sure what to do
        Y_mtx[self.comp_index, self.to_index] += -1
        Y_mtx[self.comp_index, self.comp_index] += 1
        Y_mtx[self.c_curr_index,self.c_curr_index] = 1
        pass
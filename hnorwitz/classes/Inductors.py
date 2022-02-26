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
        self.l_comp_index = -1 #INDEXING ADDITIONAL NODE
        self.l_curr_index =-1 #INDEX FOR VOLTAGE SOURCE
        #self.prev_current = .0001 #HOW I WAS GOING TO HOLD PREVIOUS CURRENT FOR CALCULATIONS IF i DID NOT ADD VOLTAGE STAMP 
        #self.list_val = [] #HOW I WAS GOING TO KEEP TRACK OF CURRENTS IF DID NOT ADD VOLTAGE STAMP
        
     
    def assign_node_indexes(self,):
        ###IF AND ELSE STATEMENTS WERE WHEN I WAS TRYING TO FIGURE OUT HOW TO NOT COUNT GROUND
        #if self.to_node == 'gnd':
            #self.from_index = Nodes.node_index_dict[self.from_node]
    
        #else:
            self.from_index = Nodes.node_index_dict[self.from_node]
            self.to_index = Nodes.node_index_dict[self.to_node]
            self.l_comp_index = Nodes.index_counter
            Nodes.index_counter += 1
            self.l_curr_index = Nodes.index_counter#zero volt independendent voltage source
            Nodes.index_counter += 1
            print("voltage across " + str(self.name)+ " is "+str(self.from_index)+ " minus " + str(self.l_comp_index))
            print("comp index "+str(self.l_comp_index))
            print("current "+ str(self.l_curr_index))
            
    #####    
      
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_mtx, J_mtx, d_t, prev, t): 
        

        ####ATTEMPTING TO NOT USE VOLTAGE SOURCE AND JUST CALCULATE THE CURRENT AT THIS MOMENT AND THEN STORE IT
        #Y_mtx[self.from_index,self.from_index] += (d_t/(2*self.l)) #Yii index
        #Y_mtx[self.from_index,self.to_index] += -(d_t/(2*self.l)) #Yij index
        #Y_mtx[self.to_index,self.from_index] += -(d_t/(2*self.l)) #Yji index
        #Y_mtx[self.to_index,self.to_index] += (d_t/(2*self.l)) #Yjj index
        #J_mtx[self.from_index,0] = -(self.prev_current+ (d_t/(2*self.l))*(prev[self.from_index]-prev[self.to_index]))#from_index also seems to work
        #J_mtx[self.to_index,0] = (self.prev_current+ (d_t/(2*self.l))*(prev[self.from_index]-prev[self.to_index]))#same    
        #self.prev_current = (self.prev_current + (d_t/(2*self.l))*(prev[self.from_index]- prev[self.to_index])) + (d_t/(2*self.l))*(prev[self.from_index]-prev[self.to_index])
        #self.list_val.append(self.prev_current)
        ####################################################################
        
        ####INCLUDING 0 VOLTAGE SOUCE STAMP AND GETTING PREVIOUS CURRENT FROM V VECTOR
        Y_mtx[self.from_index,self.from_index] += (d_t/(2*self.l)) #Yii index
        Y_mtx[self.from_index,self.l_comp_index] += -(d_t/(2*self.l)) #Yij index
        Y_mtx[self.l_comp_index,self.from_index] += -(d_t/(2*self.l)) #Yji index
        Y_mtx[self.l_comp_index,self.l_comp_index] += (d_t/(2*self.l)) #Yjj index
        ##0 VOLTAGE SOURCE STAMP
        Y_mtx[self.to_index,self.l_curr_index] += -1 #
        Y_mtx[self.l_comp_index, self.l_curr_index] += 1#Yab
        Y_mtx[self.l_curr_index, self.to_index] += -1#Ybj
        Y_mtx[self.l_curr_index, self.l_comp_index] += 1#Yba

        #####STAMP JMATRIX
        J_mtx[self.from_index,0] = -(prev[self.l_curr_index]+ (d_t/(2*self.l))*(prev[self.from_index]-prev[self.l_comp_index]))#+ (d_t/(2*self.l))*(prev[self.from_index]-prev[self.l_comp_index]))#from_index also seems to work
        J_mtx[self.l_comp_index,0] = (prev[self.l_curr_index]+ (d_t/(2*self.l))*(prev[self.from_index]-prev[self.l_comp_index]))#+(d_t/(2*self.l))*(prev[self.from_index]-prev[self.l_comp_index]))#same

        
         

    def stamp_short(self,Y_mtx):#,J_mtx,prev,d_t):#DEFINITKY NOT WORK
        ####WAS TRYING TO GET MY SHORT STAMP WORKING
        Y_mtx[self.from_index, self.from_index] += 1 #these ensure from node and comp node are 0
        Y_mtx[self.from_index, self.l_comp_index] += -1
        Y_mtx[self.l_comp_index,self.l_comp_index] += 1
        Y_mtx[self.l_comp_index,self.from_index] += -1

        #####PREVENT 0 ROW OR COLUM WHEN RUN LINSOV
        Y_mtx[self.l_comp_index,self.l_comp_index] += 1
        Y_mtx[self.l_curr_index,self.l_curr_index] += 1
        
        
        
        
        
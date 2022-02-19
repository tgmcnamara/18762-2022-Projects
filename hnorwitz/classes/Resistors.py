
import numpy as np
from itertools import count
from classes.Nodes import Nodes


class Resistors:
    def __init__(self, name, from_node, to_node, r):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.r = r
        self.from_index = -1
        self.to_index = -1

        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,):
        #####IF AND ELSE STATEMENTS WERE FROM WHEN I WAS NOT INCLUDEING GROUND IN INDEXING
        #if self.to_node == 'gnd':
        #    self.from_index = Nodes.node_index_dict[self.from_node]
        #else:
            self.from_index = Nodes.node_index_dict[self.from_node]
            self.to_index = Nodes.node_index_dict[self.to_node]
            print("voltage across " + str(self.name)+ " is "+str(self.from_index) + " minus " + str(self.to_index))
        
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, Y_mtx):
        ####IF AND ELSE WERE FOR WHEN I WAS NOT STAMPING WITH GROUND
        #if self.to_node == 'gnd':
        #    Y_mtx[self.from_index,self.from_index] += 1/self.r #Yii index
        #    pass
        #else:
        Y_mtx[self.from_index,self.from_index] += 1/self.r #Yii index
        Y_mtx[self.from_index,self.to_index] += -1/self.r #Yij index
        Y_mtx[self.to_index,self.from_index] += -1/self.r #Yji index
        Y_mtx[self.to_index,self.to_index] += 1/self.r #Yjj index
           

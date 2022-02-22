import sys
import numpy as np
from itertools import count
from classes.Nodes import Nodes
# from lib.stamping_functions import stamp_y_sparse, stamp_j_sparse

class InductionMotors:
    def __init__(
        self,
        name,
        phase_a_node,
        phase_b_node,
        phase_c_node,
        power_nom,
        v_nom,
        motor_freq,
        lm,
        rs,
        rr,
        lls,
        llr,
        j,
        tm,
        d_fric,
        n_pole_pairs):
        self.name = name
        self.phase_a_node = phase_a_node
        self.phase_b_node = phase_b_node
        self.phase_c_node = phase_c_node
        self.power_nom = power_nom
        self.v_nom = v_nom
        self.motor_freq = motor_freq
        self.lm = lm
        self.rs = rs
        self.rr = rr
        self.lls = lls
        self.llr = llr
        self.j = j
        self.tm = tm
        self.d_fric = d_fric
        self.n_pole_pairs = n_pole_pairs
        self.lss = self.lls + self.lm
        self.lrr = self.llr + self.lm
        ####Extrea variables (feel like I will need a lot of extrea variables)
        #do i need to do this for each phase
        self.phase_a_index = -1
        self.phase_b_index = -1
        self.phase_c_index = -1
        self.ids_index = -1#not sure if any of the current indexees are needed
        self.idr_index = -1
        self.iqs_index = -1
        self.iqr_index = -1
        self.vds_index = -1
        self.vqs_index = -1
        self.wr_index = -1
       
        ### intialize something to hold the previous NR values
        self.history = -1#don't think i need this
        self.prevkh = -1#don't think i need this since i am initialing this outside

        # You are welcome to / may be required to add additional class variables   

    # Some suggested functions to implement, 
    def assign_node_indexes(self,): 
        #NOT SURE IF i AM INDEXING CORRECTLY
        self.phase_a_index = Nodes.node_index_dict[self.phase_a_node]
        self.phase_b_index = Nodes.node_index_dict[self.phase_b_node]
        self.phase_c_index = Nodes.node_index_dict[self.phase_c_node]
        self.vds_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.vqs_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.ids_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.idr_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.iqs_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.iqr_index = Nodes.index_counter
        Nodes.index_counter += 1
        self.wr_index = Nodes.index_counter
        Nodes.index_counter += 1
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,Y_mtx, J_mtx, prev, prevkh,d_t, hist,time):#takes Y,J, previous V vector, current k vector, and time
        #prev = previous time step v vector
        #prevkh = previous values from kh iteration
        #hist = this holds previous dr values(not to sure about this one)
        theta = 0
        lamb = (2*np.pi)/3

        ####HISTORY USES PREVIOUS V VALUES TO KEEP TRACK(these do not change between NR iterations)
        hist_ds = prev[self.vds_index] - self.rs*prev[self.ids_index] + ((2/d_t)*((self.lss*prev[self.ids_index])+self.lm*prev[self.idr_index]))
        hist_qs = prev[self.vqs_index] - self.rs*prev[self.iqs_index] + ((2/d_t)*((self.lss*prev[self.iqs_index])+self.lm*prev[self.iqr_index]))
        hist_dr = (self.rr*prev[self.idr_index]) + ((self.lrr*prev[self.iqr_index]+self.lm*prev[self.ids_index])*prev[self.wr_index]) + ((2/d_t)*((self.lrr*(prev[self.idr_index]))+self.lm*prev[self.ids_index]))
        hist_qr = (self.rr*prev[self.iqr_index]) + ((self.lrr*prev[self.idr_index]+self.lm*prev[self.ids_index])*prev[self.wr_index]) + ((2/d_t)*((self.lrr*(prev[self.iqr_index]))+self.lm*prev[self.iqs_index]))
        hist_wr = (2/3)*self.n_pole_pairs*self.lm*((prev[self.idr_index]*prev[self.iqs_index]) - (prev[self.iqr_index]*prev[self.ids_index])) - prev[self.wr_index]*(self.d_fric-((2*self.j)/d_t)) - self.tm

        ########################################################################################
        ##converting from fabc to fdq (THIS IS INCROREST BUT THIS IS GENERALLY THE IDEA)#
        #Vds row in y (really not sure)
        Y_mtx[self.vds_index,self.phase_a_index] = 1#n+1,k
        Y_mtx[self.vds_index,self.phase_b_index] = -1#N+1, l  
        Y_mtx[self.vds_index,self.phase_c_index] = -Av #N+1,p
        Y_mtx[self.vds_index,self.phase_c_index] = Av#N+1,q
        Y_mtx[self.phase_a_index,self.vds_index] = -1
        Y_mtx[self.phase_a_index,self.vds_index] = 1#this should be the ground index
        ###attempt 2 for VDs row in Y(based off voltage controled voltage source stamp)###
        Y_mtx[self.vds_index,self.phase_a_index] = (2/3)*np.cos(theta)*prev[self.phase_a_index] 
        Y_mtx[self.vds_index,self.phase_b_index] = (2/3)*np.cos(theta-lamb)*prev[self.phase_b_index] 
        Y_mtx[self.vds_index,self.phase_c_index] = (2/3)*np.cos(theta+lamb)*prev[self.phase_c_index]
        Y_mtx[self.phase_a_index,self.vds_index] = -1
        Y_mtx[self.phase_a_index,self.vds_index] = 1#this should be the ground index
        ############
        #Vqs row in y
        Y_mtx[self.vqs_index,self.phase_a_index] = (2/3)*np.sin(theta)*prev[self.phase_a_index] 
        Y_mtx[self.vqs_index,self.phase_b_index] = (2/3)*np.sin(theta-lamb)*prev[self.phase_b_index] 
        Y_mtx[self.vqs_index,self.phase_c_index] = (2/3)*np.sin(theta+lamb)*prev[self.phase_c_index]
        Y_mtx[self.vqs_index,self.vqs_index] = -prev[self.iqs_index]

        #############
        vds = (2/3)*np.cos(theta)*prev[self.Vas] +(2/3)*np.cos(theta-lamb)*prev[self.vbs] +(2/3)*np.cos(theta+lamb)*prev[self.vcs]
        vqs = (2/3)*np.sin(theta)*prev[self.Vas] +(2/3)*np.sin(theta-lamb)*prev[self.vbs] +(2/3)*np.sin(theta+lamb)*prev[self.vcs]
        ids = (2/3)*np.cos(theta)*prev[self.Ias] +(2/3)*np.cos(theta-lamb)*prev[self.Ibs] +(2/3)*np.cos(theta+lamb)*prev[self.Ics]
        iqs = (2/3)*np.sin(theta)*prev[self.Ias] +(2/3)*np.sin(theta-lamb)*prev[self.Ibs] +(2/3)*np.sin(theta+lamb)*prev[self.Ics]
        ##############################################################################################################

        ##ALL THIS BELOW MY BELONG IN NON LINEAR STAMP OR FOR THE NEWTON RAPHSON########
        ####Ymtrix (stamp the Vd and Vq (current controlled voltage sources))
        #fds Y
        Y_mtx[self.ids_index, self.vds_index] = 1#dfdr/dvds
        Y_mtx[self.ids_index, self.vqs_index] = 0
        Y_mtx[self.ids_index, self.ids_index] = -self.rs -(2/d_t)*self.lss #dfdr/dids
        Y_mtx[self.ids_index, self.iqs_index] = 0
        Y_mtx[self.ids_index, self.idr_index] = -(2/d_t) * self.lm #dfdr/didr
        Y_mtx[self.ids_index, self.iqr_index] = 0
        Y_mtx[self.ids_index, self.wr_index] = 0
        #fds J
        J_mtx[self.ids_index,0] = -hist_ds + (1)*(prevkh[self.vds_index]) +(-self.rs -(2/d_t)*self.lss)*(prevkh[self.ids_index]) + (-(2/d_t) * self.lm)*(prevkh[self.idr_index]) #I think idrk and the others should be from
        ####I THINK VDSK_D_T AND IDSK_D_T, ETC SHOULD BE FROM PREVKH AND BE IN THE FORM prevkh[self.vds_index] and then the same for the rest

        #fqs Y
        Y_mtx[self.iqs_index, self.vds_index] = 0
        Y_mtx[self.iqs_index, self.vqs_index] = 1#dfqs/dvqs
        Y_mtx[self.iqs_index, self.ids_index] = 0 
        Y_mtx[self.iqs_index, self.iqs_index] = -self.rs -(2/d_t)*self.lss#dfqs/diqs
        Y_mtx[self.iqs_index, self.idr_index] = 0
        Y_mtx[self.iqs_index, self.iqr_index] = -(2/d_t) * self.lm#dfqs/diqr
        Y_mtx[self.iqs_index, self.wr_index] = 0
        #fqs J
        J_mtx[self.iqs_index,0] = -hist_qs + (1)*(prevkh[self.vqs_index]) +(-self.rs -(2/d_t)*self.lss)*(prevkh[self.iqs_index]) + (-(2/d_t) * self.lm)*(prevkh[self.iqr_index]) #not sure what I am supposed to do here

        #fdr y (implementing parital derivatives from work sheet)
        Y_mtx[self.idr_index, self.vds_index] = 0
        Y_mtx[self.idr_index, self.vqs_index] = 0
        Y_mtx[self.idr_index, self.ids_index] = -(2/d_t) * self.lm #dfdr/dids
        Y_mtx[self.idr_index, self.iqs_index] = self.lm*prevkh[self.wr_index]#dfdr/diqs
        Y_mtx[self.idr_index, self.idr_index] = self.rr - (2/d_t)*self.lrr#dfdr/didr
        Y_mtx[self.idr_index, self.iqr_index] = self.lrr * prevkh[self.wr_index]#dfdr/diqr
        Y_mtx[self.idr_index, self.wr_index] = (self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index]#dfdr/dwr
        #fdr J
        J_mtx[self.idr_index,0] = -hist_dr + (-(2/d_t) * self.lm)*(prevkh[self.ids_index]) +(self.lm*prevkh[self.wr_index])*(prevkh[self.iqs_index]) + (self.rr - (2/d_t)*self.lrr)*(prevkh[self.idr_index]) + ((self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index])*(prevkh[self.wr_index])#not sure what I am supposed to do here
        
        #fqr Y
        Y_mtx[self.iqr_index, self.vds_index] = 0
        Y_mtx[self.iqr_index, self.vqs_index] = 0
        Y_mtx[self.iqr_index, self.ids_index] = self.lm*prevkh[self.wr_index]#dfqr/dids
        Y_mtx[self.iqr_index, self.iqs_index] = (2/d_t) * self.lm#dfiqr/diqs
        Y_mtx[self.iqr_index, self.idr_index] = -self.lrr * prevkh[self.wr_index]#dfiqr/didr
        Y_mtx[self.iqr_index, self.iqr_index] = self.rr + (2/d_t)*self.lrr#dfiqr/diqr
        Y_mtx[self.iqr_index, self.wr_index] = -(self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index]#diqr/dwr
        #fqr J
        J_mtx[self.iqr_index,0] = -hist_qr + ((2/d_t) * self.lm)*(prevkh[self.iqs_index]) +(self.lm*prevkh[self.wr_index])*(prevkh[self.ids_index]) + (self.rr + (2/d_t)*self.lrr)*(prevkh[self.iqr_index]) + (-(self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index])*(prevkh[self.wr_index])#not sure what I am supposed to do here

        #fwr Y
        Y_mtx[self.wr_index, self.vds_index] = 0
        Y_mtx[self.wr_index, self.vqs_index] = 0
        Y_mtx[self.wr_index, self.ids_index] = -(3/2)*self.n_pole_pairs*self.lm*self.iqr_index#dwr/dids
        Y_mtx[self.wr_index, self.iqs_index] = (3/2)*self.n_pole_pairs*self.lm*self.idr_index#dwr/diqs
        Y_mtx[self.wr_index, self.idr_index] = (3/2)*self.n_pole_pairs*self.lm*self.iqs_index#dwr/didr
        Y_mtx[self.wr_index, self.iqr_index] = -(3/2)*self.n_pole_pairs*self.lm*self.ids_index#dwr/diqr
        Y_mtx[self.wr_index, self.wr_index] = -self.d_fric - (2*self.j)/d_t#dwr/dwr
        #fwr J
        J_mtx[self.wr_index,0] = -hist_wr +(-(3/2)*self.n_pole_pairs*self.lm*self.iqr_index)*(prevkh[self.ids_index]) + ((3/2)*self.n_pole_pairs*self.lm*self.idr_index)*(prevkh[self.iqs_index]) + (-(3/2)*self.n_pole_pairs*self.lm*self.ids_index)*(prevkh[self.iqr_index]) + (-self.d_fric - (2*self.j)/d_t)*(prevkh[self.wr_index])

        #########################
        #need to reset the historical values
        
        

    def stamp_t0(self,):#not sure how to set this up at the moment
        pass
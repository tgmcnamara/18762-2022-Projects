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
        self.history = -1
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

        ##converting from fabc to fdq (THIS IS INCROREST BUT THIS IS GENERALLY THE IDEA)
        vds = (2/3)*np.cos(theta)*prev[self.Vas] +(2/3)*np.cos(theta-lamb)*prev[self.vbs] +(2/3)*np.cos(theta+lamb)*prev[self.vcs]
        vqs = (2/3)*np.sin(theta)*prev[self.Vas] +(2/3)*np.sin(theta-lamb)*prev[self.vbs] +(2/3)*np.sin(theta+lamb)*prev[self.vcs]
        ids = (2/3)*np.cos(theta)*prev[self.Ias] +(2/3)*np.cos(theta-lamb)*prev[self.Ibs] +(2/3)*np.cos(theta+lamb)*prev[self.Ics]
        iqs = (2/3)*np.sin(theta)*prev[self.Ias] +(2/3)*np.sin(theta-lamb)*prev[self.Ibs] +(2/3)*np.sin(theta+lamb)*prev[self.Ics]

        ##ALL THIS BELOW MY BELONG IN NON LINEAR STAMP OR FOR THE NEWTON RAPHSON
        ####Ymtrix (stamp the Vd and Vq (current controlled voltage sources))
        #fds Y
        Y_mtx[self.ids_index, self.vds_index] = 1#dfdr/dvds
        Y_mtx[self.ids_index, self.vqs_index] = 0
        Y_mtx[self.ids_index, self.ids_index] = -self.rs -(2/d_t)*self.lss 
        Y_mtx[self.ids_index, self.iqs_index] = 0
        Y_mtx[self.ids_index, self.idr_index] = -(2/d_t) * self.lm
        Y_mtx[self.ids_index, self.iqr_index] = 0
        Y_mtx[self.ids_index, self.wr_index] = 0
        #fqs J
        J_mtx[self.ids_index,0] = -hist[self.ids_index] + (1)*(vdsk_d_t) +(-self.rs -(2/d_t)*self.lss)*(idsk_d_t) + (-(2/d_t) * self.lm)*(idrk_d_t) #not sure what I am supposed to do here
        
        #fqs Y
        Y_mtx[self.iqs_index, self.vds_index] = 0
        Y_mtx[self.iqs_index, self.vqs_index] = 1#dfqs/dvqs
        Y_mtx[self.iqs_index, self.ids_index] = 0 
        Y_mtx[self.iqs_index, self.iqs_index] = -self.rs -(2/d_t)*self.lss
        Y_mtx[self.iqs_index, self.idr_index] = 0
        Y_mtx[self.iqs_index, self.iqr_index] = -(2/d_t) * self.lm
        Y_mtx[self.iqs_index, self.wr_index] = 0
        #fqs J
        J_mtx[self.iqs_index,0] = -hist[self.iqs_index] + (1)*(vqsk_d_t) +(-self.rs -(2/d_t)*self.lss)*(iqsk_d_t) + (-(2/d_t) * self.lm)*(iqrk_d_t) #not sure what I am supposed to do here

        #fdr y (implementing parital derivatives from work sheet)
        Y_mtx[self.idr_index, self.vds_index] = 0
        Y_mtx[self.idr_index, self.vqs_index] = 0
        Y_mtx[self.idr_index, self.ids_index] = -(2/d_t) * self.lm #dfdr/dids
        Y_mtx[self.idr_index, self.iqs_index] = self.lm*prevkh[self.wr_index]#dfdr/diqs
        Y_mtx[self.idr_index, self.idr_index] = self.rr - (2/d_t)*self.lrr#dfdr/didr
        Y_mtx[self.idr_index, self.iqr_index] = self.lrr * prevkh[self.wr_index]#dfdr/diqr
        Y_mtx[self.idr_index, self.wr_index] = (self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index]#dfdr/dwr
        #fdr J
        J_mtx[self.idr_index,0] = -hist[self.idr_index] + (-(2/d_t) * self.lm)*(idsk_d_t) +(self.lm*prevkh[self.wr_index])*(iqsk_d_t) + (self.rr - (2/d_t)*self.lrr)*(idrk_d_t) + ((self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index])*(wrk_d_t)#not sure what I am supposed to do here
        
        #fqr Y
        Y_mtx[self.iqr_index, self.vds_index] = 0
        Y_mtx[self.iqr_index, self.vqs_index] = 0
        Y_mtx[self.iqr_index, self.ids_index] = self.lm*prevkh[self.wr_index]
        Y_mtx[self.iqr_index, self.iqs_index] = (2/d_t) * self.lm
        Y_mtx[self.iqr_index, self.idr_index] = -self.lrr * prevkh[self.wr_index]
        Y_mtx[self.iqr_index, self.iqr_index] = self.rr + (2/d_t)*self.lrr
        Y_mtx[self.iqr_index, self.wr_index] = -(self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index]
        #fqr J
        J_mtx[self.iqr_index,0] = -hist[self.iqr_index] + ((2/d_t) * self.lm)*(iqsk_d_t) +(self.lm*prevkh[self.wr_index])*(idsk_d_t) + (self.rr + (2/d_t)*self.lrr)*(iqrk_d_t) + (-(self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index])*(wrk_d_t)#not sure what I am supposed to do here

        #fwr Y(not sure if solved these out on paper correctly so not indcluding them yet)
        Y_mtx[self.wr_index, self.vds_index] = 0
        Y_mtx[self.wr_index, self.vqs_index] = 0
        Y_mtx[self.wr_index, self.ids_index] = 0
        Y_mtx[self.wr_index, self.iqs_index] = 0
        Y_mtx[self.wr_index, self.idr_index] = 0
        Y_mtx[self.wr_index, self.iqr_index] = 0
        Y_mtx[self.wr_index, self.wr_index] = 0
        #fqr J
        J_mtx[self.wr_index,0] = 0

        #####Jmatrix(stamp statevariable vds,vqs, vdr,vqr and swing)
        
        

    def stamp_t0(self,):#not sure how to set this up at the moment
        pass
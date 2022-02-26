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
        
        print("vds " +str(self.vds_index) + " ,vqs " +str(self.vqs_index) )
        print("ids " +str(self.ids_index) +",iqs " +str(self.iqs_index) +" ,idr " +str(self.idr_index) +",iqr " +str(self.iqr_index))
        print("wr "+str(self.wr_index))
        pass
        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self,Y_mtx, J_mtx, prev, prevkh,d_t):#takes Y,J, previous V vector, current k vector, and time step
        #prev = previous time step v vector
        #prevkh = previous values from kh iteration
        theta = 0
        lamb = (2*np.pi)/3
        ####DEFININGING MY PARKS AND INVERSE PARK
        Park = [[(2/3)*.5,(2/3)*.5,(2/3)*.5],
        [(2/3)*np.cos(theta),(2/3)*np.cos(theta-lamb),(2/3)*np.cos(theta+lamb)],
        [(2/3)*np.sin(theta),(2/3)*np.sin(theta-lamb),(2/3)*np.sin(theta+lamb)]]

        Inv_P = np.linalg.inv(Park)
        ##THIS IS HOW I GET IAS IBS AND ICS THROUGH PARKS TRANSFORM AND THEN STAMP THEM IN Y
        Y_mtx[self.phase_a_index, self.ids_index] = Inv_P[0,1]
        Y_mtx[self.phase_a_index, self.iqs_index] = Inv_P[0,2]
        Y_mtx[self.phase_b_index, self.ids_index] = Inv_P[1,1]
        Y_mtx[self.phase_b_index, self.iqs_index] = Inv_P[1,2]
        Y_mtx[self.phase_c_index, self.ids_index] = Inv_P[2,1]
        Y_mtx[self.phase_c_index, self.iqs_index] = Inv_P[2,2]

        ####HISTORY USES PREVIOUS V VALUES TO KEEP TRACK(these do not change between NR iterations)
        hist_ds = -prev[self.vds_index] + self.rs*prev[self.ids_index] - ((2/d_t)*((self.lss*prev[self.ids_index])+self.lm*prev[self.idr_index]))
        hist_qs = -prev[self.vqs_index] + self.rs*prev[self.iqs_index] - ((2/d_t)*((self.lss*prev[self.iqs_index])+self.lm*prev[self.iqr_index]))
        hist_dr = (self.rr*prev[self.idr_index]) + ((self.lrr*prev[self.iqr_index]+self.lm*prev[self.iqs_index])*prev[self.wr_index]) - ((2/d_t)*((self.lrr*(prev[self.idr_index]))+self.lm*prev[self.ids_index]))
        hist_qr = (self.rr*prev[self.iqr_index]) - ((self.lrr*prev[self.idr_index]+self.lm*prev[self.ids_index])*prev[self.wr_index]) - ((2/d_t)*((self.lrr*(prev[self.iqr_index]))+self.lm*prev[self.iqs_index]))
        #hist_wr = (3/2)*self.n_pole_pairs*self.lm*((prev[self.idr_index]*prev[self.iqs_index]) - (prev[self.iqr_index]*prev[self.ids_index])) + (((2*self.j)/d_t)-self.d_fric)*prev[self.wr_index] - 2*self.tm
        ####I REALIZE HIST_WR COULD BE WRITTEN OUT SIMPLIER BUT I FOUND THAT SUBTRACTING THE TWO GAVE DIFFERENT RESULTS SO I WROTE IT OUT FULL
        hist_wr = ((((3/2)*self.n_pole_pairs*self.lm*prev[self.idr_index])*((3/2)*self.n_pole_pairs*self.lm*prev[self.iqs_index]))-(((3/2)*self.n_pole_pairs*self.lm*prev[self.iqr_index])*((3/2)*self.n_pole_pairs*self.lm*prev[self.ids_index])))+ (((2*self.j)/d_t)-self.d_fric)*prev[self.wr_index] - 2*self.tm
        #wr_his_check = hist_wr - hist_wr_t
        #print("hist_wr "+str(hist_wr))

        ########################################################################################
        ##ALL THIS BELOW BELONG TO NON LINEAR STAMP FOR THE NEWTON RAPHSON########
        ####Ymtrix 
        ###Vds row in y
        Y_mtx[self.vds_index,self.phase_a_index] = (2/3)*np.cos(theta) 
        Y_mtx[self.vds_index,self.phase_b_index] = (2/3)*np.cos(theta-lamb) 
        Y_mtx[self.vds_index,self.phase_c_index] = (2/3)*np.cos(theta+lamb)
        Y_mtx[self.vds_index,self.vds_index] = -1
        
        
        ############
        #Vqs row in y
        Y_mtx[self.vqs_index,self.phase_a_index] = (2/3)*np.sin(theta)
        Y_mtx[self.vqs_index,self.phase_b_index] = (2/3)*np.sin(theta-lamb) 
        Y_mtx[self.vqs_index,self.phase_c_index] = (2/3)*np.sin(theta+lamb)
        Y_mtx[self.vqs_index,self.vqs_index] = -1
        

        #######################################################
        
        #fds Y 
        ds_dvds = -1#dfds/dvds
        ds_dids = self.rs +(2/d_t)*self.lss #dfds/dids
        ds_didr = (2/d_t) * self.lm #dfds/didr
        Y_mtx[self.ids_index, self.vds_index] = ds_dvds
        Y_mtx[self.ids_index, self.vqs_index] = 0
        Y_mtx[self.ids_index, self.ids_index] = ds_dids 
        Y_mtx[self.ids_index, self.iqs_index] = 0
        Y_mtx[self.ids_index, self.idr_index] = ds_didr
        Y_mtx[self.ids_index, self.iqr_index] = 0
        Y_mtx[self.ids_index, self.wr_index] = 0
        #fds J
        J_mtx[self.ids_index,0] = -hist_ds #STAMPING HISTORY IN J
        

        #fqs Y
        dqs_dvqs = -1 #dfqs/dvqs
        dqs_diqs = self.rs +(2/d_t)*self.lss#dfqs/diqs
        dqs_diqr = (2/d_t) * self.lm#dfqs/diqr
        Y_mtx[self.iqs_index, self.vds_index] = 0
        Y_mtx[self.iqs_index, self.vqs_index] = dqs_dvqs
        Y_mtx[self.iqs_index, self.ids_index] = 0 
        Y_mtx[self.iqs_index, self.iqs_index] = dqs_diqs
        Y_mtx[self.iqs_index, self.idr_index] = 0
        Y_mtx[self.iqs_index, self.iqr_index] = dqs_diqr
        Y_mtx[self.iqs_index, self.wr_index] = 0
        #fqs J
        J_mtx[self.iqs_index,0] = -hist_qs 

        #fdr y 
        ddr_dids =(2/d_t) * self.lm #dfdr/dids
        ddr_diqs = self.lm*prevkh[self.wr_index]#dfdr/diqs
        ddr_didr = self.rr + (2/d_t)*self.lrr#dfdr/didr(i origanlly had plus)
        ddr_diqr = self.lrr * prevkh[self.wr_index]#dfdr/diqr
        ddr_dwr = ((self.lrr*prevkh[self.iqr_index]) + self.lm*prevkh[self.iqs_index])#dfdr/dwr
        Y_mtx[self.idr_index, self.vds_index] = 0
        Y_mtx[self.idr_index, self.vqs_index] = 0
        Y_mtx[self.idr_index, self.ids_index] = ddr_dids
        Y_mtx[self.idr_index, self.iqs_index] = ddr_diqs
        Y_mtx[self.idr_index, self.idr_index] = ddr_didr
        Y_mtx[self.idr_index, self.iqr_index] = ddr_diqr
        Y_mtx[self.idr_index, self.wr_index] = ddr_dwr
        #fdr J
        J_mtx[self.idr_index,0] = -hist_dr 
        
        #fqr Y
        dqr_dids = -(self.lm*prevkh[self.wr_index])#dfqr/dids
        dqr_diqs = (2/d_t) * self.lm#dfiqr/diqs
        dqr_didr = -self.lrr * prevkh[self.wr_index]#dfiqr/didr
        dqr_diqr = self.rr + (2/d_t)*self.lrr#dfiqr/diqr
        dqr_dwr = -(self.lrr*prevkh[self.idr_index] + self.lm*prevkh[self.ids_index])#diqr/dwr
        Y_mtx[self.iqr_index, self.vds_index] = 0
        Y_mtx[self.iqr_index, self.vqs_index] = 0
        Y_mtx[self.iqr_index, self.ids_index] = dqr_dids
        Y_mtx[self.iqr_index, self.iqs_index] = dqr_diqs
        Y_mtx[self.iqr_index, self.idr_index] = dqr_didr
        Y_mtx[self.iqr_index, self.iqr_index] = dqr_diqr
        Y_mtx[self.iqr_index, self.wr_index] = dqr_dwr
        #fqr J
        J_mtx[self.iqr_index,0] = -hist_qr

        #fwr Y
        dwr_dids = -(3/2)*self.n_pole_pairs*self.lm*prevkh[self.iqr_index]#dwr/dids
        dwr_diqs = (3/2)*self.n_pole_pairs*self.lm*prevkh[self.idr_index]#dwr/diqs
        dwr_didr = (3/2)*self.n_pole_pairs*self.lm*prevkh[self.iqs_index]#dwr/didr
        dwr_diqr = -(3/2)*self.n_pole_pairs*self.lm*prevkh[self.ids_index]#dwr/diqr
        dwr_dwr = -(self.d_fric + (2*self.j)/d_t)#dwr/dwr
        Y_mtx[self.wr_index, self.vds_index] = 0
        Y_mtx[self.wr_index, self.vqs_index] = 0
        Y_mtx[self.wr_index, self.ids_index] = dwr_dids
        Y_mtx[self.wr_index, self.iqs_index] = dwr_diqs
        Y_mtx[self.wr_index, self.idr_index] = dwr_didr
        Y_mtx[self.wr_index, self.iqr_index] = dwr_diqr
        Y_mtx[self.wr_index, self.wr_index] = dwr_dwr
        #fwr J 
        J_mtx[self.wr_index,0] = -hist_wr 
        #print("J_wr " + str(np.amax(J_mtx[self.wr_index,0])))
        #########################
     
    def stamp_t0(self,Y_mtx):
        theta = 0
        lamb = (2*np.pi)/3

        ###FORCING INTIALLY EVERYTHING TO BE 0
        Y_mtx[self.ids_index,self.ids_index] = 1
        Y_mtx[self.iqs_index,self.iqs_index] = 1
        Y_mtx[self.idr_index,self.idr_index] = 1
        Y_mtx[self.iqr_index,self.iqr_index] = 1
        Y_mtx[self.wr_index,self.wr_index] = 1


        Y_mtx[self.vds_index,self.phase_a_index] = (2/3)*np.cos(theta)
        Y_mtx[self.vds_index,self.phase_b_index] = (2/3)*np.cos(theta-lamb)
        Y_mtx[self.vds_index,self.phase_c_index] = (2/3)*np.cos(theta+lamb)
        Y_mtx[self.vds_index,self.vds_index] = -1

        Y_mtx[self.vqs_index,self.phase_a_index] = (2/3)*np.sin(theta)
        Y_mtx[self.vqs_index,self.phase_b_index] = (2/3)*np.sin(theta-lamb) 
        Y_mtx[self.vqs_index,self.phase_c_index] = (2/3)*np.sin(theta+lamb)
        Y_mtx[self.vqs_index,self.vqs_index] = -1
        pass
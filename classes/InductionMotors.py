
import math


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
        # You are welcome to / may be required to add additional class variables   

    def assign_node_indexes(self, nodeLookup: dict):
        self.index_va = nodeLookup[self.phase_a_node]
        self.index_vb = nodeLookup[self.phase_b_node]
        self.index_vc = nodeLookup[self.phase_c_node]

        self.index_vds = self.claim_index(nodeLookup, "vds")
        self.index_vqs = self.claim_index(nodeLookup, "vqs")

        self.index_ids = self.claim_index(nodeLookup, "ids")
        self.index_iqs = self.claim_index(nodeLookup, "iqs")
        self.index_idr = self.claim_index(nodeLookup, "idr")
        self.index_iqr = self.claim_index(nodeLookup, "iqr")
        self.index_wr = self.claim_index(nodeLookup, "wr")

        #transform from ds and qs back to ia, ib, and ic
        self.index_ia = self.claim_index(nodeLookup, "ia")
        self.index_ib = self.claim_index(nodeLookup, "ib")
        self.index_ic = self.claim_index(nodeLookup, "ic")


    def claim_index(self, nodeLookup, index_name):
        modified_index = len(nodeLookup)
        nodeLookup[self.name + "-" + index_name] = modified_index
        return modified_index

    def get_nodes_connections(self):
        return [self.phase_a_node, self.phase_b_node, self.phase_c_node]

    def stamp_dense(self, Y, J, v_t_previous, v_k_previous, runtime, timestep):
        self.stamp_vds(Y)
        self.stamp_vqs(Y)

        self.stamp_fds(Y, J, timestep)
        self.stamp_fqs(Y, J, timestep)

    def stamp_vds(self, Y):
        Y[self.index_vds, self.index_va] = 2/3 * math.cos(0)
        Y[self.index_vds, self.index_vb] = 2/3 * math.cos(-2/3 * math.pi)
        Y[self.index_vds, self.index_vc] = 2/3 * math.cos(2/3 * math.pi)
    
    def stamp_vqs(self, Y):
        Y[self.index_vqs, self.index_va] = 2/3 * math.sin(0)
        Y[self.index_vqs, self.index_vb] = 2/3 * math.sin(-2/3 * math.pi)
        Y[self.index_vqs, self.index_vc] = 2/3 * math.sin(2/3 * math.pi)
    
    def stamp_fds(self, Y, J, timestep, v_t_previous, v_k_previous):
        Y[self.index_ids, self.index_vds] = -1
        Y[self.index_ids, self.index_ids] = self.rs + 2 / timestep * self.lss
        Y[self.index_ids, self.index_idr] = 2 / timestep * self.lm

    def stamp_fqs(self, Y, J, timestep, v_t_previous, v_k_previous):
        Y[self.index_iqs, self.index_vqs] = -1
        Y[self.index_iqs, self.index_iqs] = self.rs + 2 / timestep * self.lss
        Y[self.index_ids, self.index_iqr] = 2 / timestep * self.lm
    
    def stamp_fdr(self, Y, J, timestep, v_t_previous, v_k_previous):
        wr_k_previous = v_k_previous[self.index_wr]
        iqr_k_previous = v_k_previous[self.index_iqr]
        iqs_k_previous = v_k_previous[self.index_iqs]

        Y[self.index_idr, self.index_ids] = 2 / timestep * self.lm
        Y[self.index_idr, self.index_iqs] = self.lm * wr_k_previous
        Y[self.index_idr, self.index_idr] = self.rr + 2 / timestep * self.lrr
        Y[self.index_idr, self.index_iqr] = self.lrr * wr_k_previous
        Y[self.index_idr, self.index_wr] = self.lrr * iqr_k_previous + self.lm * iqs_k_previous
    
    def stamp_fqr(self, Y, J, timestep, v_t_previous, v_k_previous):
        wr_k_previous = v_k_previous[self.index_wr]
        idr_k_previous = v_k_previous[self.index_idr]
        ids_k_previous = v_k_previous[self.index_ids]

        Y[self.index_idr, self.index_ids] = -self.lm * wr_k_previous
        Y[self.index_idr, self.index_iqs] = 2 / timestep * self.lm
        Y[self.index_idr, self.index_idr] = -self.lrr * wr_k_previous

        Y[self.index_idr, self.index_iqr] = self.rr + 2 / timestep * self.lrr
        Y[self.index_idr, self.index_wr] = -(self.lrr * idr_k_previous + self.lm * ids_k_previous)
    
    def stamp_swing(self, Y, J, timestep, v_t_previous, v_k_previous):
        iqr_k_previous = v_k_previous[self.index_iqr]
        iqs_k_previous = v_k_previous[self.index_iqs]
        idr_k_previous = v_k_previous[self.index_idr]
        ids_k_previous = v_k_previous[self.index_ids]

        Y[self.index_wr, self.index_ids] = -3/2 * self.n_pole_pairs * self.lm * 

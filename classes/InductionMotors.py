
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
        self.index_node_a = nodeLookup[self.phase_a_node]
        self.index_node_b = nodeLookup[self.phase_b_node]
        self.index_node_c = nodeLookup[self.phase_c_node]

        self.index_vds = self.claim_index(nodeLookup, "vds")
        self.index_vqs = self.claim_index(nodeLookup, "vqs")

        self.index_ids = self.claim_index(nodeLookup, "ids")
        self.index_iqs = self.claim_index(nodeLookup, "iqs")
        self.index_idr = self.claim_index(nodeLookup, "idr")
        self.index_iqr = self.claim_index(nodeLookup, "iqr")
        self.index_wr = self.claim_index(nodeLookup, "wr")


    def claim_index(self, nodeLookup, index_name):
        modified_index = len(nodeLookup)
        nodeLookup[self.name + "-" + index_name] = modified_index
        return modified_index

    def get_nodes_connections(self):
        return [self.phase_a_node, self.phase_b_node, self.phase_c_node]

    def stamp_dense(self, Y, J, v_t_previous, v_k_previous, timestep):
        self.stamp_vds(Y)
        self.stamp_vqs(Y)

        self.stamp_fds(Y, J, timestep, v_t_previous, v_k_previous)
        self.stamp_fqs(Y, J, timestep, v_t_previous, v_k_previous)
        self.stamp_fdr(Y, J, timestep, v_t_previous, v_k_previous)
        self.stamp_fqr(Y, J, timestep, v_t_previous, v_k_previous)
        self.stamp_fswing(Y, J, timestep, v_t_previous, v_k_previous)

        self.stamp_ia(Y)
        self.stamp_ib(Y)
        self.stamp_ic(Y)

    def stamp_vds(self, Y):
        Y[self.index_vds, self.index_node_a] = 0.66667
        Y[self.index_vds, self.index_node_b] = -0.33333
        Y[self.index_vds, self.index_node_c] = 0.33333
        Y[self.index_vds, self.index_vds] = -1
    
    def stamp_vqs(self, Y):
        #Y[self.index_vqs, self.index_va] = 0
        Y[self.index_vqs, self.index_node_b] = -0.57735
        Y[self.index_vqs, self.index_node_c] = 0.57735
        Y[self.index_vqs, self.index_vqs] = -1
    
    def stamp_ia(self, Y):
        Y[self.index_node_a, self.index_ids] = 1.5
        Y[self.index_node_a, self.index_iqs] = -0.8660254

    def stamp_ib(self, Y):
        Y[self.index_node_b, self.index_ids] = 0
        Y[self.index_node_b, self.index_iqs] = -0.8660254

    def stamp_ic(self, Y):
        Y[self.index_node_c, self.index_ids] = 0
        Y[self.index_node_c, self.index_iqs] = 0.8660254

    def stamp_fds(self, Y, J, timestep, v_t_previous, v_k_previous):
        ids_t = v_t_previous[self.index_ids]
        idr_t = v_t_previous[self.index_idr]
        vds_t = v_t_previous[self.index_vds]

        ids_k = v_k_previous[self.index_ids]
        idr_k = v_k_previous[self.index_idr]
        vds_k = v_k_previous[self.index_vds]

        Y[self.index_ids, self.index_vds] = -1
        Y[self.index_ids, self.index_ids] = self.rs + 2 / timestep * self.lss
        Y[self.index_ids, self.index_idr] = 2 / timestep * self.lm

        psi_d_minus = self.lss * ids_t + self.lm * idr_t

        fds_minus = -vds_t + self.rs * ids_t - 2 / timestep * psi_d_minus

        psi_d_plus = self.lss * ids_k + self.lm * idr_k

        fds_plus = -vds_k + self.rs * ids_k + 2 / timestep * psi_d_plus

        fds_k = fds_minus + fds_plus

        delta_fds_k = -1 * vds_k \
            + (self.rs + 2 / timestep * self.lss) * ids_k \
            + 2 / timestep * self.lm * idr_k

        J[self.index_ids] = -fds_k + delta_fds_k

    def stamp_fqs(self, Y, J, timestep, v_t_previous, v_k_previous):
        iqs_t = v_t_previous[self.index_iqs]
        iqr_t = v_t_previous[self.index_iqr]
        vqs_t = v_t_previous[self.index_vqs]

        iqs_k = v_k_previous[self.index_iqs]
        iqr_k = v_k_previous[self.index_iqr]
        vqs_k = v_k_previous[self.index_vqs]

        Y[self.index_iqs, self.index_vqs] = -1
        Y[self.index_iqs, self.index_iqs] = self.rs + 2 / timestep * self.lss
        Y[self.index_iqs, self.index_iqr] = 2 / timestep * self.lm

        psi_q_minus = self.lss * iqs_t + self.lm * iqr_t

        fqs_minus = -vqs_t + self.rs * iqs_t - 2 / timestep * psi_q_minus

        psi_q_plus = self.lss * iqs_k + self.lm * iqr_k

        fqs_plus = -vqs_k + self.rs * iqs_k + 2 / timestep * psi_q_plus

        fds_k = fqs_minus + fqs_plus

        delta_fds_k = -1 * vqs_k \
            + (self.rs + 2 / timestep * self.lss) * iqs_k \
            + 2 / timestep * self.lm * iqr_k

        J[self.index_iqs] = -fds_k + delta_fds_k
    
    def stamp_fdr(self, Y, J, timestep, v_t_previous, v_k_previous):
        wr_t = v_t_previous[self.index_wr]
        iqr_t = v_t_previous[self.index_iqr]
        iqs_t = v_t_previous[self.index_iqs]
        idr_t = v_t_previous[self.index_idr]
        ids_t = v_t_previous[self.index_ids]

        wr_k = v_k_previous[self.index_wr]
        iqr_k = v_k_previous[self.index_iqr]
        iqs_k = v_k_previous[self.index_iqs]
        idr_k = v_k_previous[self.index_idr]
        ids_k = v_k_previous[self.index_ids]

        Y[self.index_idr, self.index_ids] = 2 / timestep * self.lm
        Y[self.index_idr, self.index_iqs] = self.lm * wr_k
        Y[self.index_idr, self.index_idr] = self.rr + 2 / timestep * self.lrr
        Y[self.index_idr, self.index_iqr] = self.lrr * wr_k
        Y[self.index_idr, self.index_wr] = self.lrr * iqr_k + self.lm * iqs_k

        psi_q_minus = self.lrr * iqr_t + self.lm * iqs_t

        psi_d_minus = self.lrr * idr_t + self.lm * ids_t

        fdr_minus = self.rr * idr_t + psi_q_minus * wr_t - 2 / timestep * psi_d_minus

        psi_q_plus = self.lrr * iqr_k + self.lm * iqs_k

        psi_d_plus = self.lrr * idr_k + self.lm * ids_k

        fdr_plus = self.rr * idr_k + psi_q_plus * wr_k + 2 / timestep * psi_d_plus

        fdr_k = fdr_minus + fdr_plus

        delta_fdr_k = 2 / timestep * self.lm * ids_k \
            + self.lm * wr_k * iqs_k \
            + (self.rr + 2 / timestep * self.lrr) * idr_k \
            + self.lrr * wr_k * iqr_k \
            + psi_q_plus * wr_k
        
        J[self.index_idr] = -fdr_k + delta_fdr_k
    
    def stamp_fqr(self, Y, J, timestep, v_t_previous, v_k_previous):
        iqr_t = v_t_previous[self.index_iqr]
        iqs_t = v_t_previous[self.index_iqs]
        idr_t = v_t_previous[self.index_idr]
        ids_t = v_t_previous[self.index_ids]
        wr_t = v_t_previous[self.index_wr]

        iqr_k = v_k_previous[self.index_iqr]
        iqs_k = v_k_previous[self.index_iqs]
        idr_k = v_k_previous[self.index_idr]
        ids_k = v_k_previous[self.index_ids]
        wr_k = v_k_previous[self.index_wr]

        Y[self.index_iqr, self.index_ids] = -self.lm * wr_k
        Y[self.index_iqr, self.index_iqs] = 2 / timestep * self.lm
        Y[self.index_iqr, self.index_idr] = -self.lrr * wr_k
        Y[self.index_iqr, self.index_iqr] = self.rr + 2 / timestep * self.lrr
        Y[self.index_iqr, self.index_wr] = -(self.lrr * idr_k + self.lm * ids_k)

        psi_d_minus = self.lrr * idr_t + self.lm * ids_t
        psi_q_minus = self.lrr * iqr_t + self.lm * iqs_t

        fqr_minus = self.rr * iqr_t - psi_d_minus * wr_t - 2 / timestep * psi_q_minus

        psi_d_plus = self.lrr * idr_k + self.lm * ids_k
        psi_q_plus = self.lrr * iqr_k + self.lm * iqs_k

        fqr_plus = self.rr * iqr_k - psi_d_plus * wr_k + 2 / timestep * psi_q_plus

        fqr_k = fqr_minus + fqr_plus

        delta_fqr_k = -self.lm * wr_k * ids_k \
            + 2 / timestep * self.lm * iqs_k \
            + -self.lrr * wr_k * idr_k \
            + (self.rr + 2 / timestep * self.lrr) * iqr_k \
            + -psi_d_plus
        
        J[self.index_iqr] = -fqr_k + delta_fqr_k
    
    def stamp_fswing(self, Y, J, timestep, v_t_previous, v_k_previous):
        iqr_t = v_t_previous[self.index_iqr]
        iqs_t = v_t_previous[self.index_iqs]
        idr_t = v_t_previous[self.index_idr]
        ids_t = v_t_previous[self.index_ids]
        wr_t = v_t_previous[self.index_wr]

        iqr_k = v_k_previous[self.index_iqr]
        iqs_k = v_k_previous[self.index_iqs]
        idr_k = v_k_previous[self.index_idr]
        ids_k = v_k_previous[self.index_ids]
        wr_k = v_k_previous[self.index_wr]

        Y[self.index_wr, self.index_ids] = -3/2 * self.n_pole_pairs * self.lm * iqr_k
        Y[self.index_wr, self.index_iqs] = 3/2 * self.n_pole_pairs * self.lm * idr_k
        Y[self.index_wr, self.index_idr] = 3/2 * self.n_pole_pairs * self.lm * iqs_k
        Y[self.index_wr, self.index_iqr] = -3/2 * self.n_pole_pairs * self.lm * ids_k
        Y[self.index_wr, self.index_wr] = -(self.d_fric + 2 * self.j / timestep)

        Te_minus = 3 / 2 * self.n_pole_pairs * self.lm * (idr_t * iqs_t - iqr_t * ids_t)
        
        fswing_minus = Te_minus + (2 * self.j / timestep - self.d_fric) * wr_t - 2 * self.tm

        Te_plus =  3 / 2 * self.n_pole_pairs * self.lm * (idr_k * iqs_k - iqr_k * ids_k)

        fswing_plus = Te_plus - (self.d_fric + 2 * self.j / timestep) * wr_k

        fswing_k = fswing_minus + fswing_plus

        delta_fswing_k = -3 / 2 * self.n_pole_pairs * self.lm * iqr_k * ids_k \
            + 3 / 2 * self.n_pole_pairs * self.lm * idr_k * iqs_k \
            + 3 / 2 * self.n_pole_pairs * self.lm * iqs_k * idr_k \
            + -3 / 2 * self.n_pole_pairs * self.lm * ids_k * iqr_k \
            + -(self.d_fric + 2 * self.j / timestep) * wr_k

        J[self.index_wr] = -fswing_k + delta_fswing_k
    
    def get_IM_waveforms(self, v_waveform):
        wr = []
        ids = []
        iqs = []
        idr = []
        iqr = []
        Te = []

        for frame in v_waveform:
            wr.append(frame[self.index_wr])
            ids.append(frame[self.index_ids])
            iqs.append(frame[self.index_iqs])
            idr.append(frame[self.index_idr])
            iqr.append(frame[self.index_iqr])

            Te.append(3 / 2 * self.n_pole_pairs * self.lm * (frame[self.index_idr] * frame[self.index_iqs] - frame[self.index_iqr] * frame[self.index_ids]))
        
        return { "wr": wr, "ids": ids, "iqs": iqs, "idr": idr, "iqr": iqr, "Te": Te }

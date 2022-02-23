
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
        self.phase_a_index = nodeLookup[self.phase_a_node]
        self.phase_b_index = nodeLookup[self.phase_b_node]
        self.phase_c_index = nodeLookup[self.phase_c_node]

    def get_nodes_connections(self):
        return [self.phase_a_node, self.phase_b_node, self.phase_c_node]

    def stamp_dense(self, Y, J, v_t_previous, v_k_previous, runtime, timestep):
        
        pass

    def return_nr_variables(v_k):
        pass

    def stamp_sparse(self,):
        pass

    def stamp_t0(self,):
        pass
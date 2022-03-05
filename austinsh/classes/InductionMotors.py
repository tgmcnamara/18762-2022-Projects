import sys
import numpy as np
import math
from classes import Nodes
from classes import VoltageSources

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
        self.theta = 0
    
    def assign_node_indexes(self,):
        self.phase_1_node = Nodes.node_index_dict[self.phase_a_node]
        self.phase_2_node = Nodes.node_index_dict[self.phase_b_node]
        self.phase_3_node = Nodes.node_index_dict[self.phase_c_node]
        return self.phase_1_node, self.phase_2_node, self.phase_3_node

        
    def stamp_sparse(self,):
        pass

    def stamp_dense(self, y_linear, j_matrix, vectors, t, tolerance, num_its, time_step):
        i = len(j_matrix) - 3
        j = len(j_matrix) - 2
        k = len(j_matrix) - 1

        cycles = -1
        sum = 1
        while sum > 0:
            iterations = 0
            while iterations < num_its:
                cycles += 1
                iterations += 1
                if cycles == 0 and t == 0:
                    x_guess = [j_matrix[i]*2/3*math.cos(self.theta) + j_matrix[j]*2/3*math.cos(self.theta - 2*np.pi/3) + 
                            j_matrix[k]*2/3*math.cos(self.theta + 2*np.pi/3), j_matrix[i]*2/3*math.sin(self.theta) +
                            j_matrix[j]*2/3*math.sin(self.theta - 2*np.pi/3) + j_matrix[k]*2/3*math.sin(self.theta + 2*np.pi/3),
                            0, 0, 0, 0, 0]
                    x_guess = np.vstack(x_guess)
                    
                    y_history = np.zeros((7,1))
                    y_history[0] = x_guess[0]
                    y_history[1] = x_guess[1]
                    y_history[0] = x_guess[0]
                    y_history[1] = x_guess[1]
                                
                elif cycles == 0:
                    step = int(t/time_step - 1)

                    x_guess = [j_matrix[i]*2/3*math.cos(self.theta) + j_matrix[j]*2/3*math.cos(self.theta - 2*np.pi/3) + 
                            j_matrix[k]*2/3*math.cos(self.theta + 2*np.pi/3), j_matrix[i]*2/3*math.sin(self.theta) +
                            j_matrix[j]*2/3*math.sin(self.theta - 2*np.pi/3) + j_matrix[k]*2/3*math.sin(self.theta + 2*np.pi/3),
                            0, 0, 0, 0, 0]
                    x_guess = np.vstack(x_guess)
                    
                    vds_n = vectors[step][0]
                    vqs_n = vectors[step][1]
                    ids_n = vectors[step][2]
                    iqs_n = vectors[step][3]
                    idr_n = vectors[step][4]
                    iqr_n = vectors[step][5]
                    wr_n = vectors[step][6]
                    
                    y_history = [vds_n, vqs_n,
                                vds_n - self.rs*ids_n + 2*((self.lls + self.lm)*ids_n + self.lm*idr_n)/time_step,
                                vqs_n - self.rs*iqs_n + 2*((self.lls + self.lm)*iqs_n + self.lm*iqr_n)/time_step,
                                self.rr*idr_n + ((self.llr + self.lm)*iqr_n + self.lm*iqs_n)*wr_n - 2*((self.llr + self.lm)*idr_n + self.lm*ids_n)/time_step,
                                -self.rr*iqr_n + ((self.llr + self.lm)*idr_n + self.lm*ids_n)*wr_n + 2*((self.llr + self.lm)*iqr_n + self.lm*iqs_n)/time_step,
                                3/2*self.n_pole_pairs*self.lm*(idr_n*iqs_n - iqr_n*ids_n) - (self.d_fric - (2*self.j/time_step))*wr_n]
                    y_history = np.vstack(y_history)
                else:
                    x_guess = x_new

                def Y_function(x_value):
                    vds = x_value[0]
                    vqs = x_value[1]
                    ids = x_value[2]
                    iqs = x_value[3]
                    idr = x_value[4]
                    iqr = x_value[5]
                    wr = x_value[6]

                    function = [vds, vqs,
                            vds - self.rs*ids - (2/time_step)*((self.lls + self.lm)*ids + self.lm*idr),
                            vqs - self.rs*iqs - (2/time_step)*((self.lls + self.lm)*iqs + self.lm*iqr),
                            self.rr*idr + ((self.llr + self.lm)*iqr + self.lm*iqs)*wr + (2/time_step)*((self.llr + self.lm)*idr + self.lm*ids),
                            -self.rr*iqr + ((self.llr + self.lm)*idr + self.lm*ids)*wr - (2/time_step)*((self.llr + self.lm)*iqr + self.lm*iqs),
                            3/2*self.n_pole_pairs*self.lm*(idr*iqs - iqr*ids) - (self.d_fric + (2*self.j/time_step))*wr - 2*self.tm]
                    iter_and_history = np.vstack(function) + np.vstack(y_history)
                    return iter_and_history
                
                def Y_derivative(x_value):
                    vds = x_value[0]
                    vqs = x_value[1]
                    ids = x_value[2]
                    iqs = x_value[3]
                    idr = x_value[4]
                    iqr = x_value[5]
                    wr = x_value[6]

                    derivative = np.zeros((7,7))
                    derivative[0,:] = [1, 0, 0, 0, 0, 0, 0]
                    derivative[1,:] = [0, 1, 0, 0, 0, 0, 0]
                    derivative[2,:] = [1, 0, -(self.rs + 2*(self.lls + self.lm)/time_step), 0, -2*self.lm/time_step,
                                        0, 0]
                    derivative[3,:] = [0, 1, 0, -(self.rs + 2*(self.lls + self.lm)/time_step), 0,
                                        -2*self.lm/time_step, 0]
                    derivative[4,:] = [0, 0, 2*self.lm/time_step, self.lm*wr, self.rr + 2*(self.llr + self.lm)/time_step,
                                        (self.llr + self.lm)*wr, (self.llr + self.lm)*iqr + self.lm*iqs]
                    derivative[5,:] = [0, 0, self.lm*wr, -2*self.lm/time_step, (self.llr+self.lm)*wr,
                                        -(self.rr + 2*(self.llr+self.lm)/time_step), (self.llr + self.lm)*idr + self.lm*ids]
                    derivative[6,:] = [0, 0, -3*self.n_pole_pairs*self.lm*iqr/2, 3*self.n_pole_pairs*self.lm*idr/2,
                                        3*self.n_pole_pairs*self.lm*iqs/2, -3*self.n_pole_pairs*self.lm*ids/2,
                                        -(self.d_fric + 2*self.j/time_step)]
                    return derivative

                y_function = Y_function(x_guess)
                y_derivative = Y_derivative(x_guess)
                rhs = np.dot(y_derivative, x_guess) - y_function

                x_new = np.linalg.solve(y_derivative, rhs)
                
            diff = abs(Y_function(x_new) - Y_function(x_guess))
            computation = diff > tolerance
            computation = computation.astype(int)
            sum = int(np.sum(computation))
            print(cycles)
        vectors_history = x_new
        return vectors_history


    def stamp_t0(self,):
        pass
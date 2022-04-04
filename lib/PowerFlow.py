import numpy as np
from scipy.sparse.linalg import spsolve
from lib.MatrixBuilder import MatrixBuilder
from lib.settings import Settings
import math as math

V_DIFF_MAX = 1
V_MAX = 5
V_MIN = -5

class PowerFlow:

    def __init__(self, settings: Settings, raw_data, size_Y):
        self.settings = settings
        self.size_Y = size_Y

        self.buses = raw_data['buses']
        self.slack = raw_data['slack']
        self.generator = raw_data['generators']
        self.transformer = raw_data['xfmrs']
        self.branch = raw_data['branches']
        self.shunt = raw_data['shunts']
        self.load = raw_data['loads']

        self.linear_elments = self.slack + self.branch + self.shunt + self.transformer
        self.nonlinear_elements = self.generator + self.load

    def solve(self, Y, J):
        if self.settings.use_sparse:
            return spsolve(Y, J)
        else:
            return np.linalg.solve(Y, J)

    def apply_limiting(self, v_next, v_previous, diff):
        #voltage limiting
        for bus in self.buses:
            v_next[bus.node_Vr] = np.clip(v_previous[bus.node_Vr] + np.clip(diff[bus.node_Vr], -V_DIFF_MAX, V_DIFF_MAX), V_MIN, V_MAX)
            v_next[bus.node_Vi] = np.clip(v_previous[bus.node_Vi] + np.clip(diff[bus.node_Vi], -V_DIFF_MAX, V_DIFF_MAX), V_MIN, V_MAX)

        return v_next

    def stamp_linear(self, Y: MatrixBuilder, J, v_previous):
        for element in self.linear_elments:
            element.stamp(Y, J, v_previous)
            Y.assert_valid()

    def stamp_nonlinear(self, Y: MatrixBuilder, J, v_previous):
        for element in self.nonlinear_elements:
            element.stamp(Y, J, v_previous)
            Y.assert_valid()

    def run_powerflow(self, v_init):

        v_previous = np.copy(v_init)

        Y = MatrixBuilder(self.settings, self.size_Y)
        J_linear = [0] * len(v_init)

        self.stamp_linear(Y, J_linear, v_previous)

        linear_index = Y.get_usage()

        for iteration_num in range(self.settings.max_iters):
            J = J_linear.copy()

            self.stamp_nonlinear(Y, J, v_previous)

            Y.assert_valid(check_zeros=True)

            v_next = self.solve(Y.to_matrix(), J)

            if np.isnan(v_next).any():
                raise Exception("Error solving linear system")

            diff = v_next - v_previous

            err = abs(diff)

            err_max = err.max()
            
            if err_max < self.settings.tolerance:
                return (v_next, iteration_num)
            elif self.settings.limiting and err_max > self.settings.tolerance:
                v_next = self.apply_limiting(v_next, v_previous, diff)

            v_previous = v_next
            Y.clear(retain_idx=linear_index)

        raise Exception("Exceeded maximum NR iterations")
    
    def dump_index_map(self):
        map = {}

        for bus in self.buses:
            map[f'bus-{bus.Bus}-Vr'] = bus.node_Vr
            map[f'bus-{bus.Bus}-Vi'] = bus.node_Vi
            if bus.node_Q != None:
                map[f'bus-{bus.Bus}-Q'] = bus.node_Q
        
        for slack in self.slack:
            map[f'slack-{slack.bus.Bus}-Ir'] = slack.slack_Ir
            map[f'slack-{slack.bus.Bus}-Ii'] = slack.slack_Ii

        return map

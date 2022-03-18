import numpy as np
from scipy.sparse.linalg import spsolve
from lib.MatrixBuilder import MatrixBuilder
from lib.settings import Settings


class PowerFlow:

    def __init__(self, settings: Settings, raw_data):
        self.settings = settings

        self.slack = raw_data['slack']
        self.generator = raw_data['generators']
        self.transformer = raw_data['xfmrs']
        self.branch = raw_data['branches']
        self.shunt = raw_data['shunts']
        self.load = raw_data['loads']

        self.linear_elments = self.slack + self.branch + self.shunt + self.transformer
        self.nonlinear_elements = self.generator + self.load

    def solve(self):
        pass

    def apply_limiting(self):
        # TODO: PART 2, STEP 1 - Develop the apply_limiting function which implements voltage and reactive power
        #  limiting. Also, complete the else condition. Do not complete this step until you've finished Part 1.
        #  You need to decide the input arguments and return values.
        raise Exception("Variable limiting not implemented")

    def check_error(self):
        pass

    def stamp_linear(self, Y, J, v_previous):
        for element in self.linear_elments:
            element.stamp(Y, J, v_previous)

    def stamp_nonlinear(self, Y, J, v_previous):
        for element in self.nonlinear_elments:
            element.stamp(Y, J, v_previous)

    def run_powerflow(self, v_init):

        v_previous = np.copy(v_init)

        Y = MatrixBuilder()
        J_linear = [None] * len(v_init)

        self.stamp_linear(Y, J_linear, v_previous)

        linear_index = Y.get_usage()

        for _ in range(self.settings.max_iters):
            J = J_linear.copy()

            self.stamp_nonlinear()

            v_next = spsolve(Y.to_matrix(), J)

            err_max = (abs(v_next - v_previous)).max()
            
            if self.settings.limiting and err_max > self.settings.tolerance:
                self.apply_limiting()

            if err_max < self.settings.tolerance:
                return v_next

            v_previous = v_next
            Y.clear(retain_index=linear_index)

        raise Exception("Exceeded maximum NR iterations")

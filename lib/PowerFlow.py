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

    def stamp_linear(self, Y: MatrixBuilder, J, v_previous):
        for element in self.linear_elments:
            element.stamp(Y, J, v_previous)
            if self.settings.debug:
                Y.assert_valid()

    def stamp_nonlinear(self, Y: MatrixBuilder, J, v_previous):
        for element in self.nonlinear_elements:
            element.stamp(Y, J, v_previous)
            if self.settings.debug:
                Y.assert_valid()

    def run_powerflow(self, v_init):

        v_previous = np.copy(v_init)

        Y = MatrixBuilder()
        J_linear = [0] * len(v_init)

        self.stamp_linear(Y, J_linear, v_previous)

        linear_index = Y.get_usage()
        err_previous = 999999999999

        for _ in range(self.settings.max_iters):
            J = J_linear.copy()

            self.stamp_nonlinear(Y, J, v_previous)

            if self.settings.debug:
                Y.assert_valid(check_zeros=True)

            v_next = np.linalg.solve(Y.to_matrix().todense(), J) #TODO: spsolve(Y.to_matrix(), J)

            err_max = (abs(v_next - v_previous)).max()
            
            if self.settings.limiting and err_max > self.settings.tolerance:
                self.apply_limiting()

            if err_max < self.settings.tolerance:
                return v_next

            if err_max > err_previous:
                raise Exception("Failing to converge")

            v_previous = v_next
            Y.clear(retain_idx=linear_index)
            err_previous = err_max

        raise Exception("Exceeded maximum NR iterations")
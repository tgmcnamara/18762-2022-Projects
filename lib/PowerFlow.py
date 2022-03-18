import numpy as np
from scipy.sparse.linalg import spsolve
from lib.MatrixBuilder import MatrixBuilder
from lib.settings import Settings


class PowerFlow:

    def __init__(self, settings: Settings):
        self.settings = settings

    def solve(self):
        pass

    def apply_limiting(self):
        # TODO: PART 2, STEP 1 - Develop the apply_limiting function which implements voltage and reactive power
        #  limiting. Also, complete the else condition. Do not complete this step until you've finished Part 1.
        #  You need to decide the input arguments and return values.
        raise Exception("Variable limiting not implemented")

    def check_error(self):
        pass

    def stamp_linear(self):
        pass

    def stamp_nonlinear(self):
        pass

    def run_powerflow(self,
                      v_init,
                      bus,
                      slack,
                      generator,
                      transformer,
                      branch,
                      shunt,
                      load):

        v_previous = np.copy(v_init)

        Y = MatrixBuilder(len(v_init))
        J_linear = [None] * len(v_init)

        self.stamp_linear()

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

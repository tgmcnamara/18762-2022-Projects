import numpy as np
from scipy.sparse import lil_array
from scipy.sparse.linalg import spsolve

class MatrixProvider:
    def __init__(self, use_sparse, y_size):
        self.use_sparse = use_sparse
        self.y_size = y_size
    
    def generate_zero_vector(self):
        return np.zeros(self.y_size)
    
    def generate_zero_matrix(self):
        if self.use_sparse:
            return lil_array((self.y_size, self.y_size))
        else:
            return np.zeros((self.y_size, self.y_size))
    
    def solve(self, A, B):
        if self.use_sparse:
            return spsolve(A.asformat("csr"), B)
        else:
            return np.linalg.solve(A, B)

    def copy(self, x):
        if self.use_sparse:
            return x.copy()
        else:
            return np.copy(x)

    def max_difference(self, x, y):
        if self.use_sparse:
            return np.amax(np.abs(x - y))
        else:
            return (abs(x - y)).max()
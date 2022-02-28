import numpy as np

class MatrixProvider:
    def __init__(self, use_sparse, y_size):
        self.use_sparse = use_sparse
        self.y_size = y_size
    
    def generate_zero_vector(self):
        return np.zeros(self.y_size)
    
    def generate_zero_matrix(self):
        return np.zeros((self.y_size, self.y_size))
    
    def solve(self, A, B):
        return np.linalg.solve(A, B)

    def copy(self, x):
        return np.copy(x)

    def max_difference(self, x, y):
        return np.amax(np.abs(x - y))
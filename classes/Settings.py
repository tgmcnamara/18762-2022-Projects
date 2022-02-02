

from matplotlib import use


class Settings:
    def __init__(self, tolerance: float = 1E-05, maxNewtonIterations: int = 5, simulationTime: float = 0.2, useSparseMatrix: bool = False, timestep: float = 0.001):
        # Tolerance for Newton-Raphson
        self.tolerance = tolerance
        # Maximum number of newton iterations for non-linear loop at given time step
        self.maxNewtonIterations = maxNewtonIterations
        # Total time to simulate: [0, tf]
        self.simulationTime = simulationTime
        # Use sparse matrix formulation
        self.useSparseMatrix = useSparseMatrix
        # For now just letting this be defined up front
        self.timestep = timestep


from matplotlib import use


class Settings:
    def __init__(self, tolerance: float, maxNewtonIterations: int, simulationTime: float, useSparseMatrix: bool):
        self.tolerance = tolerance
        self.maxNewtonIterations = maxNewtonIterations
        self.simulationTime = simulationTime
        self.useSparseMatrix = useSparseMatrix
class Settings:
    def __init__(self, tolerance = 1E-05, max_iters = 1000, limiting = False, debug = False, use_sparse = True, flat_start = False, tx_stepping = False) -> None:
        self.tolerance = tolerance
        self.max_iters = max_iters
        self.limiting = limiting
        self.debug = debug
        self.use_sparse = use_sparse
        self.flat_start = flat_start
        self.tx_stepping = tx_stepping
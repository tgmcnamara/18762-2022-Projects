class Settings:
    def __init__(self, tolerance = 1E-05, max_iters = 1000, limiting = False, v_init = None, debug = False) -> None:
        """
        Args:
            tol (float): The chosen NR tolerance.
            max_iters (int): The maximum number of NR iterations.
            enable_limiting (bool): A flag that indicates if we use voltage limiting or not in our solver.
        """

        self.tolerance = tolerance
        self.max_iters = max_iters
        self.limiting = limiting
        self.v_init = v_init
        self.debug = debug
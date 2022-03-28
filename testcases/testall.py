import unittest
from lib.MatrixBuilder import MatrixBuilder
from lib.Solve import solve
from lib.settings import Settings
from models.Branches import Branches
from models.Buses import Bus
from models.Generators import Generators
from models.Loads import Loads
from models.Shunts import Shunts
from models.Slack import Slack
from models.Transformers import Transformers

class PowerFlowTests(unittest.TestCase):
    def test_generator(self):
        b = Bus(1, 2, 1, 0, None)
        b.assign_nodes()
        generator = Generators(1, 200, 1, None, None, None, None, None, None, None, None)

        settings = Settings(debug=True, max_iters=30)

        Y = MatrixBuilder(settings)
        J = [0, 0, 0]
        v_prev = [0.9819, -0.01673, 190]

        generator.stamp(Y, J, v_prev)

        matrix = Y.to_matrix().todense()

        print(matrix)
        print(J)

    def test_load(self):
        b = Bus(1, 2, 1, 0, None)
        b.assign_nodes()
        load = Loads(1, 200, 100, None, None, None, None, None, None)

        settings = Settings(debug=True, max_iters=30)

        Y = MatrixBuilder(settings)
        J = [0, 0]
        v_prev = [0.9819, -0.01673]

        load.stamp(Y, J, v_prev)

        matrix = Y.to_matrix().todense()

        print(matrix)
        print(J)

    def test_branch(self):
        b1 = Bus(1, 1, 1, 0, None)
        b1.assign_nodes()
        b2 = Bus(2, 1, 1, 0, None)
        b2.assign_nodes()

        branch = Branches(1, 2, 1.00800E-2, 5.04000E-2, 1.02500E-1, None, None, None, None)

        settings = Settings(debug=True, max_iters=30)

        Y = MatrixBuilder(settings)
        J = [0, 0]
        v_prev = None

        branch.stamp(Y, J, v_prev)

        matrix = Y.to_matrix().todense()

        print(matrix)
        print(J)
    
    def test_shunt(self):
        b = Bus(1, 2, 1, 0, None)
        b.assign_nodes()
        shunt = Shunts(1, 0, 19.0, 0, None, None, None, None, None, None, None)

        settings = Settings(debug=True, max_iters=30)

        Y = MatrixBuilder(settings)
        J = [0, 0]
        v_prev = [0.9819, -0.01673]

        shunt.stamp(Y, J, v_prev)

        matrix = Y.to_matrix().todense()

        print(matrix)
        print(J)

    def test_transformer(self):
        b1 = Bus(1, 1, 1, 0, None)
        b1.assign_nodes()
        b2 = Bus(2, 1, 1, 0, None)
        b2.assign_nodes()

        transformer = Transformers(1, 2, 1e-07, 0.20912, None, 0.978, 0.0, None, None, None)
        transformer.assign_nodes()

        settings = Settings(debug=True, max_iters=30)

        Y = MatrixBuilder(settings)
        J = [0, 0]
        v_prev = None

        transformer.stamp(Y, J, v_prev)

        matrix = Y.to_matrix().todense()

        print(matrix)
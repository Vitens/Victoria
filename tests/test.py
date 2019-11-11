import unittest
from epyphreeqc import EpyPhreeqc
from epynet import Network
from phreeqpython import PhreeqPython

pp = PhreeqPython()


class TestFlows(unittest.TestCase):
    # Test volumetric flows of the pipes

    def setUp(self):
        # PHREEQC solutions
        sol_list = {}
        sol0 = pp.add_solution({'pH': 7})
        sol_list[0] = sol0
        # Network node 1
        sol1 = pp.add_solution({'pH': 5})
        sol_list[1] = sol1
        # Network node 7
        sol2 = pp.add_solution({'pH': 8})
        sol_list[2] = sol2
        self.run = EpyPhreeqc('demo2.inp', sol_list, pp)
        self.run.steady_state()

        self.flows = {}
        for link in self.run.solver.net.links:
            self.flows[link.uid] = self.run.solver.models.pipes[link.uid].output_state[0]['volume']

    def test_flow1(self):
        self.assertEqual(round(self.flows['1'], 2), 137.61)


if __name__ == '__main__':
    unittest.main()

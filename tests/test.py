import unittest
from victoria import Victoria
from epynet import Network
from phreeqpython import PhreeqPython


class Test_line_network(unittest.TestCase):
    # Test simple network consisting of 4 nodes in a line
    def setUp(self):
        # self.net = Network(inputfile="tests/Case1.inp")
        self.net = Network(inputfile="Case1.inp")
        self.pp = PhreeqPython()
        self.vic = Victoria(self.net, self.pp)
        self.solutions = {}
        sol0 = self.pp.add_solution({'Ca': 0, 'units': 'mmol/l'})
        sol1 = self.pp.add_solution({'Ca': 1, 'units': 'mmol/l'})
        self.solutions[0] = sol0
        self.solutions[self.net.reservoirs['1'].uid] = sol1

    def test1(self):
        models = self.vic.solver.models
        # Test node count
        self.assertEqual(len(self.net.nodes), len(models.nodes))
        # Test junction count
        self.assertEqual(len(self.net.junctions), len(models.junctions))
        # Test reservoir count
        self.assertEqual(len(self.net.reservoirs), len(models.reservoirs))
        # Test tank count
        self.assertEqual(len(self.net.tanks), len(models.tanks))
        # Test link count
        self.assertEqual(len(self.net.links), len(models.links))
        # Test pipe count
        self.assertEqual(len(self.net.pipes), len(models.pipes))
        # Test pump count
        self.assertEqual(len(self.net.pumps), len(models.pumps))
        # Test valve count
        self.assertEqual(len(self.net.valves), len(models.valves))

    def test2(self):
        # Fill the network with a standard solution
        self.net.solve()
        self.vic.fill_network(self.solutions, from_reservoir=False)
        # Test the initial concentrations of Ca
        self.assertEqual(self.vic.get_conc_pipe_avg(self.net.links['1'], 'Ca', 'mmol'), 0)
        self.assertEqual(self.vic.get_conc_pipe_avg(self.net.links['2'], 'Ca', 'mmol'), 0)
        self.assertEqual(self.vic.get_conc_pipe_avg(self.net.links['3'], 'Ca', 'mmol'), 0)
        self.assertEqual(self.vic.get_conc_pipe_avg(self.net.links['6'], 'Ca', 'mmol'), 0)

    def test3(self):
        # Fill the network with the initial reservoir solution
        self.net.solve()
        self.vic.fill_network(self.solutions, from_reservoir=True)
        # Test the initial concentrations of Ca
        self.assertAlmostEqual(self.vic.get_conc_pipe_avg(self.net.links['1'], 'Ca', 'mmol'), 1, 4)
        self.assertAlmostEqual(self.vic.get_conc_pipe_avg(self.net.links['2'], 'Ca', 'mmol'), 1, 4)
        self.assertAlmostEqual(self.vic.get_conc_pipe_avg(self.net.links['3'], 'Ca', 'mmol'), 1, 4)
        self.assertAlmostEqual(self.vic.get_conc_pipe_avg(self.net.links['6'], 'Ca', 'mmol'), 1, 4)

    def test4(self):
        # Test the residence time in the pipes. Each pipe has a residence time of 1000 seconds

        # Time parameters Victoria
        time_end = 2  # hours
        timestep_network = 60  # minutes
        timestep_victoria = 1  # second
        # Convert units to seconds
        time_end *= 3600
        timestep_network *= 60
        time_count = 0

        # Fill the network
        self.net.solve()  # Need to run Epynet for a single timestep
        self.vic.fill_network(self.solutions, from_reservoir=False)

        for t1 in range(0, time_end, timestep_network):
            self.net.solve(simtime=t1)
            self.vic.check_flow_direction()

            for t2 in range(0, timestep_network, timestep_victoria):
                self.vic.step(timestep_victoria, self.solutions)
                time_count += t2
                if time_count == 999:
                    node = self.vic.get_conc_node(self.net.nodes['2'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 0, 4)
                elif time_count == 1000:
                    node = self.vic.get_conc_node(self.net.nodes['2'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 1, 4)
                elif time_count == 1999:
                    node = self.vic.get_conc_node(self.net.nodes['3'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 0, 4)
                elif time_count == 2000:
                    node = self.vic.get_conc_node(self.net.nodes['3'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 1, 4)
                elif time_count == 2999:
                    node = self.vic.get_conc_node(self.net.nodes['4'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 0, 4)
                elif time_count == 3000:
                    node = self.vic.get_conc_node(self.net.nodes['4'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 1, 4)
                elif time_count == 3999:
                    node = self.vic.get_conc_node(self.net.nodes['6'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 0, 4)
                elif time_count == 4000:
                    node = self.vic.get_conc_node(self.net.nodes['6'], 'Ca', 'mmol')
                    self.assertAlmostEqual(node, 1, 4)


if __name__ == '__main__':
    unittest.main()

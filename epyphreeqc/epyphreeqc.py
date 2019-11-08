from solver import Solver
from water_quality import Water_quality


class EpyPhreeqc(object):

    def __init__(self, network, sol_list, pp):
        self.solver = Solver(network, sol_list, pp)
        self.quality = Water_quality(pp)
        self.output = []

    def run(self, network, sol_list, timestep):

        for t in range(0, 1, 1):
            print('COUNTER', t)
            self.solver.step(network, timestep, sol_list)

        # Timestep PHREEQC transport
        # How often quality at nodes is calculated

        for link in network.links:
            print('pipe', link.uid, self.solver.models.pipes[link.uid].state)

        self.quality.nodes(network, self.solver.models)
        self.quality.pipes(network, self.solver.models)

    def tempadadda(self):
        self.qw.quality_nodes(self.net, self.models)
        self.qw.quality_pipes(self.net, self.models)

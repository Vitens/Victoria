from .solver import Solver
from .quality import Quality


class Victoria(object):

    def __init__(self, network, pp):
        self.net = network
        self.solver = Solver(network)
        self.quality = Quality(pp, self.solver.models)
        self.output = []

    def step(self, timestep, input_sol):
        # Solve the volume fractions for the whole network for one timestep
        # Run trace starting at each reservoir node

        for emitter in self.net.reservoirs:
            self.solver.run_trace(emitter, timestep, input_sol)

        for link in self.net.links:
            self.solver.models.links[link.uid].ready = False

    def fill_network(self, input_sol, from_reservoir=True):
        # Fill the network with initial solution
        if from_reservoir:
            # Fill the whole network with reservoir solution, while
            # considering the mix ratio. Links not filled with run_trace
            # are filled with a standard solution
            for emitter in self.net.reservoirs:
                try:
                    self.solver.fill_network(emitter, input_sol)
                except KeyError:
                    print('No solution defined for reservoir', emitter)
                    raise
            # Construct set of links unfilled links
            link_list = [link for link in self.net.links]
            link_filled = self.solver.filled_links
            unfilled = set(link_list) - set(link_filled)
            # Fill links with standard solution
            try:
                for link in unfilled:
                    q = {}
                    q[input_sol[0]] = 1
                    self.solver.models.pipes[link.uid].fill(q)
            except KeyError:
                print('No initial solution defined for 0')
                raise
            # Reset ready state
            for link in self.net.links:
                self.solver.models.links[link.uid].ready = False

        else:
            # Fill the whole network with an initial solution
            try:
                for pipe in self.net.pipes:
                    q = {}
                    q[input_sol[0]] = 1
                    self.solver.models.pipes[pipe.uid].fill(q)
            except KeyError:
                print('No initial solution defined, solution for Key = 0')
                raise

    def check_flow_direction(self):
        self.solver.check_connections()

    def garbage_collect(self):
        self.registered_solutions = []
        pass

    def get_solution_node(self, node, element, units='mmol'):
        return self.quality.get_conc_node(node, element, units)

    def get_mixture_node(self, node):
        return self.quality.get_mixture_node(node)

    def get_solution_pipe(self, link, element, units='mmol'):
        return self.quality.get_conc_parcels(link, element, units)

    def get_mixture_pipe(self, link):
        return self.quality.get_parcels(link)

    def get_avg_solution_pipe(self, link, element, units='mmol'):
        return self.quality.get_avg_conc_pipe(link, element, units)

from .solver import Solver
from .quality import Quality

import datetime
import openpyxl
import os


class Victoria(object):

    def __init__(self, network, sol_dict, pp):
        self.net = network
        self.solver = Solver(network, sol_dict, pp)
        self.quality = Quality(pp, self.solver.models)
        self.output = []

    def fill_network(self):
        return

    def step(self, timestep, input_sol):
        # Solve the volume fractions for the whole network for one timestep
        # Run trace starting at each reservoir node

        for emitter in self.net.reservoirs:
            nodetype = 'emitter'
            self.solver.run_trace(emitter, nodetype, timestep, input_sol)

        for link in self.net.links:
            self.solver.models.pipes[link.uid].ready = False

    def check_flow_direction(self):
        self.solver.check_connections()

    def get_solution_node(self, node, element, units='mmol'):
        return self.quality.get_conc_node(node, element, units)

    def get_mixture_node(self, node):
        return self.quality.get_mixture_node(node)
                            
    def get_solution_pipe(self, link, element, units='mmol'):
        return self.quality.get_conc_parcels(link, element, units)
    
    def get_mixture_pipe(self, link):
        return self.quality.get_parcels(link)

from solver import Solver
from quality import Quality

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

    def get_solution_node(self, node):
        return self.quality.get_solution_node(node)
    
    def get_mixture_node(self, node):
        return self.quality.get_mixture_node(node)
    
    def get_parcels(self, link):
        return self.quality.get_parcels(link)
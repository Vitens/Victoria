from fifo import FIFO
from mix import MIX
import math


class Models(object):
    # Models class, which mainly calls the required model classes
    # Might be redundant

    def __init__(self, network, sol_list):
        self.nodes = {}
        self.pipes = {}
        self.load_pipes(network, sol_list)
        self.load_nodes(network, sol_list)

    def load_nodes(self, network, sol_list):
        for node in network.nodes:
            self.nodes[node.uid] = MIX(sol_list)

    def load_pipes(self, network, sol_list):
        for link in network.links:
            volume = 1/4 * math.pi * link.length * (link.diameter * 10**-3)**2
            self.pipes[link.uid] = FIFO(volume, sol_list)

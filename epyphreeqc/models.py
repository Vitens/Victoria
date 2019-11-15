from fifo import FIFO
from mix import MIX
import math


class Models(object):
    # Models class, which mainly calls the required model classes
    # Might be redundant

    def __init__(self, network, sol_dict):
        self.nodes = {}
        self.pipes = {}
        self.load_pipes(network, sol_dict)
        self.load_nodes(network, sol_dict)

    def load_nodes(self, network, sol_dict):
        for node in network.nodes:
            self.nodes[node.uid] = MIX(sol_dict)

    def load_pipes(self, network, sol_dict):
        for link in network.links:
            if link.link_type == 'pipe':
                volume = 1/4 * math.pi * link.length * (link.diameter * 10**-3)**2
                self.pipes[link.uid] = FIFO(volume, sol_dict)
            elif link.link_type == 'pump':
                volume = 0
                self.pipes[link.uid] = FIFO(volume, sol_dict)
            elif link.link_type == 'valve':
                volume = 0
                self.pipes[link.uid] = FIFO(volume, sol_dict)

from fifo import FIFO
from mix import MIX
from fifo import FIFO
import math

class Models(object):
    
    def __init__(self, network):
        self.nodes = {}
        self.pipes = {}
        self.load_pipes(network)
        self.load_nodes(network)
            
    def load_nodes(self, network):
        
        for node in network.nodes:
            self.nodes[node.uid] = MIX()
        
    def load_pipes(self, network):
        for link in network.links:
            volume = 1/4 * math.pi * link.length * (link.diameter * 10**-3)**2
            self.pipes[link.uid] = FIFO(volume)
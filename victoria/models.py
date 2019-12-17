from .fifo import FIFO, Pipe, Pump, Valve
from .mix import Junction, Reservoir, Tank_CSTR, Tank_FIFO, Tank_LIFO
from math import pi


class Models(object):
    # Models class

    def __init__(self, network):
        self.nodes = {}
        self.junctions = {}
        self.reservoirs = {}
        self.tanks = {}

        self.links = {}
        self.pipes = {}
        self.pumps = {}
        self.valves = {}

        self.load_links(network)
        self.load_nodes(network)

    def load_nodes(self, network):
        for junction in network.junctions:
            node = Junction()
            self.junctions[junction.uid] = node
            self.nodes[junction.uid] = node

        for reservoir in network.reservoirs:
            node = Reservoir()
            self.reservoirs[reservoir.uid] = node
            self.nodes[reservoir.uid] = node

        for tank in network.tanks:
            node = Tank_CSTR(tank.initvolume)
            # node = Tank_FIFO(tank.maxvolume)
            # node = Tank_LIFO(tank.volume)
            self.tanks[tank.uid] = node
            self.nodes[tank.uid] = node

    def load_links(self, network):
        for pipe in network.pipes:
            pipe_volume = 1/4 * pi * pipe.length * (
                    pipe.diameter * 10**-3)**2
            link = Pipe(volume=pipe_volume)
            self.pipes[pipe.uid] = link
            self.links[pipe.uid] = link

        for pump in network.pumps:
            link = Pump()
            self.pumps[pump.uid] = link
            self.links[pipe.uid] = link

        for valve in network.valves:
            link = Valve()
            self.valves[valve.uid] = link
            self.links[valve.uid] = link

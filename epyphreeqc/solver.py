from models import Models

class Solver(object):
    # Solves the main calculation loop for water quality.
    # requires a solved epynet network as input

    def __init__(self, network, sol_dict, pp):
        self.output = []
        self.sol_dict = sol_dict
        # Construct model
        self.models = Models(network, self.sol_dict)

    def step(self, network, timestep, sol_dict):
        # Solve the volume fractions for the whole network for one timestep
        # Run trace starting at each reservoir node

        for emitter in network.reservoirs:
            nodetype = 'emitter'
            self.run_trace(emitter, nodetype, timestep, sol_dict)

        for link in network.links:
            self.models.pipes[link.uid].ready = False

    def run_trace(self, startnode, node_type, timestep, sol_dict):

        dgt = 7
        # Check whether all upstream pipes are ready
        ready = all(list(self.models.pipes[link.uid].ready for link in startnode.upstream_links))
        if not ready:
            return

        # Check type of node
        if node_type == 'emitter':
            shift_volume = timestep * startnode.outflow/60
            self.models.nodes[startnode.uid].emitter(startnode, shift_volume, sol_dict)

        if node_type == 'junction':
            # Collect all parcels flowing into the node
            inflow = []
            for link in startnode.upstream_links:
                inflow += self.models.pipes[link.uid].output_state
            # Mix the parcels at the node
            demand = round(startnode.demand/60 * timestep, dgt)  # Adjust demand to m3/minute
            self.models.nodes[startnode.uid].mix(inflow, demand)
            # Assign downstream outflow matrix
            outflow = [abs(link.flow) for link in startnode.downstream_links]
            # Calculate the parcel size flowing to the downstream pipes
            self.models.nodes[startnode.uid].parcels_out(outflow)

        self.models.nodes[startnode.uid].flowcount = 0

        for link in startnode.downstream_links:

            if abs(link.flow)/60*timestep <= 1E-6:
                self.models.pipes[link.uid].ready = True
                self.models.nodes[startnode.uid].flowcount += 1
                continue

            else:
                flow_cnt = self.models.nodes[startnode.uid].flowcount
                flow_in = round(abs(link.flow)/60 * timestep, dgt)

                if link.link_type == 'pipe':
                    # Push the parcels in the pipe and pull them
                    self.models.pipes[link.uid].push_pull_v2(flow_in, self.models.nodes[startnode.uid].outflow[flow_cnt])

                elif link.link_type == 'pump' or link.link_type == 'valve':
                    # Push the parcels instantly through the pump/valve
                    self.models.pipes[link.uid].pump_valve(flow_in, self.models.nodes[startnode.uid].outflow[flow_cnt])

                self.models.pipes[link.uid].ready = True
                # Run trace from downstream node
                self.models.nodes[startnode.uid].flowcount += 1
                self.run_trace(link.downstream_node, 'junction', timestep, sol_dict)

    def check_connections(self, network):
        # Check whether the flow direction of a pipe has shifted.
        for link in network.links:
            if (link.upstream_node == self.models.pipes[link.uid].upstream_node and
               link.downstream_node == self.models.pipes[link.uid].downstream_node):
                continue
            else:
                self.models.pipes[link.uid].reverse_parcels(link.downstream_node, link.upstream_node)

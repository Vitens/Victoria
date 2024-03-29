class Solver(object):
    # Solves the main calculation loop for water quality.
    # requires a solved epynet network as input

    def __init__(self, models, network):
        self.output = []
        self.net = network
        # Construct model
        self.models = models
        self.filled_links = []

    def run_trace(self, node, timestep, input_sol):
        # Main solver method
        dgt = 7
        # Check whether all upstream pipes are ready
        ready = all(list(self.models.links[link.uid].ready for link in
                    node.upstream_links))
        if not ready:
            return

        # Gather all parcels from upstream links
        inflow = []
        for link in node.upstream_links:
            inflow += self.models.links[link.uid].output_state

        # Mix parcels from upstream links at node
        self.models.nodes[node.uid].mix(inflow, node, timestep, input_sol)

        self.models.nodes[node.uid].flowcount = 0

        for link in node.downstream_links:
            if link.velocity < 0.001:
                return
            flow_cnt = self.models.nodes[node.uid].flowcount
            flow_in = round(abs(link.flow)/3600 * timestep, dgt)
            # Push and Pull parcels into and from the downstream link
            self.models.links[link.uid].push_pull(flow_in, self.models.nodes[node.uid].outflow[flow_cnt])

            self.models.links[link.uid].ready = True
            # Run trace from downstream node
            self.models.nodes[node.uid].flowcount += 1
            self.run_trace(link.downstream_node, timestep, input_sol)

    def check_connections(self):
        # Check whether the flow direction of a pipe has shifted.
        for link in self.net.links:
            if (link.upstream_node == self.models.links[link.uid].upstream_node and
               link.downstream_node == self.models.links[link.uid].downstream_node):
                continue
            else:
                self.models.links[link.uid].reverse_parcels(link.downstream_node,
                                                            link.upstream_node)

    def fill_network(self, node, input_sol):
        # Run trace method for filling the whole network
        # Check whether all upstream pipes are ready

        ready = all(list(self.models.links[link.uid].ready for link in node.upstream_links))
        if not ready:
            return

        inflow = []
        for link in node.upstream_links:
            inflow += self.models.links[link.uid].output_state

        timestep = 60
        self.models.nodes[node.uid].mix(inflow, node, timestep, input_sol)

        for link in node.downstream_links:
            sol = self.models.nodes[node.uid].outflow[0][0][1]
            self.models.links[link.uid].fill(sol)
            self.models.links[link.uid].ready = True
            # Run trace from downstream node
            self.filled_links.append(link)

            self.fill_network(link.downstream_node, input_sol)

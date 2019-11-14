

class Water_quality(object):
    # Calculates the water at nodes and pipes by first mixing respective
    # PHREEQC solutions and retrieving the desired values when called for

    def __init__(self, pp):
        self.mixture = []
        self.pp = pp

    def nodes(self, network, models):
        # Calculates the quality of the water in each node in the network
        self.q_nodes = {}

        for node in network.nodes:
            output_temp = []

            for parcel in models.nodes[node.uid].mixed_parcels:
                mix_temp = {}

                # Make dict entry for each phreeqc solutions with its
                # respective volume fraction
                for sol in parcel['q']:
                    mix_temp[sol] = parcel['q'][sol]

                # Calculate the phreeqc solution mixture and store it
                output_temp.append({
                    'x0': parcel['x0'],
                    'x1': parcel['x1'],
                    'q': self.pp.mix_solutions(mix_temp),
                    'volume': parcel['volume']
                    })
            self.q_nodes[node.uid] = output_temp

    def pipes(self, network, models):
        # Calculates the quality of the water of each parcel in the network.
        self.q_pipes = {}

        for link in network.links:
            output_temp = []

            for parcel in models.pipes[link.uid].state:
                mix_temp = {}

                # Make dict entry for each phreeqc solutions with its
                # respective volume fraction
                for sol in parcel['q']:
                    mix_temp[sol] = parcel['q'][sol]

                # Calculate the phreeqc solution mixture and store it
                output_temp.append({
                    'x0': parcel['x0'],
                    'x1': parcel['x1'],
                    'q': self.pp.mix_solutions(mix_temp)
                    })
            self.q_pipes[link.uid] = output_temp

    def get_quality_nodes(self, network, species, unit):
        # Returns the species concentration in the requested units
        output = {}
        for node in network.nodes:
            # Only requests the first parcel of the list. This parcel is at the node
            # at the requested moment
            parcel = self.q_nodes[node.uid][0]
            output[node.uid] = ({
                    'species': species,
                    'q': parcel['q'].total(species, unit),
                    'units': unit
                    })


            #for parcel in self.q_nodes[node.uid]:
                #output_temp.append({
                    #'x0': parcel['x0'],
                    #'x1': parcel['x1'],
                    #'species': species,
                    #'q': parcel['q'].total(species, unit),
                    #'units': unit,
                    #'volume': parcel['volume']
                    #})
            #output[node.uid] = output_temp
        return output

    def get_quality_pipes(self, network, species, unit):
        # Returns the species concentration in the requested units
        output = {}
        for link in network.links:
            output_temp = []
            for parcel in self.q_pipes[link.uid]:
                output_temp.append({
                    'x0': parcel['x0'],
                    'x1': parcel['x1'],
                    'species': species,
                    'q': parcel['q'].total(species, unit),
                    'units': unit
                    })
            output[link.uid] = output_temp
        return output

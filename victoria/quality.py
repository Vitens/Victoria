

class Quality(object):
    # Calculates the water at nodes and pipes by first mixing respective
    # PHREEQC solutions and retrieving the desired values when called for

    def __init__(self, pp, models):
        self.mixture = []
        self.q_nodes = {}
        self.models = models
        self.pp = pp

    def get_conc_node(self, node, element, units):

        if not self.models.nodes[node.uid].mixed_parcels:
            return 0

        parcel = self.models.nodes[node.uid].mixed_parcels[0]
        mix_temp = {}
        for sol in parcel['q']:
            mix_temp[sol] = parcel['q'][sol]

        # Calculate the phreeqc solution mixture
        mixture = self.pp.mix_solutions(mix_temp)

        return mixture.total(element, units)

    def get_mixture_node(self, node):

        if not self.models.nodes[node.uid].mixed_parcels:
            return 0

        return self.models.nodes[node.uid].mixed_parcels[0]['q']

    def get_conc_parcels(self, link, element, units):

        if not self.models.pipes[link.uid].state:
            return 0

        output = []
        for parcel in self.models.pipes[link.uid].state:
            mix_temp = {}

            # Make dict entry for each phreeqc solutions with its
            # respective volume fraction
            for sol in parcel['q']:
                mix_temp[sol] = parcel['q'][sol]

            # Calculate the phreeqc solution mixture and store it
            mixture = self.pp.mix_solutions(mix_temp)

            output.append({
                    'x0': parcel['x0'],
                    'x1': parcel['x1'],
                    'species': element,
                    'q': mixture.total(element, units),
                    'units': units
                    })
        return output

    def get_parcels(self, link):
        return self.models.pipes[link.uid].state

    def get_avg_conc_pipe(self, link, element, units):
        if not self.models.pipes[link.uid].state:
            return 0

        average_conc = 0
        
        for parcel in self.models.pipes[link.uid].state:
            mix_temp = {}
            for sol in parcel['q']:
                mix_temp[sol] = parcel['q'][sol]

            # Calculate the phreeqc solution mixture and store it
            vol_frac = parcel['x1'] - parcel['x0']
            mixture = self.pp.mix_solutions(mix_temp)
            average_conc += mixture.total(element, units)*vol_frac
            
        return average_conc



class Quality(object):
    # Calculates the water at nodes and pipes by first mixing respective
    # PHREEQC solutions and retrieving the desired values when called for

    def __init__(self, pp, models):
        self.mixture = []
        self.q_nodes = {}
        self.models = models
        self.pp = pp

    def get_parcels(self, link):
        # Return the parcels in a pipe
        return self.models.pipes[link.uid].state

    def get_conc_node(self, node, element, units):
        # Calculate the concentration of desired species exiting the node
        # at this exact moment
        if not self.models.nodes[node.uid].mixed_parcels:
            return 0

        parcel = self.models.nodes[node.uid].mixed_parcels[0]
        mix_temp = {}
        for sol in parcel['q']:
            phreeqc_sol = self.pp.get_solution(sol)
            mix_temp[phreeqc_sol] = parcel['q'][sol]
        # Calculate the phreeqc solution mixture
        mixture = self.pp.mix_solutions(mix_temp)

        return mixture.total(element, units)

    def get_conc_node_avg(self, node, element, units):
        # Calculate the average concentration of a species exitting
        # the node during the last timestep
        if not self.models.nodes[node.uid].mixed_parcels:
            return 0

        mixture = 0
        for parcel in self.models.nodes[node.uid].mixed_parcels:
            mix_temp = {}
            for sol in parcel['q']:
                phreeqc_sol = self.pp.get_solution(sol)
                mix_temp[phreeqc_sol] = parcel['q'][sol]
            parcel_mix = self.pp.mix_solutions(mix_temp)
            conc = parcel_mix.total(element, units)
            mixture += conc * (parcel['x1']-parcel['x0'])

        return mixture

    def get_mixture_node(self, node):
        # Return the PHREEQC solution number with its respective
        # volume fraction
        if not self.models.nodes[node.uid].mixed_parcels:
            return 0

        return self.models.nodes[node.uid].mixed_parcels[0]['q']

    def get_mixture_node_avg(self, node):
        # Return the PHREEQC solution number with its respective
        # volume fraction averaged over the last timestep
        if not self.models.nodes[node.uid].mixed_parcels:
            return 0
        merge_load = self.models.nodes['1'].merge_load

        average_dict = {}
        for parcel in self.models.nodes[node.uid].mixed_parcels:
            frac = parcel['x1'] - parcel['x-']
            average_dict = merge_load(average_dict, parcel['q'], frac)

        return average_dict

    def get_conc_pipe(self, link, element, units):
        # Calculate the concentration of the element in each parcel in a pipe
        if not self.models.links[link.uid].state:
            return 0

        pipe_conc = []
        for parcel in self.models.links[link.uid].state:
            mix_temp = {}
            for sol in parcel['q']:
                phreeqc_sol = self.pp.get_solution(sol)
                mix_temp[phreeqc_sol] = parcel['q'][sol]
            parcel_mix = self.pp.mix_solutions(mix_temp)
            conc = parcel_mix.total(element, units)
            pipe_conc.append({
                'x0': parcel['x0'],
                'x1': parcel['x1'],
                'q': conc
            })

        return pipe_conc

    def get_conc_pipe_avg(self, link, element, units):
        # Calculate the average concentration of an element over the whole pipe
        if not self.models.pipes[link.uid].state:
            return 0

        average_conc = 0

        for parcel in self.models.pipes[link.uid].state:
            mix_temp = {}
            for sol in parcel['q']:
                phreeqc_sol = self.pp.get_solution(sol)
                mix_temp[phreeqc_sol] = parcel['q'][sol]

            # Calculate the phreeqc solution mixture and store it
            vol_frac = parcel['x1'] - parcel['x0']
            mixture = self.pp.mix_solutions(mix_temp)
            average_conc += mixture.total(element, units)*vol_frac

        return average_conc

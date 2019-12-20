import numpy as np
import pandas as pd
from math import exp


class MIX(object):
    # Class for mixing pipes at nodes, -> mixing parcels at nodes
    def __init__(self):
        self.sorted_parcels = []
        self.outflow = []
        self.mixed_parcels = []

    def merge_load(self, dict1, dict2, volume):
        # Function for mixing PHREEQC solutions at nodes
        dict3 = {**dict1, **dict2}

        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = value * volume + dict1[key]
            if key not in dict1 and key in dict2:
                dict3[key] = value * volume
        return dict3

    def parcels_out(self, flows_out):
        # Assigns parcels flowing out to the appropiate pipe
        self.outflow = []
        output = []
        total_flow = sum(flows_out)
        if total_flow <= 1E-7:
            return

        for flow in flows_out:
            temp = []
            for parcel in self.mixed_parcels:
                parcel_volume = ((parcel['x1']-parcel['x0']) *
                                 flow/total_flow*parcel['volume'])
                parcel_volume = round(parcel_volume, 6)
                temp.append([parcel_volume, parcel['q']])
            output.append(temp)
        self.outflow = output


class Junction(MIX):
    # Junction MIX subclass
    def mix(self, inflow, node, timestep, input_sol):
        # Main function for mixing parcels at nodes
        xcure = 0
        self.mixed_parcels = []
        demand = round(node.demand/3600 * timestep, 7)

        # Sort parcels along their x1 coordinate
        self.sorted_parcels = sorted(inflow, key=lambda a: a['x1'])
        # Mix parcels with overlapping coordinates
        for parcel1 in self.sorted_parcels:
            if parcel1['x1'] <= xcure:
                continue

            mixture = {}
            total_volume = 0
            cell_volume = 0
            for parcel2 in self.sorted_parcels:
                if parcel2['x1'] <= xcure:
                    continue
                if parcel2['x0'] >= parcel1['x1']:
                    continue

                total_volume += parcel2['volume']

                # Calculate volume fraction * volume of each pipe
                rv = (parcel1['x1']-xcure) * parcel2['volume']
                # Calculate mixture
                mixture = super().merge_load(mixture, parcel2['q'], rv)
                cell_volume += rv
            # Adjust the volume fraction with the total volume of the
            # mixed parcel
            for charge in mixture:
                mixture[charge] = round(mixture[charge] / cell_volume, 3)
            total_volume -= demand

            self.mixed_parcels.append({
                'x0': xcure,
                'x1': parcel1['x1'],
                'q': mixture,
                'volume': total_volume
            })

            xcure = parcel1['x1']

        flows_out = [abs(link.flow) for link in node.downstream_links]
        super().parcels_out(flows_out)


class Reservoir(MIX):
    # Reservoir MIX subclass
    def mix(self, inflow, node, timestep, input_sol):
        # Special function for when the node is an emitter, source of PHREEQC
        # solutions flowing through the network
        self.mixed_parcels = []

        q = {}
        q[input_sol[node.uid].number] = 1
        shift_volume = timestep * node.outflow/3600

        # Required for the model
        self.outflow = [[[shift_volume, q]]]

        # For easier access later.
        self.mixed_parcels.append({
                'x0': 0,
                'x1': 1,
                'q': self.outflow[0][0][1],
                'volume': shift_volume
                })


class Tank_CSTR(MIX):
    # CSTR Tank MIX subclass
    # Ideal and instanteneous mixing is assumed in the tank
    def __init__(self, initvolume):
        self.volume = initvolume
        self.mixture = {}
        self.mixed_parcels = []

    def mix(self, inflow, node, timestep, input_sol):

        volume_tank = node.volume

        flows_out = [abs(link.flow) for link in node.downstream_links]

        self.mixed_parcels = []
        mixture = {}
        total_volume = 0

        # Calculate the mixture of all parcels flowing into the tank:
        for parcel in inflow:
            rv = (parcel['x1']-parcel['x0']) * parcel['volume']
            mixture = super().merge_load(mixture, parcel['q'], rv)
            total_volume += rv
        for charge in mixture:
            mixture[charge] = round(mixture[charge] / total_volume, 4)

        # Determine fraction of inflow solution in the tank mixture solution
        frac = (1 - exp(-(total_volume/volume_tank)))

        volume_out = node.outflow/3600*timestep

        # Mix the PHREEQC solution mixture from the inflow with the mixture
        # already present in the tank
        new_solution = {}
        new_solution = super().merge_load(new_solution, mixture, frac)
        new_solution = super().merge_load(new_solution, self.mixture, 1-frac)

        # For the outflow solution mixture an average between the old and
        # updated value is used
        solution_out = {}
        solution_out = super().merge_load(solution_out, self.mixture, 0.5)
        solution_out = super().merge_load(solution_out, new_solution, 0.5)

        self.mixed_parcels.append({
            'x0': 0,
            'x1': 1,
            'q': solution_out,
            'volume': volume_out
        })

        self.mixture = new_solution

        flows_out = [abs(link.flow) for link in node.downstream_links]
        super().parcels_out(flows_out)


class Tank_LIFO(MIX):
    # LIFO Tank MIX subclass
    # Parcels inside tank are stored on Last In First Out principle
    # parcel position is relative to the max tank volume
    def __init__(self, maxvolume):
        self.maxvolume = maxvolume
        self.state = []
        self.mixed_parcels = []

    def mix(self, inflow, node, timestep, input_sol):

        if not node.downstream_links:
            # If no downstream links, the tank must be in the filling state
            for parcel in inflow:
                volume = (parcel['x1']-parcel['x0']) * parcel['volume']
                shift = volume / self.maxvolume

                self.state = [{'x0': s['x0']+shift,
                               'x1':s['x1']+shift, 'q':s['q']}
                              for s in self.state]
                # Only form new parcels if previous parcel is not identical
                new_state = []
                if parcel['q'] == self.state[0]['q']:
                    self.state['x0'] = 0
                else:
                    x0 = 0
                    x1 = x0 + shift
                    new_state.append({
                        'x0': x0,
                        'x1': x1,
                        'q': parcel['q']
                    })
                self.state = new_state + self.state

        elif sum(node.downstream_links.flow) > 0:
            # If the tank is emptying
            # Determine the total volume all pipes exiting the tank
            flows_out = [abs(link.flow) for link in node.downstream_links]
            vol_out = sum(flows_out)*3600*timestep
            shift = vol_out/self.maxvolume
            # Update the position of each parcel
            self.state = [{'x0': s['x0']-shift,
                           'x1':s['x1']-shift, 'q':s['q']} for s in self.state]

            xcure = 1
            for parcel in self.state:
                vol = abs(parcel['x0']) * self.maxvolume if x1 > 0 \
                        else (x1 - x0) * self.maxvolume
                excess = vol/vol_out
                if parcel['x0'] < 0:
                    x0 = xcure - excess
                    self.mixed_parcels.append({
                        'x0': x0,
                        'x1': xcure,
                        'q': parcel['q'],
                        'volume': vol_out
                    })
                    xcure = x0
                    if parcel['x1'] > 0:
                        parcel['x0'] = 0
                        new_state.append(parcel)
                else:
                    new_state.append(parcel)
            super().parcels_out(flows_out)


class Tank_FIFO(MIX):
    # FIFO Tank MIX subclass
    # Parcels in the tank are stored on First In First Out principle
    # the parcel position is relative to the max tank volume
    def __init__(self, volume):
        self.volume = volume
        self.volume_prev = volume
        self.state = []
        self.mixed_parcels = []

    def mix(self, inflow, node, timestep, input_sol):
        for parcel in inflow:
            # Determine correction factor for change in total volume
            factor = self.volume_prev / self.volume

            # Calculate the shift in parcel position relative to the changed
            # volume
            volume = (parcel['x1']-parcel['x0']) * parcel['volume']
            shift = volume / self.volume

            self.state = [{'x0': s['x0']*factor+shift,
                           'x1':s['x1']*factor+shift,
                           'q':s['q']}
                          for s in self.state]

            # Only form new parcels if previous parcel is not identical
            new_state = []
            if parcel['q'] == self.state[0]['q']:
                self.state['x0'] = 0
            else:
                x1 = 0
                x0 = x1 + shift
                new_state.append({
                    'x0': x0,
                    'x1': x1,
                    'q': parcel['q']
                })
            self.state = new_state + self.state

            self.volume_prev = self.volume

        # Determine the total volume all pipes exiting the tank
        new_state = []
        output = []
        flows_out = [abs(link.flow) for link in node.downstream_links]
        vol_out = sum(flows_out)*3600*timestep
        x0 = 0
        for parcel in self.state:
            vol = (x1 - 1) * self.volume if x0 < 1 else (x1 - x0) * self.volume
            if parcel['x1'] > 1:
                x1 = x0 + vol/vol_out
                output.append({
                    'x0': x0,
                    'x1': x1,
                    'q': parcel['q'],
                    'volume': vol_out
                })
                if parcel['x0'] < 1:
                    parcel['x1'] = 1
                    new_state.append(parcel)
                x0 = x1
            else:
                new_state.append(parcel)

        self.mixed_parcels = output
        self.state = new_state

        super().parcels_out(flows_out)

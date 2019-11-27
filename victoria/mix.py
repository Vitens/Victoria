import numpy as np
import pandas as pd


class MIX(object):
    # Class for mixing pipes at nodes, -> mixing parcels at nodes
    def __init__(self):
        self.sorted_parcels = []
        self.outflow = []
        self.mixed_parcels = []
        self.flowcount = []

    def reset_outflow(self):
        self.outflow = []

    def merge_load(self, dict1, dict2, volume):
        # Function for mixing PHREEQC solutions at nodes
        dict3 = {**dict1, **dict2}

        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = value * volume + dict1[key]
            if key not in dict1 and key in dict2:
                dict3[key] = value * volume
        return dict3

    def mix(self, inflow, demand):
        # Main function for mixing parcels at nodes
        xcure = 0
        self.mixed_parcels = []
        # Sort parcels along their x1 coordinate
        self.sorted_parcels = sorted(inflow, key=lambda a: a['x1'])
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
                mixture = self.merge_load(mixture, parcel2['q'], rv)
                cell_volume += rv

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

    def parcels_out(self, flows_out):
        # Assigns parcels flowing out to the correct downstream pipe
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

    def emitter(self, node, shift_volume, input_sol):
        # Special function for when the node is an emitter, source of PHREEQC
        # solutions flowing through the network
        self.mixed_parcels = []

        q = {}
        q[input_sol[node.uid]] = 1

        # Required for the model
        self.outflow = [[[shift_volume, q]]]

        # For easier access later.
        self.mixed_parcels.append({
                'x0': 0,
                'x1': 1,
                'q': self.outflow[0][0][1],
                'volume': shift_volume
                })
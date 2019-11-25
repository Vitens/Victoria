import numpy as np
import pandas as pd


class FIFO(object):
    # Class for pipes, which contain segregated parcels.

    def __init__(self, volume, sol_dict):
        self.volume = volume
        self.state = [{'x0': 0, 'x1': 1, 'q': {sol_dict[0]: 1}}]
        self.output = []
        self.ready = False
        self.output_state = []
        self.downstream_node = []
        self.upstream_node = []

    def connections(self, downstream, upstream):

        self.downstream_node = downstream
        self.upstream_node = upstream

    def push_pull(self, volumes):

        # Push part of function
        # Calculate total volume of pushed section
        total_volume = sum([v[0] for v in volumes])
        fraction = total_volume / self.volume

        # Shift fractions in current state
        self.state = [{'x0': s['x0']+fraction,
                      'x1':s['x1']+fraction, 'q':s['q']} for s in self.state]

        # Convert input volumes
        x0 = 0
        new_state = []

        for (v, q) in volumes:
            x1 = x0 + v / self.volume
            new_state.append({
                'x0': x0,
                'x1': x1,
                'q': q
            })
            x0 = x1

        self.state = new_state + self.state
        # Pull part of function
        new_state = []
        output = []
        output_state = []

        for parcel in self.state:
            # Need to round 10th decimal in order to
            # prevent the creation of "ghost volumes"
            parcel['x0'] = round(parcel['x0'], 10)
            parcel['x1'] = round(parcel['x1'], 10)

            x0 = parcel['x0']
            x1 = parcel['x1']

            vol = (x1 - 1) * self.volume if x0 < 1 else (x1 - x0) * self.volume
            if x1 > 1:
                output.append([vol, parcel['q']])
                if x0 < 1:
                    parcel['x1'] = 1
                    new_state.append(parcel)
            else:
                new_state.append(parcel)

        volume = sum([v[0] for v in output])
        x0 = 0

        for (v, q) in output:
            x1 = x0 + v / volume
            output_state.append({
                'x0': x0,
                'x1': x1,
                'q': q,
                'volume': volume
            })
            x0 = x1
        self.state = new_state
        self.output_state = output_state
        self.ready = True

    def merge_parcels(self):
        new_state = []
        for parcel1 in self.state:
            for parcel2 in self.state:
                if parcel1['x1'] == parcel2['x0'] and (parcel1['q'] == parcel2['q']):
                    new_state.append({
                        'x0': parcel1['x0'],
                        'x1': parcel2['x1'],
                        'q': parcel1['q']
                        })
                    self.state.remove(parcel1)
                    self.state.remove(parcel2)
                    self.state = new_state + self.state
                    self.state = sorted(self.state, key=lambda a: a['x1'])
                    self.merge_parcels()

    def reverse_parcels(self, downstream, upstream):
        # Reverse the parcels incase the flow switches around and
        # store the new down- and upstream nodes
        temp_state = []
        for parcel in self.state:
            x0_temp = abs(1-parcel['x1'])
            x1_temp = abs(1-parcel['x0'])

            temp_state.append({
                'x0': x0_temp,
                'x1': x1_temp,
                'q': parcel['q']
            })

        self.state = sorted(temp_state, key=lambda a: a['x1'])
        self.downstream_node = downstream
        self.upstream_node = upstream

    def pump_valve(self, flow, volumes):
        # Special function for link_type: 'pump' and 'valve'
        # Pump and Valve do not have a length so NO residence time

        total_volume = sum([v[0] for v in volumes])

        vol_updated = []
        for (v, q) in volumes:

            vol = v / total_volume * flow
            vol_updated.append([vol, q])

        x0 = 0
        output_state = []

        for (v, q) in volumes:
            x1 = x0 + v / total_volume
            output_state.append({
                'x0': x0,
                'x1': x1,
                'q': q,
                'volume': flow
            })
            x0 = x1

        self.output_state = output_state

    def push_pull_v2(self, flow, volumes):

        # Push part of function
        # Calls recursive function
        total_volume = sum([v[0] for v in volumes])
        vol_updated = []

        for (v, q) in volumes:

            vol = v / total_volume * flow
            vol_updated.append([vol, q])

        self.push_in(vol_updated)

        # Pull part of function
        new_state = []
        output = []
        output_state = []

        for parcel in self.state:
            # Need to round 10th decimal in order to
            # prevent the creation of "ghost volumes"
            parcel['x0'] = round(parcel['x0'], 10)
            parcel['x1'] = round(parcel['x1'], 10)

            x0 = parcel['x0']
            x1 = parcel['x1']

            vol = (x1 - 1) * self.volume if x0 < 1 else (x1 - x0) * self.volume
            if x1 > 1:
                output.append([vol, parcel['q']])
                if x0 < 1:
                    parcel['x1'] = 1
                    new_state.append(parcel)
            else:
                new_state.append(parcel)

        volume = sum([v[0] for v in output])
        x0 = 0

        for (v, q) in output:
            x1 = x0 + v / volume
            output_state.append({
                'x0': x0,
                'x1': x1,
                'q': q,
                'volume': volume
            })
            x0 = x1
        self.state = new_state
        self.output_state = output_state
        self.ready = True

    def push_in(self, volumes):
        # Recursive function for pushing parcels into the pipe
        # Seems to be more stable
        if not volumes:
            return

        v = volumes[len(volumes)-1][0]
        q = volumes[len(volumes)-1][1]

        fraction = v/self.volume
        self.state = [{'x0': s['x0']+fraction,
                      'x1':s['x1']+fraction, 'q':s['q']} for s in self.state]
        x0 = 0

        new_state = []
        if q == self.state[0]['q']:
            self.state[0]['x0'] = 0

        else:
            x1 = x0 + v / self.volume
            new_state.append({
                'x0': x0,
                'x1': x1,
                'q': q
                })

        self.state = new_state + self.state

        volumes.remove([v, q])

        if not volumes:
            return
        else:
            self.push_in(volumes)

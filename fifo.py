import numpy as np
import pandas as pd

class FIFO(object):
    
    def __init__(self, volume):
        self.volume = volume
        self.state =  [{'x0':0, 'x1':1, 'q': pd.Series(np.zeros(6))}] 
        # Need to write a function to auto update the size of the PHREEQC solution matrix
        self.output = []
        self.ready = False 
        self.output_state = []
        self.state[0]['q'][0] = 1
        
    def reset_output(self):
        self.output_state = []
        self.ready = False
        
    def push_pull(self,volumes):
        
        # Push part of function
        # Calculate total volume of pushed section
        total_volume = sum([v[0] for v in volumes])
        fraction = total_volume / self.volume
        
        # Shift fractions in current state
        self.state = [{'x0':s['x0']+fraction, 'x1':s['x1']+fraction, 'q':s['q']} for s in self.state]
        
        # Convert input volumes
        x0 = 0 
        new_state = []
        
        for (v,q) in volumes:
            x1 = x0 + v / self.volume # 
            new_state.append({
                'x0': x0,
                'x1': x1,
                'q' : q
            })
            x0 = x1
         
        self.state = new_state + self.state
        # Pull part of function
        new_state = []
        output = []
        output_state = []
        
        for parcel in self.state:
            # Need to round 10th decimal in order to prevent the creation of "ghost volumes"
            parcel['x0'] = round(parcel['x0'],10)
            parcel['x1'] = round(parcel['x1'],10)
            
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
        
        for (v,q) in output:
            x1 = x0 + v / volume
            output_state.append({
                'x0': x0,
                'x1': x1,
                'q': q,
                'volume': volume
            })
            x0 = x1
        self.state = new_state
        self.output_state= output_state
        self.ready = True
    
    
    def merge_parcels(self):
        new_state = []
        for parcel1 in self.state:
            for parcel2 in self.state:
                if parcel1['x1'] == parcel2['x0'] and parcel1['q'].equals(parcel2['q']):
                    new_state.append({
                    'x0': parcel1['x0'],
                    'x1': parcel2['x1'],
                    'q': parcel1['q']
                    })  
                    self.state.remove(parcel1)
                    self.state.remove(parcel2)
                    self.state = new_state + self.state
                    self.merge_parcels()

        
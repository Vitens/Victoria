import numpy as np
import pandas as pd

class MIX(object):
    
    def __init__(self):
        self.sorted_parcels = []
        self.outflow = []
        
        
        
    def reset_outflow(self):
        self.outflow = []
    
    def mix(self, inflow, demand):
    
        xcure = 0
        count = 0
        self.mixed_parcels = []
        self.sorted_parcels = sorted(inflow, key=lambda a:a['x1'])
    
        for parcel1 in self.sorted_parcels:
            if parcel1['x1'] <= xcure:
                continue

            #mixture = pd.Series(np.zeros(len(self.sorted_parcels[0]['q'])))
            mixture = 0 
            
            total_volume = 0
            cell_volume= 0
            for parcel2 in self.sorted_parcels:
                if parcel2['x1'] <= xcure:
                    continue
                if parcel2['x0'] >= parcel1['x1']:
                    continue
                
                total_volume += parcel2['volume']
                
                # Calculate volume fraction * volume of each pipe
                rv =  (parcel1['x1']-xcure) * parcel2['volume']
                # Calculate mixture 
                mixture += parcel2['q'].multiply(rv)
                cell_volume += rv
    
            total_volume -= demand
            self.mixed_parcels.append({
                'x0': xcure,
                'x1': parcel1['x1'],
                'q': mixture.divide(cell_volume),
                'volume': total_volume
            })
            self.mixed_parcels[count]['q'] = self.mixed_parcels[count]['q'].round(10)
            xcure = parcel1['x1']
            count += 1
        
    def parcels_out(self, flows_out):
        self.outflow = []
        output = []
        total_flow = sum(flows_out)
        
        for flow in flows_out:
            temp = []
            for parcel in self.mixed_parcels:
                parcel_volume = (parcel['x1']-parcel['x0'])*flow/total_flow*parcel['volume']
                if parcel_volume < 1E-5:
                    continue
                else:
                    parcel_volume = round(parcel_volume,5)
                    temp.append([parcel_volume,parcel['q']])      
            output.append(temp)
        self.outflow = output
        
    def emitter(self, shift_volume):
        q= pd.DataFrame(np.zeros((6,6)))
        for i in range(6):
            q[i][i] = 1
        
        self.outflow = [[[shift_volume,q[1]]]]
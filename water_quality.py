

class Water_quality(object):
    ### WIP ###
    
    def __init__(self, pp):
        self.mixture = []
        self.pp = pp
    
    def quality_nodes(self, network, sol_list, models):
        # Calculates the quality of the water in each node in the network, excluding the reservoirs (boundary values anyway)
        self.q_nodes = {}
       
        for node in network.nodes:
            output_temp = []
                
            for parcel in models.nodes[node.uid].mixed_parcels:
                mix_temp = {}
                
                
                 # Make dict entry for phreeqc solutions with its respective volume fraction
                for i in sol_list:
                    mix_temp[sol_list[i]] = parcel['q'][i]    
                  
                #output_temp.append(pp.mix_solutions(mix_temp)) # Calculate the phreeqc solution mixture and store it 
                output_temp.append({
                'x0': parcel['x0'],
                'x1': parcel['x1'],
                'q': self.pp.mix_solutions(mix_temp),
                'volume': parcel['volume']
                })
            self.q_nodes[node.uid] = output_temp
                
        
    
    def quality_pipes(self, network, sol_list, models):
        # Calculates the quality of the water of each parcel in the network.
        self.q_pipes = {}
        
        for link in network.links:
            output_temp = []
           
            for parcel in models.pipes[link.uid].state:
                mix_temp = {}
                
                for i in sol_list:
                    mix_temp[sol_list[i]] = parcel['q'][i]
                    
                output_temp.append({
                'x0': parcel['x0'],
                'x1': parcel['x1'],
                'q': self.pp.mix_solutions(mix_temp)
                }) 
            self.q_pipes[link.uid] = output_temp
       

    
    
    def get_quality_nodes(self, network, species, unit):
        
        output = {}
        for node in network.nodes:
            output_temp = []
            for parcel in self.q_nodes[node.uid]:
                output_temp.append({
                'x0': parcel['x0'],
                'x1': parcel['x1'],
                'species': species,
                'q': parcel['q'].total(species,unit),
                'units': unit,
                'volume': parcel['volume']
                })
            output[node.uid] = output_temp
        return output
        

    def get_quality_pipes(self, network, species, unit):
        
        output = {}
        for link in network.links:
            output_temp =  []
            for parcel in self.q_pipes[link.uid]:
                output_temp.append({
                'x0': parcel['x0'],
                'x1': parcel['x1'],
                'species': species,
                'q': parcel['q'].total(species,unit),
                'units': unit
                })
            output[link.uid] = output_temp
        return output


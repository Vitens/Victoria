from models import Models
from epynet import Network
from water_quality import Water_quality

class Solver(object):
    
    def __init__(self, inputfile):
        self.net = Network(inputfile)
        self.output = []
        # Construct model
        self.models = Models(self.net)
        self.quality = Water_quality(self.net)
        
    def step(self, timestep):
        # Solve the volume fractions for the whole network for one timestep 
        # Loop over all nodes reservoir nodes
        for emitter in self.net.nodes[self.net.nodes.inflow==0]:
            nodetype = 'emitter'
            self.run_trace(emitter, nodetype, timestep)
        
        for link in self.net.links:
            self.models.pipes[link.uid[0]].ready = False
            
            
    def minor(self):
        # Solve the volume fractions for the whole network over multiple timesteps, hydraulic equations are only solved once
        self.net.solve()
        timestep = 1
        
        for t in range(0,10,1):
            print('COUNTER',t)
            self.step(timestep)
        
        for link in self.net.links:
            print('pipe', link.uid, self.models.pipes[link.uid].state)
        return
        
        
    def major(self):
        # Solve the hydraulic equations and volume fractions for the whole network over multiple timesteps
        return
    
    
    def run_trace(self, startnode, node_type, timestep):
        print(startnode)
        # Check whether all upstream pipes are ready
        ready = all(list(self.models.pipes[link.uid[0]].ready for link in startnode.upstream_links))
        if not ready:
            return
        
        # Check type of node 
        if node_type == 'emitter': 
            shift_volume = timestep * startnode.outflow
            self.models.nodes[startnode.uid].emitter(shift_volume)
            
        if node_type ==  'junction':
            # Collect all parcels flowing into the node
            inflow = []
            for link in startnode.upstream_links:
                inflow += self.models.pipes[link.uid[0]].output_state
            
            # Mix the parcels at the node 
            demand = startnode.demand * timestep
            self.models.nodes[startnode.uid].mix(inflow, demand)
            # Assign downstream outflow matrix 
            outflow = [abs(link.flow) for link in startnode.downstream_links]
            
            # Calculate the parcel size flowing to the downstream pipes
            self.models.nodes[startnode.uid].parcels_out(outflow)
            self.models.nodes[startnode.uid].outflow
        
        #self.models.nodes[startnode.uid].parcels_out()
        
        flowcount = 0
        
        for link in startnode.downstream_links:
            
            self.models.pipes[link.uid[0]].push_pull(self.models.nodes[startnode.uid].outflow[flowcount])
            self.models.pipes[link.uid[0]].merge_parcels()
            ## Run FIFO.push_pull()
            ## Run FIFO.merge_parcels()
            self.models.pipes[link.uid[0]].ready = True
            self.run_trace(link.downstream_node,'junction', timestep)
            flowcount += 1
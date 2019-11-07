from models import Models
from epynet import Network
from water_quality import Water_quality

class Solver(object):
    # Solves the main calculation loop, both the hydraulic equations (epynet) and water quality.  
    # 
    # Inputfile is an Epanet '.inp' file
    
    def __init__(self, inputfile, sol_list, pp):
        self.net = Network(inputfile)
        self.output = []
        self.sol_list = sol_list
        # Construct model
        self.models = Models(self.net, self.sol_list)
        self.qw = Water_quality(pp)
        
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
                
        self.qw.quality_nodes(self.net, self.sol_list, self.models)
        self.qw.quality_pipes(self.net, self.sol_list, self.models)
        
    def major(self):
        # Solve the hydraulic equations and volume fractions for the whole network over multiple timesteps
        return
    
    
    def run_trace(self, startnode, node_type, timestep):
        #print(startnode)
        # Check whether all upstream pipes are ready
        ready = all(list(self.models.pipes[link.uid[0]].ready for link in startnode.upstream_links))
        if not ready:
            return
        
        # Check type of node 
        if node_type == 'emitter': 
            shift_volume = timestep * startnode.outflow
            self.models.nodes[startnode.uid].emitter(startnode, shift_volume)
            
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
            
            # Push the parcels in the pipe and pull them
            self.models.pipes[link.uid[0]].push_pull(self.models.nodes[startnode.uid].outflow[flowcount])
            # Merge neighbouring parcels with identical PHREEQC solution matrix
            self.models.pipes[link.uid[0]].merge_parcels()
            # Update ready state of the pipe
            self.models.pipes[link.uid[0]].ready = True
            # Run trace from downstream node
            flowcount += 1
            self.run_trace(link.downstream_node,'junction', timestep)
            
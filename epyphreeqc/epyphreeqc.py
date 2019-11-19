from solver import Solver
from water_quality import Water_quality


class EpyPhreeqc(object):

    def __init__(self, network, sol_dict, pp):
        self.solver = Solver(network, sol_dict, pp)
        self.quality = Water_quality(pp)
        self.output = []

    def run(self, network, sol_dict, timestep,
            start_time, total_time, reporting_timestep):
        # Main calculation loop 

        self.output = []
        # Check the flow direction in each pipe
        self.solver.check_connections(network)

        for t in range(start_time, total_time, timestep):
            # Timestep in minutes
            self.solver.step(network, timestep, sol_dict)
            output_temp = []
            print('TIME',t)

            # Store output at reporting timestep 
            if t % reporting_timestep == 0:
                self.quality.nodes(network, self.solver.models)
                self.quality.pipes(network, self.solver.models)

                self.output.append(self.quality.get_quality_nodes(network,
                                   'Ca', 'mg'))

        return self.output

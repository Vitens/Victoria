from solver import Solver

class EpyPhreeqc(object):
    
    def __init__(self, inputfile, sol_list, pp):
        self.solver = Solver(inputfile, sol_list, pp)
        self.output = []
     
    def steady_state(self):
        self.solver.minor()
        
    def dynamic(self, timestep_epynet, timestep_phreeqc):
        self.solver.major
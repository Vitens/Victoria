from solver import Solver

class EpyPhreeqc(object):
    
    def __init__(self, inputfile):
        self.solver = Solver(inputfile)
        self.output = []
     
    def steady_state(self):
        self.solver.minor()
        
    def dynamic(self, timestep_epynet, timestep_phreeqc):
        self.solver.major
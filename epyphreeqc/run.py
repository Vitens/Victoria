from epyphreeqc import EpyPhreeqc
from phreeqpython import PhreeqPython
from epynet import Network

pp = PhreeqPython()
# File for quickly testing the code, will be redundant in the future
# PHREEQC SOLUTION INPUT #####

sol_list = {}

sol0 = pp.add_solution({
    'pH': 7,
    'Ca': 120,
    'Mg': 5,
    'Na': 40,
    'Cl': 16,
    'units': 'mg/l',
    'Alkalinity': '5 as CO2'
})
sol_list[0] = sol0

# Network node 1
sol1 = pp.add_solution({
    'pH': 5,
    'Ca': 120,
    'Mg': 5,
    'Na': 40,
    'Cl': 16,
    'units': 'mg/l',
    'Alkalinity': '5 as CO2'
})
sol_list[1] = sol1

# Network node 7
sol2 = pp.add_solution({
    'pH': 8,
    'Ca': 120,
    'Mg': 5,
    'Na': 40,
    'Cl': 16,
    'units': 'mg/l',
    'Alkalinity': '5 as CO3'
})
sol_list[2] = sol2

network = Network('demo2.inp')
network.solve()
timestep = 1

run = EpyPhreeqc(network, sol_list, pp)
run.run(network, sol_list, timestep)

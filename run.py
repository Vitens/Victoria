from epyphreeqc import EpyPhreeqc
from phreeqpython import PhreeqPython

pp = PhreeqPython()
##### PHREEQC SOLUTION INPUT #####

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

run = EpyPhreeqc('demo2.inp',sol_list, pp)
run.steady_state()
print(run.solver.models.pipes[run.solver.net.links['1'].uid[0]].output_state[0])

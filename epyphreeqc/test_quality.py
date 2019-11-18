from epyphreeqc import EpyPhreeqc
from phreeqpython import PhreeqPython
from epynet import Network
import matplotlib.pyplot as plt

# TIME INPUT PARAMETERS
timestep = 1  # minutes,  timestep for solving PHREEQC
time_end = 3  # hours,   maximum duration of the simulation
time_report = 1  # minutes  timestep for reporting the result
time_start = 0  # Start time

# Convert input to minutes
time_end = time_end * 60

# Initialize Epynet
network1 = Network('quality1.inp')
# Initialize PhreeqPython and set a initial phreeqc solution
pp = PhreeqPython()
solutions = {}
sol0 = pp.add_solution({
    'Ca': 0,
    'units': 'mg/l'
})
solutions[0] = sol0

# Initialize EpyPhreeqc
run_quality = EpyPhreeqc(network1, solutions, pp)
# Initialize Phreeqpython for the reservoirs
sol1 = pp.add_solution({
    'Ca': 1,
    'units': 'mg/l'
})

sol7 = pp.add_solution({
    'Ca': 0.5,
    'units': 'mg/l'
})
solutions[network1.reservoirs['1'].uid] = sol1


# Solve the Epynet network
network1.solve()
# Solve the quality of the system
conc = run_quality.run(network1, solutions, timestep, time_start, time_end, time_report)

t = [tt/60 for tt in range(0, time_end, time_report)]
Ca2 = [x['2']['q'] for x in conc]
Ca3 = [x['3']['q'] for x in conc]
Ca4 = [x['4']['q'] for x in conc]

plt.plot(t, Ca2)
plt.plot(t, Ca3)
plt.plot(t, Ca4)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration of Ca [mg/l]')
plt.legend(['Node 2', 'Node 3', 'Node 4'])
plt.show()

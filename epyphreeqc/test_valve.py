from epyphreeqc import EpyPhreeqc
from phreeqpython import PhreeqPython
from epynet import Network
import matplotlib.pyplot as plt
import datetime
import time


# TIME INPUT PARAMETERS
timestep = 1  # minutes,  timestep for solving PHREEQC
time_end = 3  # hours,   maximum duration of the simulation
time_phreeqc = 1  # hours   timestep for changing PHREEQC solutions at reservoirs
time_report = 1  # minutes  timestep for reporting the result

# Convert input to minutes
time_end = time_end * 60
time_phreeqc = time_phreeqc * 60

# Initialize Epynet
network1 = Network('valve.inp')
# Initialize PhreeqPython and set a initial phreeqc solution
pp = PhreeqPython()
solutions = {}
sol0 = pp.add_solution({
    'Na': 0,
    'units': 'mg/l'
})
solutions[0] = sol0

# Initialize EpyPhreeqc
run_quality = EpyPhreeqc(network1, solutions, pp)
# Initialize Phreeqpython for the reservoirs
sol1 = pp.add_solution({
    'Na': 1,
    'units': 'mg/l'
})

sol7 = pp.add_solution({
    'Na': 0.5,
    'units': 'mg/l'
})

# Solve the Epynet network
network1.solve()
# Prepare an empty concentrations list
conc = []
solutions[network1.reservoirs['1'].uid] = sol1

# Main loop for solving the PHREEQC solutions
for time in range(0, time_end, time_phreeqc):
    sim_end = time + time_phreeqc

    # Assign PHREEQC solutions to reservoirs at select time intervals
    print(time)
    conc += run_quality.run(network1, solutions, timestep, time, sim_end, time_report)


# Plot output
t = [tt/60 for tt in range(0, time_end, time_report)]
Na2 = [x['2']['q'] for x in conc]
Na3 = [x['3']['q'] for x in conc]
Na4 = [x['4']['q'] for x in conc]

plt.subplot(311)
plt.plot(t, Na2)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Na [mg/l]')

plt.subplot(312)
plt.plot(t, Na3)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Na [mg/l]')

plt.subplot(313)
plt.plot(t, Na4)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Na [mg/l]')

plt.show()

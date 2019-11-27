from epyphreeqc import EpyPhreeqc
from phreeqpython import PhreeqPython
from epynet import Network

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time


# TIME INPUT PARAMETERS
timestep = 1  # minutes,  timestep for solving PHREEQC
time_end = 2  # hours,   maximum duration of the simulation
time_phreeqc = 2  # hours   timestep for changing PHREEQC solutions at reservoirs
time_report = 1  # minutes  timestep for reporting the result

# Convert input to minutes
time_end = time_end * 60
time_phreeqc = time_phreeqc * 60

# Initialize Epynet
network1 = Network('10_nodes.inp')
# Initialize PhreeqPython and set a initial phreeqc solution
pp = PhreeqPython()
solutions = {}
sol0 = pp.add_solution({
    'Ca': 0,
    'units': 'mg/l'
})
solutions[0] = sol0

# Initialize EpyPhreeqc
time_1 = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
run_quality = EpyPhreeqc(network1, solutions, pp, time_1)
# Initialize Phreeqpython for the reservoirs
sol1 = pp.add_solution({
    'Ca': 1,
    'units': 'mg/l'
})

# Solve the Epynet network
network1.solve()
# Prepare an empty concentrations list
conc = []
solutions[network1.reservoirs['1'].uid] = sol1

t = []
date_step = datetime.timedelta(minutes=time_report)

# Main loop for solving the PHREEQC solutions
for time in range(0, time_end, time_phreeqc):
    sim_end = time + time_phreeqc

    # Assign PHREEQC solutions to reservoirs at select time intervals
    conc += run_quality.run(network1, solutions, timestep, time, sim_end, time_report, time_1)

for i in range(0, time_end, time_report):
    t.append(time_1)
    time_1 += date_step

# Plot output
Ca2 = [x['2']['q'] for x in conc]
Ca6 = [x['6']['q'] for x in conc]

Ca7 = [x['7']['q'] for x in conc]
Ca8 = [x['8']['q'] for x in conc]
Ca11 = [x['11']['q'] for x in conc]

data = pd.DataFrame([t,Ca2,Ca6,Ca7,Ca8,Ca11])
data = data.transpose()
data.to_csv('10_nodes.csv')


plt.subplot(511)
plt.plot(t, Ca2)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Ca [mg/l]')

plt.subplot(512)
plt.plot(t, Ca6)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Ca [mg/l]')

plt.subplot(513)
plt.plot(t, Ca7)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Ca [mg/l]')

plt.subplot(514)
plt.plot(t, Ca8)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Ca [mg/l]')

plt.subplot(515)
plt.plot(t, Ca11)
plt.xlabel('Time [hours]')
plt.ylabel('Concentration Ca [mg/l]')

plt.show()

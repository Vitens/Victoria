<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/victoria.png" alt="Victoria Logo"/>
</p>


Victoria is a model for tracking the quality of water in a water distribution network.  
## Example Usage
```python
# load an Epanet network, PhreeqPython and Victoria
from epynet import Network
from phreeqpython import PhreeqPython
from victoria import Victoria
network = Network('network.inp')
pp = PhreeqPython()
model = Victoria(network,pp)
# Fill the links in the network from the reservoir
solutions = {}
sol0 = pp.add_solution({'Ca': 0,'units': 'mg/l'})
sol1 = pp.add_solution({'Ca': 1,'units': 'mg/l'})
solutions[0] = sol0
solutions[network.reservoirs['1'].uid] = sol1
# Solve the models
timestep_victoria = 60 # seconds
network.solve()
model.step(timestep_victoria, solutions)
# Calculate concentration of Ca
model.get_conc_node(network.nodes['2'], 'Ca', 'mg')
model.get_conc_pipe(network.links['1'], 'Ca', 'mg')
```
## Installation
* Clone or download repository
* ```python setup.py install```

## Requirements
* 64 bit Python 3
* EPYNET 
* PhreeqPython

## About Vitens

Vitens is the largest drinking water company in The Netherlands. We deliver top quality drinking water to 5.6 million people and companies in the provinces Flevoland, Fryslân, Gelderland, Utrecht and Overijssel and some municipalities in Drenthe and Noord-Holland. Annually we deliver 350 million m³ water with 1,400 employees, 100 water treatment works and 49,000 kilometres of water mains.

One of our main focus points is using advanced water quality, quantity and hydraulics models to further improve and optimize our treatment and distribution processes.

## Licence

Copyright 2019 Vitens

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

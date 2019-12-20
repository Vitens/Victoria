# Solver 

## Filling the network
After initialization of the network, the links in the network require to be filled with an initial solution. It is either filled with a user defined standard solution or the initial solution from the reservoirs is used as the initial condition. 

## Solving the network

The solver is a recursive function starting at a reservoir or tank. It uses the downstream and upstream links from Epynet to efficiently run through the whole network, while taking into account that all upstream links of a node have to be calculated before the solver can continue.


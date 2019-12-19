# Link Class

Victoria uses a Lagrangian time-based approach to track parcels along the pipes and nodes of a distribution network. For each parcel its position relative to the total volume of the pipe and its PHREEQC solution number or mixture of PHREEQC solutions numbers are tracked. With each PHREEQC solution number corresponding to all information about the solution such as temperature, pH and ion composition. 

For each time step the relative position of each parcel is updated depending on the flowrate of the particular pipe and the size of the time step. New parcels at the entrance of the pipe are only formed if the mixture of solution numbers is not similar to the subsequent parcel. Parcels exceeding the length of the pipe are removed from the pipe and stored in the order they exceeded the boundary in preparation of mixing the parcels at the nodes. 

<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/img/FIFO.PNG"/>
</p>


## Pipe Subclass
Standard link behavior, the main connection between individual nodes.

## Pump and Valve Subclass
Pumps and valve do not have a length in EPANET, so these link types require special treatment. If there is a flow through pump or valve the parcel is instantaneously pushed through the link. 

<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/img/PumpValve.PNG"/>
</p>
# MIX: Main Node Class

At nodes parcels from upstream pipes are mixed by the smallest parcel volume for each section of segment, in order to prevent the loss of data. The PHREEQC solutions are not actually mixed, only their relative volume fractions is determined and stored.

<img src="https://render.githubusercontent.com/render/math?math=X_%7Bk%7D%3D%5Cfrac%7B%5Csum_%7Bi%3D0%7D%5E%7Bn%7DQ_%7BIN%2Cn%7DX_%7Bk%2CIN%2Cn%7D%7D%7B%5Csum_%7Bj%3D0%7D%5E%7Bm%7DQ_%7BOUT%2Cm%7D%2BQ_%7BDEMAND%7D%7D%5C%5D"> 

Where Q IN,n  and X k,IN,n respectively represent the volumetric flowrate and fraction of PRHEEQC solution number “k” of upstream pipe “n”. Qout is the volumetric flowrate of the downstream pipes and QDemand is the volumetric flow demand at the particular node. After mixing the parcels are pushed to the downstream pipes.

<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/img/MIX.PNG"/>
</p>

## Junction Subclass
Standard node behavior, primarily the main node connecting sections of links.

## Reservoir Subclass
Special node which acts as an starting point for the calculation of the water quality in the system.It uses the outflow property from Epynet to assign the proper size of the flow into the downstream pipes.
A PHREEQC solution needs to be assigned to each reservoir in order for Victoria to work.

## Tank CSTR Subclass
The water entering the tank is instantaneously mixed with the water already present in the tank. The volume fraction of the water entering the tank can be derived from:\
<img src="https://render.githubusercontent.com/render/math?math=%5Cfrac%7Bd%7D%7Bdt%7D(N_%7BA%7D)%3DQ_%7BIN%7DC_%7BA%2CIN%7D-Q_%7BOUT%7DC_%7BA%7D">\
Assuming the volume of the tank is constant:\
<img src="https://render.githubusercontent.com/render/math?math=V%5Cfrac%7Bd%7D%7Bdt%7D(C_%7BA%7D)%3DQ_%7BIN%7DC_%7BA%2CIN%7D-Q_%7BOUT%7DC_%7BA%7D">\
Introduce a variable which is a fraction relative to the inflow concentration:\
<img src="https://render.githubusercontent.com/render/math?math=X_%7BA%7D%3D%5Cfrac%7BC_%7BA%7D%7D%7BC_%7BA%2CIN%7D%7D">\
by dividing the equation by CA,IN:\
<img src="https://render.githubusercontent.com/render/math?math=V%5Cfrac%7Bd%7D%7Bdt%7D(X_%7BA%7D)%3DQ_%7BIN%7D-Q_%7BOUT%7DX_%7BA%7D">\
Assuming the flowrate entering the tank is equal to the flowrate exiting the tank:\
<img src="https://render.githubusercontent.com/render/math?math=%5Cfrac%7Bd%7D%7Bdt%7D(X_%7BA%7D)%3D%5Cfrac%7BQ_%7BIN%7D%7D%7BV%7D(1-X_%7BA%7D)">\
Separation of variables and integrate:\
<img src="https://render.githubusercontent.com/render/math?math=%5Cint_0%5E%7BC_%7BA%7D%7D%5Cfrac%7BdC_%7BA%7D%7D%7B(X_%7BA%7D-1)%7D%3D-%5Cint_0%5Et%5Cfrac%7BQ_%7BIN%7D%7D%7BV%7Ddt">\
At t = 0 there is no volume fraction of the stream entering the tank present, so XA = 0\
<img src="https://render.githubusercontent.com/render/math?math=%5Cln(%5Cfrac%7BX_%7BA%7D-1%7D%7B-1%7D)%3D-%5Cfrac%7BQ_%7BIN%7D%7D%7BV%7Dt">\
Results in the equation describing the fraction of new solution entering the reactor:\
<img src="https://render.githubusercontent.com/render/math?math=X_%7BA%7D%3D1-%5Cexp(-%5Cfrac%7BQ_%7BIN%7D%7D%7BV%7Dt)">\
Similar, for the equation of the fraction of solution present in the reactor:\
<img src="https://render.githubusercontent.com/render/math?math=X_%7BB%7D%3D1-X_%7BA%7D%3D%5Cexp(-%5Cfrac%7BQ_%7BIN%7D%7D%7BV%7Dt)">\
Which allows the volume fractions of PHREEQC solutions in the tank to be calculated. 


## Tank LIFO Subclass
Water enters this tank based on Last In First Out principle, so it is basically like filling a column from the bottom. The parcel layers are segregated. When the tank empties, the parcels leave in order of last arrival. 

<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/img/TankLIFO.PNG"/>
</p>

## Tank FIFO Subclass
Water enters this tank based on First In First Out principle, like the pipes in the distribution network. The position of each parcel is dynamically updated based on the current volume of the tank, for example an increase in tank head will result in new parcel positions. 

<p align="center">
  <img src="https://github.com/michaeltan91/Victoria/blob/master/img/TankFIFO.PNG"/>
</p>


## LATEX:
In case the formulas do not show up and if Github supports inline formulas.

X_{k}=\frac{\sum_{i=0}^{n}Q_{IN,n}X_{k,IN,n}}{\sum_{j=0}^{m}Q_{OUT,m}+Q_{DEMAND}}\]

\frac{d}{dt}(N_{A})=Q_{IN}C_{A,IN}-Q_{OUT}C_{A}

V\frac{d}{dt}(C_{A})=Q_{IN}C_{A,IN}-Q_{OUT}C_{A}

X_{A}=\frac{C_{A}}{C_{A,IN}}

V\frac{d}{dt}(X_{A})=Q_{IN}-Q_{OUT}X_{A}

\frac{d}{dt}(X_{A})=\frac{Q_{IN}}{V}(1-X_{A})

\int_0^{C_{A}}\frac{dC_{A}}{(X_{A}-1)}=-\int_0^t\frac{Q_{IN}}{V}dt

\ln(\frac{X_{A}-1}{-1})=-\frac{Q_{IN}}{V}t

X_{A}=1-\exp(-\frac{Q_{IN}}{V}t)

X_{B}=1-X_{A}=\exp(-\frac{Q_{IN}}{V}t)
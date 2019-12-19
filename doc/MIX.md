# MIX: Main Node Class

At nodes parcels from upstream pipes are mixed by the smallest parcel volume for each section of segment, in order to prevent the loss of data. The PHREEQC solutions are not actually mixed, only their relative volume fractions is determined and stored.

![\X_{k}=\frac{\sum_{i=0}^{n}Q_{IN,n}X_{k,IN,n}}{\sum_{j=0}^{m}Q_{OUT,m}+Q_{DEMAND}}\\]](https://render.githubusercontent.com/render/math?math=%5CX_%7Bk%7D%3D%5Cfrac%7B%5Csum_%7Bi%3D0%7D%5E%7Bn%7DQ_%7BIN%2Cn%7DX_%7Bk%2CIN%2Cn%7D%7D%7B%5Csum_%7Bj%3D0%7D%5E%7Bm%7DQ_%7BOUT%2Cm%7D%2BQ_%7BDEMAND%7D%7D%5C%5D)
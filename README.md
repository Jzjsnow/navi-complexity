# Quantifying navigation complexity in transportation networks
Title: Quantifying navigation complexity in transportation networks
## Abstract
The complexity of navigation in large cities is increasing with the expansion of transportation networks, which brings a number of problems such as congestion and increased travel costs. When analysing urban navigation, previous studies typically assume that travellers make route choices based on global information of transportation networks, but the actual trips are mainly made based on local information. Here, using 76 million trips on Beijing subway, we characterise the information accessed by travellers in a sub-network and measure the navigation difficulty from an information perspective. We find that the traveller's decision cost is much smaller on the local network than on the global network, and for complex trips that require a large number of transfers, people tend to reduce their route choices to ease the local navigation. Furthermore, we calculate the navigation costs of Beijing subway from 2003 to 2020 and show that the local navigability can be improved while the global navigability is reduced during the network growth.

## Code description
- **route_matching.py** is used to calculate the matched paths from the OD records (Results sections 1).

- **LSI_from_matching.py** is used to calculate the local search information from the matched paths. (Results sections 2).

- **LSI_from_ksp.py** is used to calculate the local search information from the k shortest paths. (Results section 3).

- **GSI.py** reproduces the amount of global search information according to ref. [1] (Results sections 2 & 3).

- **funcs.py** includes the basic functions for the calculations in the networks.

- **iofiles.py** includes the I/O functions for saving and loading the files.

## Data description
All the data supporting the program is included in ./src_data/.

## References
[1] Gallotti, R., Porter,  M.  A.  & Barthelemy, M. Lost in transportation: Information measures and cognitive limits in multilayer navigation. Science Advances 2, e1500445 (2016).

## Cite
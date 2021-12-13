# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu and Yu Liu
## Abstract
The complexity of navigation in large cities increases with the expansion of transportation networks, which brings a number of problems such as congestion and increased travel costs. When analysing urban navigation, previous studies typically assume that travellers make route choices based on global information of networks, but the actual trips are mainly made based on local information. Here, using 76 million trips on the Beijing subway, we quantify the navigation difficulty from an information perspective. We find that the traveller's decision information on a local network is much smaller than on a global network and grows more slowly with the number of transfers. The evolution of navigation costs over the last two decades further demonstrates that while the global network becomes difficult to navigate, local navigability can still be improved. We also discover that behind the complexity of network dynamics a simple linear relationship exists between the local and global navigation information(s) that allows the two metrics to predict each other.

## Code description
Python codes to replicate the results of the paper:
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


Contact: zhuojun.jiang@pku.edu.cn
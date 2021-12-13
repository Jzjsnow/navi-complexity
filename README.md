# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in large cities increases with the expansion of transportation networks, which brings a number of problems such as congestion and increased travel costs. When analysing urban navigation, previous studies typically assume that travellers make route choices based on global information of networks, but the actual trips are mainly made based on local information. Here, using 76 million trips on the Beijing subway, we quantify the navigation difficulty from an information perspective. We find that the traveller's decision information on a local network is much smaller than on a global network and grows more slowly with the number of transfers. The evolution of navigation costs over the last two decades further demonstrates that while the global network becomes difficult to navigate, local navigability can still be improved. We also discover that behind the complexity of network dynamics a simple linear relationship exists between the local and global navigation information(s) that allows the two metrics to predict each other.

## Code
Python codes to replicate the results of the paper:
- **route_matching.py** is used to calculate the matched paths from the OD records.

- **LSI_from_matching.py** is used to calculate the local search information from the matched paths. 

- **LSI_from_ksp.py** is used to calculate the local search information from the k shortest paths.

- **GSI.py** reproduces the amount of global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

- **funcs.py** includes the basic functions for the calculations in the networks.

- **iofiles.py** includes the I/O functions for saving and loading the files.


Contact: zhuojun.jiang@pku.edu.cn


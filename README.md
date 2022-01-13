# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in large cities increases with the expansion of urban areas, which brings challenging transportation problems. Researchers have conducted many theoretical or simulation-based studies on urban navigation, but large-scale analyses based on actual mobility data are rare. Here, using 225 million subway trips of three major cities in China, we quantify the navigation difficulty from an information perspective, which reveals that 1) people conserve a small number of repeatedly used routes and 2) the navigation information in the real travel network is much smaller than the theoretical value. By modelling routing behaviours in the growing networks, we show that while the global navigability is deteriorating, local navigability can still be improved and there is a surprisingly universal linear relationship between the local and global navigation information(s). Our findings demonstrate how large-scale observations can quantify real-world navigation behaviour and could help evaluate transportation planning.

## Code
Python codes to replicate the results of the paper:
- **route_matching.py** is used to calculate the matched paths from the OD records.

- **LSI_from_matching.py** is used to calculate the local search information from the matched paths. 

- **LSI_from_ksp.py** is used to calculate the local search information from the k shortest paths.

- **GSI.py** reproduces the amount of global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

- **funcs.py** includes the basic functions for the calculations in the networks.

- **iofiles.py** includes the I/O functions for saving and loading the files.


Contact: zhuojun.jiang@pku.edu.cn


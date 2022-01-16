# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in large cities increases with the expansion of urban areas, which brings challenging transportation problems. Researchers have conducted many theoretical studies on urban navigation, but large-scale analyses based on actual mobility data are rare. Here, using 225 million subway trips of three major cities in China, we quantify the navigation difficulty from an information perspective, which reveals that 1) people conserve a small number of repeatedly used routes and tend to prefer a simplest path, and 2) the navigation information in the real travel network (the local network) is much smaller than the theoretical value (the global network). By modelling routing behaviours in the growing networks, we show that while the global network becomes difficult to navigate, local navigability can still be improved. Moreover, there is a surprisingly universal linear relationship between the local and global navigation information(s), which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviours and could help evaluate transportation planning.

## Code
Python codes to replicate the results of the paper:
- **route_matching.py** is used to calculate the matched paths from the OD records.

- **LSI_from_matching.py** is used to calculate the local search information from the matched paths. 

- **LSI_from_ksp.py** is used to calculate the local search information from the k shortest paths.

- **GSI.py** reproduces the amount of global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

- **funcs.py** includes the basic functions for the calculations in the networks.

- **iofiles.py** includes the I/O functions for saving and loading the files.

- **gen_figures.ipynb** reproduces the figures in the paper.

## Data
Data to replicate the results of the paper (saved as python objects in pickle files):
- networks: subway networks of three cities from 2000 to 2020.
	* Beijing (bj): 15 snapshots.
	* Shanghai (sh): 18 snapshots.
	* Shenzhen (sz): 8 snapshots.
- networks_with_records: subway networks of three cities in the specific years with smart card data.
	* Beijing (2019), Shanghai (2015), Shenzhen (2017).
	* Due to a data non-disclosure agreement, only three days of smart card records are shared in this data set for replication, please contact the authors for more data.
- src_data: basic information used to initialize the code.
- output: output data used to generate the figures in the paper.

Contact: zhuojun.jiang@pku.edu.cn


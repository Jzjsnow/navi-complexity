# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in cities increases with the expansion of urban areas, which creates challenging transportation problems and drives many studies on the navigability of networks. However, due to the lack of individual mobility data, large-scale empirical analysis of the wayfinder's real-world navigation is rare. Here, using 225 million subway trips from three major cities in China, we quantify navigation difficulty from an information perspective. Our results reveal that 1) people conserve a small number of repeatedly used routes, and 2) the navigation information in the sub-network formed by those routes is much smaller than the theoretical value in the global network, suggesting that the decision cost in actual trips is significantly smaller than the theoretical upper limit found in previous studies. By modeling routing behaviors in the growing networks, we show that while the global network becomes difficult to navigate, the navigability can be improved in sub-networks. We further present a universal linear relationship between the empirical and theoretical search information, which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviors and could help evaluate transportation planning.

## Code
Python codes to replicate the results of the paper:
- **route_matching.py** is used to calculate the matched paths from the OD records.

- **ESI_from_matching.py** is used to calculate the empirical search information from the matched paths. 

- **ESI_from_ksp.py** is used to calculate the empirical search information from the k shortest paths.

- **TSI.py** reproduces the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

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
	* Due to a data non-disclosure agreement, 7 days of smart card records in Beijing and Shanghai, and 5 days in Shenzhen (all for Shenzhen) are shared in this data set for replication, please contact the authors for more data.
- surveydata: 272 subway trips with known routes and duration through questionnaires in the three studied cities.
- src_data: basic information used to initialize the code.
- output: output data used to generate the figures in the paper.

Contact: zhuojun.jiang@pku.edu.cn


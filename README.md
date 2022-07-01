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
Data to replicate the results of the paper:
- [smart_card_data](https://github.com/Jzjsnow/navi-complexity/blob/main/data/smart_card_data): 7 days of smart card records in Beijing and Shanghai, and 5 days in Shenzhen (all for Shenzhen) are shared in this data set for replication.
	* bj_2019.csv: Beijing subway from 2019/5/15-2019/5/21.
	* sh_2015.csv: Shanghai subway from 2015/4/15-2015/4/21.
	* sz_2017.csv: Shenzhen subway from 2017/10/16-2017/10/20.
- [subway_info](https://github.com/Jzjsnow/navi-complexity/blob/main/data/subway_info): attributes of subway lines and stations in Beijing/Shanghai/Shenzhen (by 2020).
	* lines_[bj/sh/sz].csv: list of subway lines.
	* stations_[bj/sh/sz].csv: list of subway stations.
	* Eudistance_[bj/sh/sz].csv: Euclidean distance between each station pair.
- [networks](https://github.com/Jzjsnow/navi-complexity/blob/main/data/networks): subway networks of three cities from 2000 to 2020.
	* Beijing (bj): 15 snapshots.
	* Shanghai (sh): 18 snapshots.
	* Shenzhen (sz): 8 snapshots.
	* Each subway network and its information network are separately constructed by [networkx](https://networkx.org/) graph models and saved in [GML](https://web.archive.org/web/20190207140002/http://www.fim.uni-passau.de/index.php?id=17297&L=1) format.
- surveydata: 272 subway trips with known routes and duration through questionnaires in the three studied cities.
- flow_official: the official ridership of the Beijing subway for May 2019.
- src_data: basic information used to initialize the code.
- output: output data used to generate the figures in the paper.

Contact: snow.jiangzj@gmail.com


# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in cities has increased with the expansion of urban areas, creating challenging transportation problems that drive many studies on the navigability of networks. However, due to the lack of individual mobility data, large-scale empirical analysis of the wayfinder's real-world navigation is rare. Here, using 225 million subway trips from three major cities in China, we quantify navigation difficulty from an information perspective. Our results reveal that 1) people conserve a small number of repeatedly used routes, and 2) the navigation information in the sub-networks formed by those routes is much smaller than the theoretical value in the global network, suggesting that the decision cost for actual trips is significantly smaller than the theoretical upper limit found in previous studies. By modeling routing behaviors in growing networks, we show that while the global network can become difficult to navigate, navigability can be improved in sub-networks. We further present a universal linear relationship between the empirical and theoretical search information, which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviors and aid in evaluating transportation planning.

## Code
Codes to replicate the results of the paper.
### Overview
- **data_prepoccessing.sql** is used to pre-process and export smart card data.
- **route_matching.py** is used to calculate the matched paths from the OD records.

- **ESI_from_matching.py** is used to calculate the empirical search information from the matched paths. 

- **ESI_from_ksp.py** is used to calculate the empirical search information from the k shortest paths.

- **TSI.py** reproduces the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

- **funcs.py** includes the basic functions for the calculations in the networks.

- **iofiles.py** includes the I/O functions for saving and loading the files.

- **gen_figures.ipynb** reproduces the figures in the paper.

### Code description
See [README_for_code.md](https://github.com/Jzjsnow/navi-complexity/blob/main/README_for_code.md) for detail. 


## Data
Data to replicate the results of the paper.
### Overview
- [smart_card_data](https://github.com/Jzjsnow/navi-complexity/blob/main/data/smart_card_data): Smart card records in Beijing, Shanghai and Shenzhen.
	* bj_2019.csv: Beijing subway in May 2019.
	* sh_2015.csv: Shanghai subway in April 2015.
	* sz_2017.csv: Shenzhen subway from October 2017.
- [subway_info](https://github.com/Jzjsnow/navi-complexity/blob/main/data/subway_info): attributes of subway lines and stations in Beijing/Shanghai/Shenzhen (by 2020).
	* lines_[bj/sh/sz].csv: list of subway lines.
	* stations_[bj/sh/sz].csv: list of subway stations.
	* Eudistance_[bj/sh/sz].csv: Euclidean distance between each station pair.
- [networks](https://github.com/Jzjsnow/navi-complexity/blob/main/data/networks): subway networks of three cities from 2000 to 2020.
	* Beijing (bj): 15 snapshots.
	* Shanghai (sh): 18 snapshots.
	* Shenzhen (sz): 8 snapshots.
- surveydata: 272 subway trips with known routes and duration through questionnaires in the three studied cities.
- flow_official: the official published ridership of the Beijing subway for May 2019.
- src_data: basic information used to generate the figures.
- output: output data used to generate the figures in the paper.

### Data description
See [README_for_data.md](https://github.com/Jzjsnow/navi-complexity/blob/main/README_for_data.md) for detail. 




Contact: snow.jiangzj@gmail.com


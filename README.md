# Quantifying navigation complexity in transportation networks
Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in cities has increased with the expansion of urban areas, creating challenging transportation problems that drive many studies on the navigability of networks. However, due to the lack of individual mobility data, large-scale empirical analysis of the wayfinder's real-world navigation is rare. Here, using 225 million subway trips from three major cities in China, we quantify navigation difficulty from an information perspective. Our results reveal that 1) people conserve a small number of repeatedly used routes, and 2) the navigation information in the sub-networks formed by those routes is much smaller than the theoretical value in the global network, suggesting that the decision cost for actual trips is significantly smaller than the theoretical upper limit found in previous studies. By modeling routing behaviors in growing networks, we show that while the global network can become difficult to navigate, navigability can be improved in sub-networks. We further present a universal linear relationship between the empirical and theoretical search information, which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviors and aid in evaluating transportation planning.

***

## Data

Data to replicate the results of the paper.

### Smart card data

Smart card records in Beijing, Shanghai and Shenzhen. The datasets provide OD at the station level grouped by travel time (see [data prepoccessing](https://github.com/Jzjsnow/navi-complexity/blob/main/code/data_prepoccessing.sql) for details):
- bj_2019.csv: Beijing subway in May 2019. [[Download]](https://drive.google.com/file/d/1bvmvDsBAu70z3hQmaPV03DwKE7N-YZuT/view?usp=sharing)
- sh_2015.csv: Shanghai subway in April 2015. [[Download]](https://drive.google.com/file/d/1paTKWMMhFTNv4ech9u4IjCknbBKIWsTp/view?usp=sharing)
- sz_2017.csv: Shenzhen subway in October 2017. [[Download]](https://drive.google.com/file/d/118K2ny2So78NbKgWLAuZ-wCoQBBG7-rZ/view?usp=sharing)

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|lineid_o|identication of the starting subway line|int|
|stationid_o|identication of the starting subway station|int|
|stationname_o|name of the starting subway station|str|
|lineid_d|identication of the terminal subway line|int|
|stationid_d|identication of the terminal subway station|int|
|stationname_d|name of the terminal subway station|str|
|d\_time|interval between the entry and exit timestamps (in seconds)|int|
|count|number of trips with a *d_time* travel time between this station pair|int|

	
### [Subway information](https://github.com/Jzjsnow/navi-complexity/blob/main/data/subway_info)

Attributes of subway lines and stations in Beijing/Shanghai/Shenzhen (by 2020):
- lines_[bj/sh/sz].csv: list of subway lines.
- stations_[bj/sh/sz].csv: list of subway stations.
- Eudist_[bj/sh/sz].csv: Euclidean distance between each station pair. 


### [Networks](https://github.com/Jzjsnow/navi-complexity/blob/main/data/networks)

Subway/information networks of three cities from 2000 to 2020:

- PrimalGraph\_[bj/sh/sz]\_[yyyy].gml: the subway network of Beijing/Shanghai/Shenzhen in the year of 'yyyy'. 
    * Node: each node represents a station.
    * Edge: each edge represents the subway line connecting adjacent stations.
	
|**Node attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled as 'lineid-stationid'|str|
			
|**Edge attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
|source|the serial number of the starting node|int|
|target|the serial number of the terminal node|int|
|key/nid|identication of the subway line|int|
|duration|the in-vehicle time of the section|double|
|distance|the Euclidean distance along the subway line between the connected stations|double|


- DualGraph\_[bj/sh/sz]\_[yyyy].gml: the information network of Beijing/Shanghai/Shenzhen in the year of 'yyyy'. 
    * Node: each node represents a subway line.
    * Edge: each edge represents the transfer station connecting the two intersecting lines. 

|**Node attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled by 'lineid', where lineid represents the line ID|str|
|name|name of the line|int|
		
|**Edge attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
|source|the serial number of the starting node|int|
|target|the serial number of the terminal node|int|
|key/sid|identication of the subway station|int|
|crossing|name of the transfer station|str|

**Usage (Python 3.7)**

Import the networkx module with
```python
>>> import networkx as nx
```

Import the subway network with
```python
>>> H = nx.read_gml('PrimalGraph_bj_2019.gml')
```
	
### [Survey data](https://github.com/Jzjsnow/navi-complexity/blob/main/data/survey_data.csv)

272 subway trips with known routes and duration through questionnaires in the three studied cities.

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|id|questionnaire id|int|
|city|abbreviation of the city name|str|
|line_o|name of the starting subway line|str|
|station_o|name of the starting subway station|str|
|line_d|name of the terminal subway line|str|
|station_d|name of the terminal subway station|str|
|line1|name of the 1st subway line taken in this trip|str|
|line2|name of the 2nd subway line taken in this trip (blank if none)|str|
|line3|name of the 3rd subway line taken in this trip (blank if none)|str|
|line4|name of the 4th subway line taken in this trip (blank if none)|str|
|line5|name of the 5th subway line taken in this trip (blank if none)|str|
|line6|name of the 6th subway line taken in this trip (blank if none)|str|
|transfer1|name of the 1st transfer station taken in this trip (blank if none)|str|
|transfer2|name of the 2nd transfer station taken in this trip (blank if none)|str|
|transfer3|name of the 3rd transfer station taken in this trip (blank if none)|str|
|transfer4|name of the 4th transfer station taken in this trip (blank if none)|str|
|transfer5|name of the 5th transfer station taken in this trip (blank if none)|str|
|hour_o|Hour of the entry timestamp|int|
|minute_o|Minute of the entry timestamp|int|
|second_o|Second of the entry timestamp|int|
|hour_d|Hour of the exit timestamp|int|
|minute_d|Minute of the exit timestamp|int|
|second_d|Second of the exit timestamp|int|
|d\_time|interval between the entry and exit timestamps (in seconds)|int|
|nroutes|number of subway lines taken along the trip|int|
|choice|the way passengers choose this route(1: by intuitive/habit/experience, 2: selected from multiple routes, 3: directly select the first route recommended by the navigatison software, 4: others)|int|
|age|passenger's age group(1: <18, 2: 18-25, 3: 26-30, 4: 31-40, 5: 41-50, 6: 51-60, 7: >60)|int|


### [Official flow data](https://github.com/Jzjsnow/navi-complexity/blob/main/data/flow_official.csv)

The official published ridership of the Beijing subway for May 2019. The numbers are obtained from [Beijing Subway Company’s official Weibo](https://weibo.com/bjsubway).

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|linename|name of the subway line|str|
|2019/5/1|Ridership on 2019/5/1 (in millions)|double|
|2019/5/2|Ridership on 2019/5/2 (in millions)|double|
|...|...|double|
|2019/5/31|Ridership on 2019/5/31 (in millions)|double|

### [Data for figures](https://github.com/Jzjsnow/navi-complexity/blob/main/data/output)

Data used to generate the figures in the paper, which is the output of the [code](#code) for the paper (see [gen_figures](https://github.com/Jzjsnow/navi-complexity/blob/main/code/gen_figures.ipynb) for details).
- matrix_matched_path_[bj/sh/sz]\_[yyyy].pkl: the results of matched paths from [Route matching](#route-matching). The file contains:
	* a matrix of dataframes where the dataframe of matched paths from station i to station j is stored at (i,j)

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|seq_stops|sequence of stations along the path|str[]|
|pathturns|transfer stations along the path|str[]|
|seq_lines|sequence of lines along the matched path|int[]|
|nroutes|number of subway lines taken along the path|int|
|duration|the travel time of the matched path|double|
|distance|the Euclidean distance along the matched path|double|
|avg_counts|number of trips on the path|double|
|total|total number of trips between the OD stations|double|
	
- ESI/res_stationlevel_card_[bj/sh/sz]\_[yyyy].pkl: the results of the station-level empirical search information calculated based on the matched paths from [Calculate the empirical search information (ESI)](#calculate-the-empirical-search-information-esi). The file contains:
	* a dataframe of empirical search information values for all matched path in the information network
	* a dataframe of the empirical search information between station pairs

dataframe of empirical search information for matched paths
|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|i|start station id|int|
|j|terminal station id|int|
|seq_lines|sequence of nodes along the matched path in the information network|int[]|
|pathturns|transfer stations along the path|str[]|
|nroutes|number of subway lines taken along the trip|int|
|diff_nroutes|difference between the transfer number of this matched path and the minimum transfer number of all the matched paths between the OD stations|int|
|duration|the travel time of the matched path|double|
|avg_counts|number of trips on the path|double|
|Ktot_sub|number of connections in the sub-network of the OD stations|int|
|S_sub|empirical search information of taking this matched path|double|

&emsp;
	
dataframe of empirical search information for station pairs
|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|i|start station id|int|
|j|terminal station id|int|
|nroutes|number of subway lines taken between the OD stations|double|
|min_nroutes|minimum number of subway lines taken on the matched paths between the OD stations|int|
|duration|the travel time between the OD stations|double|
|Ktot_sub|number of connections in the sub-network of the OD stations|int|
|avg_counts|number of trips between the OD stations|double|
|k_paths|number of matched paths between the OD stations|int|
|S_sub|empirical search information between the OD stations|double|
	
- ESI/res_linelevel_card_[bj/sh/sz]\_[yyyy].pkl: the results of the line-level empirical search information calculated based on the matched paths from [Calculate the empirical search information (ESI)](#calculate-the-empirical-search-information-esi). The file contains:
	* matrices of line-level empirical search information between line pairs with all/1/2/3 transfers on the travel paths
	

- ESI/ksp_[k]\_[bj/sh/sz]\_[yyyy].pkl: the results of the empirical search information calculated based on the k shortest paths from [Calculate the empirical search information (ESI)](#calculate-the-empirical-search-information-esi). The file contains:
	* a matrix of station-level empirical search information values
	* a matrix of number of subway lines taken between station pairs
	* a matrix of travel time between station pairs
	* a matrix of travel distance between station pairs
	* matrices of line-level empirical search information between line pairs with all/1/2/3 transfers.


- TSI/[bj/sh/sz]\_[yyyy].pkl: the results of the theoretical search information calculated  from [Calculate the theoretical search information (TSI)](#calculate-the-theoretical-search-information-tsi). The file contains:
	* a matrix of station-level theoretical search information values
	* a matrix of number of subway lines on the fastest simplest path between station pairs
	* a matrix of travel time of the fastest simplest path between station pairs
	* a matrix of travel distance of the fastest simplest path between station pairs
	* matrices of line-level theoretical search information between line pairs with all/1/2/3 transfers on the fastest simplest paths

	
**Usage (Python 3.7)**

Import the I/O functions with
```python
>>> from iofiles import *
```

Import the data for figures with
```python
>>> data = load_variable('data/output/ESI/res_stationlevel_card_bj_2019.pkl')
>>> data[0] # view the dataframe
```

***

## Code

### Overview

- **data_prepoccessing.sql** is used to pre-process smart card data.

- **route_matching.py** is used to match paths from the OD records.

- **ESI_from_matching.py** is used to calculate the empirical search information from the matched paths. 

- **ESI_from_ksp.py** is used to calculate the empirical search information from the k shortest paths.

- **TSI.py** reproduces the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

- **funcs.py** includes the basic functions for the calculations in networks.

- **iofiles.py** includes the I/O functions for saving and loading files.

- **gen_figures.ipynb** reproduces figures in the paper.

### Route matching

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python route_matching.py 
```
The output will be in `output/`.

### Calculate the empirical search information (ESI) 

To generate the ESI results based on the matched path from the OD records, run in the terminal:
```linux
$ python ESI_from_matching.py
```
The output will be in `output/ESI`.

When no smart card data (matched paths) are available from 2000 to 2020, the ESI of the subway networks is calculated using the k shortest paths for each year (Beijing: k=13, Shanghai: k=12, Shenzhen k=6, see paper for detail).
To generate the ESI results based on the k shortest paths, run in the terminal:
```linux
$ python ESI_from_ksp.py
```

### Calculate the theoretical search information (TSI) 
Reproduce the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

To generate the TSI results using the provided scripts, run in the terminal:
```linux
$ python TSI.py
```
The output will be in `output/TSI`. 



***

Contact: snow.jiangzj@gmail.com


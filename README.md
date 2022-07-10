# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in cities has increased with the expansion of urban areas, creating challenging transportation problems that drive many studies on the navigability of networks. However, due to the lack of individual mobility data, large-scale empirical analysis of the wayfinder's real-world navigation is rare. Here, using 225 million subway trips from three major cities in China, we quantify navigation difficulty from an information perspective. Our results reveal that 1) people conserve a small number of repeatedly used routes, and 2) the navigation information in the sub-networks formed by those routes is much smaller than the theoretical value in the global network, suggesting that the decision cost for actual trips is significantly smaller than the theoretical upper limit found in previous studies. By modeling routing behaviors in growing networks, we show that while the global network can become difficult to navigate, navigability can be improved in sub-networks. We further present a universal linear relationship between the empirical and theoretical search information, which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviors and aid in evaluating transportation planning.

## Content

- [Code](#code)
  * [Overview](#overview)
  * [Setup](#setup)
  * [Route matching](#route-matching)
  * [Calculate the empirical search information (ESI)](#calculate-the-empirical-search-information-esi)
    + [From the matched paths](#from-the-matched-paths)
    + [From the k shortest paths](#from-the-k-shortest-paths)
  * [Calculate the theoretical search information (TSI)](#calculate-the-theoretical-search-information-tsi)
- [Data](#data)
  * [Overview](#overview-1)
  * [Smart card data](#smart-card-data)
  * [Subway basic information](#subway-basic-information)
  * [Subway network data](#subway-network-data)
  * [Survey data](#survey-data)
  * [Official ridership data](#official-ridership-data)


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

### Setup
The codes are based on Python 3.7.7. They have been tested on Ubuntu 18.04.3 LTS.

**Dependencies:** 
- networkx 2.5
- numpy 1.20.2
- pandas 1.2.4

### Route matching
Calculate the matched paths from the OD records.

**Data requirements**

- stations_[bj/sh/sz].csv: station list
- PrimalGraph_[bj/sh/sz]\_yyyy.gml: subway networks
- DualGraph_[bj/sh/sz]\_yyyy.gml: information networks
- Eudistance_[bj/sh/sz].csv: Euclidean distances between stations
- smart_card_data/[bj/sh/sz]\_yyyy.csv: smart card data

**Code requirements**
- route_matching.py
- funcs.py
- iofiles.py

**Output**
|**Variable**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|matrix_matched_path|matched paths between each station pair|matrix|


**Usage**

To generate the route matching results (data/output/ESI/matrix_matched_path_[suffix]) using the provided scripts, run in the terminal:
```linux
$ python route_matching.py # The target city can be changed by editing the script
```
The output will be in `output/ESI`. The format of the output can also be changed by editing the script.

Load the output in python
```python
>>> from iofiles import *
>>> [matrix_matched_path] = load_variable(
    'output/ESI/matrix_matched_path_2019_402_284.pkl') # results for Beijing subway
```

View the match paths between the station pair sid1-sid2 (stations 1-15 for example)
```python
>>> matrix_matched_path[1-1][15-1] # return a dataframe of matched paths between the station pair.
```

### Calculate the empirical search information (ESI) 

#### From the matched paths

**Data requirements**
- lines_[bj/sh/sz].csv: subway line list
- PrimalGraph_[bj/sh/sz]\_yyyy.gml: subway networks
- DualGraph_[bj/sh/sz]\_yyyy.gml: information networks
- Eudistance_[bj/sh/sz].csv: Euclidean distances between stations
- matrix_matched_path_[suffix].pkl: matched paths
	
**Code requirements**

- ESI_from_matching.py
- funcs.py
- iofiles.py

**Output**

|**Variable**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|df_matched_paths|search information of all matched paths|dataframe|
|df_Ss_i_j|station-level ESI for each OD station pair|dataframe|
|matrix_S_sub_nid|line-level ESI between each line pair|matrix|
|matrix_S_sub_nid_C1|line-level ESI between each line pair with C=1 transfer|matrix|
|matrix_S_sub_nid_C2|line-level ESI between each line pair with C=2 transfers|matrix|
|matrix_S_sub_nid_C3|line-level ESI between each line pair with C=3 transfers|matrix|


**Usage**

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_matching.py
```
The output will be in `output/ESI`. The format of the output can also be changed by editing the script.


View the output of the station-level ESI in python
```python
>>> from iofiles import *
>>> [df_matched_paths 
	,df_Ss_i_j
	] = load_variable(
	'output/ESI/res_stationlevel_bj_card_2019_402_284.pkl') # for Beijing subway
>>> df_Ss_i_j  # station-level ESI for each OD station pair.
```

View the output of the line-level ESI
```python
>>> [matrix_S_sub_nid,		
	matrix_S_sub_nid_C1,
	matrix_S_sub_nid_C2,
	matrix_S_sub_nid_C3,
	] = load_variable(
	'output/ESI/res_linelevel_card_2019_402_284.pkl')
>>> matrix_S_sub_nid_C2 # line-level ESI between each line pair with C=2 transfers
```	

#### From the k shortest paths

**Data requirements**

- stations_[bj/sh/sz].csv: station list
- lines_[bj/sh/sz].csv: subway line list
- PrimalGraph_[bj/sh/sz]\_yyyy.gml: subway networks
- DualGraph_[bj/sh/sz]\_yyyy.gml: information networks
- Eudistance_[bj/sh/sz].csv: Euclidean distances between stations

	
**Code requirements**
- ESI_from_ksp.py
- funcs.py
- iofiles.py

**Output**

|**Variable**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|matrix_Ss_sub|station-level ESI between each station pair|matrix|
|matrix_nroutes_sub|number of lines included in the fastest simplest path of each station pair|matrix|
|matrix_pathlength_sub|travel time of the fastest simplest path of each station pair|matrix|
|matrix_pathdist_sub|travel distance of the fastest simplest path of each station pair|matrix|
|matrix_Ktot_sub|number of connections in the sub-networks of each station pair|matrix|
|matrix_S_sub_nid|line-level ESI between each line pair|matrix|
|matrix_Ktot_st_sub|average number of connections in the sub-networks of all the OD stations between the line pair|matrix|
|matrix_S_sub_nid_C1|line-level ESI between each line pair with C=1 transfer|matrix|
|matrix_Ktot_st_C1_sub|average number of connections in the sub-networks of OD stations with C=1 transfer between the line pair|matrix|
|matrix_S_sub_nid_C2|line-level ESI between each line pair with C=2 transfers|matrix|
|matrix_Ktot_st_C2_sub|average number of connections in the sub-networks of OD stations with C=2 transfer between the line pair|matrix|
|matrix_S_sub_nid_C3|line-level ESI between each line pair with C=3 transfers|matrix|
|matrix_Ktot_st_C3_sub|average number of connections in the sub-networks of OD stations with C=3 transfer between the line pair|matrix|


**Usage**

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_ksp.py
```
The output will be in `output/ESI`.  The format of the output can also be changed by editing the script.


Load the output in python
```python
>>> from iofiles import *
>>> [matrix_Ss_sub,
	 matrix_nroutes_sub,
	 matrix_pathlength_sub,
	 matrix_pathdist_sub,
 	 matrix_Ktot_sub,
	 matrix_S_sub_nid,
	 matrix_Ktot_st_sub,
	 matrix_S_sub_nid_C1,		
	 matrix_Ktot_st_C1_sub,
	 matrix_S_sub_nid_C2,
	 matrix_Ktot_st_C2_sub,
	 matrix_S_sub_nid_C3,
	 matrix_Ktot_st_C3_sub,
    ] = load_variable(
	'output/ESI/ksp_13_bj_2015.pkl') # results for Beijing subway in 2015 with k=13 paths
```

View the matrix of station-level ESI for each OD station pair
```python
>>> matrix_Ss_sub
```

View the line-level ESI between each line pair with C=2 transfers
```python
>>> matrix_S_sub_nid_C2
```	



### Calculate the theoretical search information (TSI) 
Reproduce the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

**Data requirements**

- stations_[bj/sh/sz].csv: station list	
- line list: lines_[bj/sh/sz].csv
- PrimalGraph_[bj/sh/sz]\_yyyy.gml: subway networks
- DualGraph_[bj/sh/sz]\_yyyy.gml: information networks
	
**Code requirements**
- TSI.py
- funcs.py
- iofiles.py

**Output**

|**Variable**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|matrix_Ss|station-level TSI between each station pair|matrix|
|matrix_nroutes|number of lines included in the fastest simplest path of each station pair|matrix|
|matrix_pathlength|travel time of the fastest simplest path of each station pair|matrix|
|matrix_pathdist|travel distance of the fastest simplest path of each station pair|matrix|
|matrix_S_nid|line-level TSI between each line pair|matrix|
|matrix_S_nid_C1|line-level TSI between each line pair with C=1 transfer|matrix|
|matrix_S_nid_C2|line-level TSI between each line pair with C=2 transfers|matrix|
|matrix_S_nid_C3|line-level TSI between each line pair with C=3 transfers|matrix|


**Usage**

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python TSI.py
```
The output will be in `output/TSI`. The format of the output can also be changed by editing the script.


Load the output in python
```python
>>> from iofiles import *
>>> [matrix_Ss,
	 matrix_nroutes,
	 matrix_pathlength,
	 matrix_pathdist,
	 G,             # subway network
 	 dualG,         # information network
	 dualG_nodes, 	# list of nodes in the dualG.
	 dualG_edges,   # list of edges in the dualG.
	 N_sub,         # number of nodes in G
	 N_Ktot,        # number of connections in dualG
	 matrix_S_nid,
	 matrix_S_nid_C1,
	 matrix_S_nid_C2,
	 matrix_S_nid_C3]
    = load_variable(
	'output/TSI/bj_2015.pkl') # results for Beijing subway in 2015
```

View the station-level TSI for each OD station pair
```python
>>> matrix_Ss
```

View the line-level TSI between each line pair with C=2 transfers
```python
>>> matrix_S_nid_C2
```	




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

### Smart card data
Smart card records in Beijing, Shanghai and Shenzhen are shared in this data set.
The dataset provides the number of trips(records) at each travel time between each pair of stations ([Data prepoccessing](https://github.com/Jzjsnow/navi-complexity/blob/main/code/data_prepoccessing.sql)).

**Data-specific Information**

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|f\_line|identication of the starting subway line|int|
|sid1|identication of the starting subway station|int|
|fst\_name|name of the starting subway station|string|
|t\_line|identication of the terminal subway line|int|
|sid2|identication of the terminal subway station|int|
|tst\_name|name of the terminal subway station|string|
|d\_time|interval between the entry and exit timestamps (in seconds)|int|
|count|number of trips with a *d_time* travel time between this station pair|int|


**Usage**

View data in the terminal:
```linux
$ head -5 bj_2019.csv
```


### Subway basic information

The attributes of subway lines/stations in Beijing/Shanghai/Shenzhen (by 2020).

**Data-specific Information**

<a name="lines"></a>
- **lines\_[bj/sh/sz].csv**: list of subway lines.

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|nid|identication of the subway line|int|
|name|name of the subway line|string|
|full\_names|list of full names of the line that distinguishes the direction (marked by the starting and terminal station)|string[]|

&emsp;
<a name="stations"></a>
- **stations\_[bj/sh/sz].csv**: list of subway stations.

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|sid|identication of the subway station|int|
|name|name of the subway station|string|
|linesid|list of ids of subway lines where the station is located|int[]|
|lines|list of names of subway lines where the station is located|string[]|
|lat|latitude of the station|double|
|lng|longitude of the station|double|

&emsp;
<a name="Eudist"></a>
- **Eudistance\_[bj/sh/sz].csv**: Euclidean distance between each station pair. The distance is the geodesic distance calculated based on the latitude and longitude of the two stations

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|id|row index|int|
|sid1|starting station id|int|
|sid2|terminal station id|int|
|Eudistance|Euclidean distance between stations sid1 and sid2 (in meters)|double|

### Subway network data

Subway networks of of Beijing/Shanghai/Shenzhen from 2000 to 2020.

- 15 snapshots in Beijing (bj): 2003, 2004, 2007, 2008, 2009, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

- 18 snapshots in Shanghai (sh): 2000, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2020.

- 8 snapshots in Shenzhen (sz): 2004, 2007, 2009, 2010, 2011, 2016, 2019, 2020.


**Data-specific Information**

Each subway network (primal graph) and its information network (dual graph) are separately constructed by [networkx](https://networkx.org/) graph models and saved in [GML](https://web.archive.org/web/20190207140002/http://www.fim.uni-passau.de/index.php?id=17297&L=1) format.

- PrimalGraph\_[bj/sh/sz]\_yyyy.gml: the subway network of Beijing/Shanghai/Shenzhen in the year of 'yyyy'. 

	* Node: each node represents a station.
	* Edge: each edge represents the subway line connecting adjacent stations.
	
|**Node attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled as 'nid-sid', where [nid](#lines) represents the ID of the line on which the station is located and [sid](#stations) represents the station ID |string|
			
|**Edge attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|source|the serial number of the starting node|int|
|target|the serial number of the terminal node|int|
|key/nid|[line ID](#lines)|int|
|duration|the in-vehicle time of the section|double|
|distance|the Euclidean distance along the subway line between the connected stations|double|

\* If 'nid'=0, the edge connects a station that is on two different lines at the same time, i.e., the edge represents the transfer process. In this case, 'duration' indicates the transfer delay and is set to 300(s) by default.

\* If 'yyyy'='card', the network is used for route matching and the transfer delay is set specifically based on the smart card data (Beijing: 402s, Shanghai: 431s, Shenzhen: 376s).

&emsp;
- DualGraph\_[bj/sh/sz]\_yyyy.gml: the information network of Beijing/Shanghai/Shenzhen in the year of 'yyyy'. 

	* Node: each node represents a subway line.
	* Edge: each edge represents the transfer station connecting the two intersecting lines. 

|**Node attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled by 'nid', where [nid](#lines) represents the line ID|string|
|name|name of the line|int|

		
|**Edge attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|source|the serial number of the starting node|int|
|target|the serial number of the terminal node|int|
|key/sid|[station ID](#stations) |int|
|crossing|name of the transfer station|string|


**Usage (Python 3.7)**

Import the networkx module with
```python
>>> import networkx as nx
```


Import the subway network with
```python
>>> H = nx.read_gml('PrimalGraph_bj_2019.gml')
```

Get the nodes with
```python
>>> H.nodes
NodeView(('1-18', '1-1', '1-12', '1-11', '1-2',…, '24-334', '24-340'))
```

Get the edges with
```python
>>> H.edges(data=True)
OutMultiEdgeDataView([('1-18', '1-1', {'distance': 1174.0, 'duration': 120.0, 'nid': 1}), ('1-18', '1-20', {'distance': 1165.0, 'duration': 120.0, 'nid': 1}),…,('24-340', '24-334', {'distance': 1343.0, 'duration': 180.0, 'nid': 24})])
```

Import the information network with

```python
>>> dualH = nx.read_gml('Dual Graph_bj_2019.gml', destringizer=int)
```
Get the nodes with

```python
>>> dualH.nodes(data=True)
NodeDataView({1: {'name': 'LINE 1'}, 2: {'name': 'LINE 2'},…,24: {'name': 'YIZHUANG LINE'}})
```

Get the edges with
```python
>>> dualH.edges(data=True)
MultiEdgeDataView([(1, 9, {'sid': 18, 'crossing': 'MILITARY MUSEUM'}), (1, 3, {'sid': 16, 'crossing': 'XIDAN'}), …, (20, 23, {'sid': 312, 'crossing': 'YANCUNDONG'})])
```

### Survey data

272 subway trips with known routes and duration through questionnaires in the three studied cities.

**Data-specific Information**

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|id|questionnaire id|int|
|city|abbreviation of the city name|string|
|line_o|name of the starting subway line|string|
|station_o|name of the starting subway station|string|
|line_d|name of the terminal subway line|string|
|station_d|name of the terminal subway station|string|
|line1|name of the 1st subway line taken in this trip|string|
|line2|name of the 2nd subway line taken in this trip (blank if none)|string|
|line3|name of the 3rd subway line taken in this trip (blank if none)|string|
|line4|name of the 4th subway line taken in this trip (blank if none)|string|
|line5|name of the 5th subway line taken in this trip (blank if none)|string|
|line6|name of the 6th subway line taken in this trip (blank if none)|string|
|transfer1|name of the 1st transfer station taken in this trip (blank if none)|string|
|transfer2|name of the 2nd transfer station taken in this trip (blank if none)|string|
|transfer3|name of the 3rd transfer station taken in this trip (blank if none)|string|
|transfer4|name of the 4th transfer station taken in this trip (blank if none)|string|
|transfer5|name of the 5th transfer station taken in this trip (blank if none)|string|
|HH1|Hour of the entry timestamp|int|
|MM1|Minute of the entry timestamp|int|
|SS1|Second of the entry timestamp|int|
|HH2|Hour of the exit timestamp|int|
|MM2|Minute of the exit timestamp|int|
|SS2|Second of the exit timestamp|int|
|d\_time|interval between the entry and exit timestamps (in seconds)|int|
|nroutes|number of subway lines taken along the trip|int|
|choice|the way passengers choose this route(1: by intuitive/habit/experience, 2: selected from multiple routes, 3: directly select the first route recommended by the navigatison software, 4: others)|int|
|age|passenger's age group(1: <18, 2: 18-25, 3: 26-30, 4: 31-40, 5: 41-50, 6: 51-60, 7: >60)|int|


### Official ridership data

The official published ridership of the Beijing subway for May 2019. The numbers are obtained from [Beijing Subway Company’s official Weibo](https://weibo.com/bjsubway).

**Data-specific Information**

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|line_name|name of the subway line|string|
|2019/5/1|Ridership on 2019/5/1 (in millions)|double|
|2019/5/2|Ridership on 2019/5/2 (in millions)|double|
|...|...|int|
|2019/5/31|Ridership on 2019/5/31 (in millions)|double|


&emsp;

Contact: snow.jiangzj@gmail.com


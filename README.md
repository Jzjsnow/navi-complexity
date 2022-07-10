# Quantifying navigation complexity in transportation networks
by Zhuojun Jiang, Lei Dong, Lun Wu, and Yu Liu

## Abstract
The complexity of navigation in cities has increased with the expansion of urban areas, creating challenging transportation problems that drive many studies on the navigability of networks. However, due to the lack of individual mobility data, large-scale empirical analysis of the wayfinder's real-world navigation is rare. Here, using 225 million subway trips from three major cities in China, we quantify navigation difficulty from an information perspective. Our results reveal that 1) people conserve a small number of repeatedly used routes, and 2) the navigation information in the sub-networks formed by those routes is much smaller than the theoretical value in the global network, suggesting that the decision cost for actual trips is significantly smaller than the theoretical upper limit found in previous studies. By modeling routing behaviors in growing networks, we show that while the global network can become difficult to navigate, navigability can be improved in sub-networks. We further present a universal linear relationship between the empirical and theoretical search information, which allows the two metrics to predict each other. Our findings demonstrate how large-scale observations can quantify real-world navigation behaviors and aid in evaluating transportation planning.


## Data

Data to replicate the results of the paper.

### Overview

- smart_card_data: Smart card records in Beijing, Shanghai and Shenzhen. The datasets provide OD at the station level grouped by travel time (see [Data prepoccessing](https://github.com/Jzjsnow/navi-complexity/blob/main/code/data_prepoccessing.sql) for details).
	* bj_2019.csv: Beijing subway in May 2019. [[Download]](https://drive.google.com/file/d/1IQwbTV3HCTYjAvU-CjDDn2YP4eS1An3l/view?usp=sharing)
	* sh_2015.csv: Shanghai subway in April 2015. [[Download]](https://drive.google.com/file/d/1kdfKzGT5vRyWn8abCJJoX4FSdWjBLRNu/view?usp=sharing)
	* sz_2017.csv: Shenzhen subway from October 2017. [[Download]](https://drive.google.com/file/d/1fp0c98tR8AnXSueauymgFKIimzOPe1LF/view?usp=sharing)

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|f\_line|identication of the starting subway line|int|
|sid1|identication of the starting subway station|int|
|fst\_name|name of the starting subway station|string|
|t\_line|identication of the terminal subway line|int|
|sid2|identication of the terminal subway station|int|
|tst\_name|name of the terminal subway station|string|
|d\_time|interval between the entry and exit timestamps (in seconds)|int|
|count|number of trips with a *d_time* travel time between this station pair|int|


	
- [subway_info](https://github.com/Jzjsnow/navi-complexity/blob/main/data/subway_info): attributes of subway lines and stations in Beijing/Shanghai/Shenzhen (by 2020).
	* lines_[bj/sh/sz].csv: list of subway lines.
	* stations_[bj/sh/sz].csv: list of subway stations.
	* Eudistance_[bj/sh/sz].csv: Euclidean distance between each station pair.

- [networks](https://github.com/Jzjsnow/navi-complexity/blob/main/data/networks): subway networks of three cities from 2000 to 2020.
	* Beijing (bj): 15 snapshots.
	* Shanghai (sh): 18 snapshots.
	* Shenzhen (sz): 8 snapshots.


- PrimalGraph\_[bj/sh/sz]\_yyyy.gml: the subway network of Beijing/Shanghai/Shenzhen in the year of 'yyyy'. 

	* Node: each node represents a station.
	* Edge: each edge represents the subway line connecting adjacent stations.
	
|**Node attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled as 'nid-sid', where [nid](#lines) represents the ID of the line on which the station is located and [sid](#stations) represents the station ID |string|
			
|**Edge attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
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
| :- | :- | :-: |
|id|serial number of the node in the network (starting from 0)|int|
|label|each node is labelled by 'nid', where [nid](#lines) represents the line ID|string|
|name|name of the line|int|

		
|**Edge attribute**|**Definition**|**Data type**|
| :- | :- | :-: |
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

	
- [surveydata](https://github.com/Jzjsnow/navi-complexity/blob/main/data/surveydata.csv): 272 subway trips with known routes and duration through questionnaires in the three studied cities.


|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
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

- [flow_official](https://github.com/Jzjsnow/navi-complexity/blob/main/data/flow_official.csv): the official published ridership of the Beijing subway for May 2019. The numbers are obtained from [Beijing Subway Company’s official Weibo](https://weibo.com/bjsubway).

|**Column**|**Definition**|**Data type**|
| :- | :- | :-: |
|line_name|name of the subway line|string|
|2019/5/1|Ridership on 2019/5/1 (in millions)|double|
|2019/5/2|Ridership on 2019/5/2 (in millions)|double|
|...|...|int|
|2019/5/31|Ridership on 2019/5/31 (in millions)|double|

- [data_figures](https://github.com/Jzjsnow/navi-complexity/blob/main/data/output): data used to generate the figures in the paper.


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

### Calculate the empirical search information (ESI) 

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_matching.py
```
The output will be in `output/ESI`.

#### From the k shortest paths

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_ksp.py
```
The output will be in `output/ESI`. 

### Calculate the theoretical search information (TSI) 
Reproduce the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python TSI.py
```
The output will be in `output/TSI`. 



&emsp;

Contact: snow.jiangzj@gmail.com


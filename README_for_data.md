# Data description 
Data for paper "Quantifying navigation complexity in transportation networks".
## Content
- [Smart card data](#smart-card-data)
  * [Data-specific Information](#data-specific-information)
  * [Usage](#usage)
- [Subway basic information](#subway-basic-information)
  * [Data-specific Information](#data-specific-information-1)
- [Subway network data](#subway-network-data)
  * [Data-specific Information](#data-specific-information-2)
  * [Usage (Python 3.7)](#usage-python-37)
- [Survey data](#survey-data)
  * [Data-specific Information](#data-specific-information-3)
- [Official ridership data](#official-ridership-data)
  * [Data-specific Information](#data-specific-information-4)


## Smart card data
Smart card records in Beijing, Shanghai and Shenzhen are shared in this data set.
The dataset provides the number of trips(records) at each travel time between each pair of stations ([Data prepoccessing](https://github.com/Jzjsnow/navi-complexity/blob/main/code/data_prepoccessing.sql)).

- **bj_2019.csv**: Beijing subway in May 2019.

- **sh_2015.csv**: Shanghai subway in April 2015.

- **sz_2017.csv**: Shenzhen subway from October 2017.

### Data-specific Information
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


### Usage
View data in the terminal:
```linux
$ head -5 bj_2019.csv
```


## Subway basic information
The attributes of subway lines/stations in Beijing/Shanghai/Shenzhen (by 2020).

### Data-specific Information
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

## Subway network data
Subway networks of of Beijing/Shanghai/Shenzhen from 2000 to 2020.

- 15 snapshots in Beijing (bj): 2003, 2004, 2007, 2008, 2009, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

- 18 snapshots in Shanghai (sh): 2000, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2020.

- 8 snapshots in Shenzhen (sz): 2004, 2007, 2009, 2010, 2011, 2016, 2019, 2020.


### Data-specific Information
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


### Usage (Python 3.7)
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

## Survey data

272 subway trips with known routes and duration through questionnaires in the three studied cities.

### Data-specific Information
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


## Official ridership data
The official ridership of the Beijing subway for May 2019. The ridership numbers are obtained from [Beijing Subway Company’s official Weibo](https://weibo.com/bjsubway).
### Data-specific Information
|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|line_name|name of the subway line|string|
|2019/5/1|Ridership on 2019/5/1|int|
|2019/5/2|Ridership on 2019/5/2|int|
|...|...|int|
|2019/5/31|Ridership on 2019/5/31|int|


&emsp;

Contact: snow.jiangzj@gmail.com
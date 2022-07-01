# Data description for network data

The subway networks of Beijing/Shanghai/Shenzhen from 2000 to 2020 are shared in this dataset. 

- 15 snapshots in Beijing (bj): 2003, 2004, 2007, 2008, 2009, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020.

- 18 snapshots in Shanghai (sh): 2000, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2020.

- 8 snapshots in Shenzhen (sz): 2004, 2007, 2009, 2010, 2011, 2016, 2019, 2020.

## Methodological Information

Each subway network (primal graph) and its information network (dual graph) are separately constructed by [networkx](https://networkx.org/) graph models and saved in [GML](https://web.archive.org/web/20190207140002/http://www.fim.uni-passau.de/index.php?id=17297&L=1) format.

## Data-specific Information

- PrimalGraph\_[bj/sh/sz]\_yyyy.gml: the subway network of Beijing/Shanghai/Shenzhen in the year of ‘yyyy’. 

	* Each node represents a station and is labelled as ‘nid-sid’, where nid represents the ID of the line on which the station is located and sid represents the station ID.

	* Each edge represents the subway line connecting adjacent stations. Edge attributes are detailed as following:


|**Edge attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|nid|line ID |int|
|duration|the in-vehicle time of the section.|double|
|distance|the Euclidean distance along the subway line between the connected stations.|double|

- DualGraph\_[bj/sh/sz]\_yyyy.gml: the information network of Beijing/Shanghai/Shenzhen in the year of ‘yyyy’. 

	* Each node represents a subway line and is labelled by ‘nid’, where nid represents the line ID. The attribute ‘name’ denotes the name of the line.

	* Each edge represents the transfer station connecting the two intersecting lines. Edge attributes are detailed as following:


|**Edge attribute**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|sid|station ID |int|
|crossing|name of the transfer station.|string|


## Data usage (in Python)

\# import the package

\>>> import networkx as nx

\# import the subway network

\>>> H = nx.read\_gml('PrimalGraph\_bj\_2019.gml')


\# return the nodes

\>>> H.nodes

NodeView(('1-18', '1-1', '1-12', '1-11', '1-2',…, '24-334', '24-340'))

\# return the edges

\>>> H.edges(data=True)

OutMultiEdgeDataView([('1-18', '1-1', {'distance': 1174.0, 'duration': 120.0, 'nid': 1}), ('1-18', '1-20', {'distance': 1165.0, 'duration': 120.0, 'nid': 1}),…,('24-340', '24-334', {'distance': 1343.0, 'duration': 180.0, 'nid': 24})])

\# import the information network

\>>> dualH = nx.read\_gml('Dual Graph\_bj\_2019.gml', destringizer=int)

\# return the nodes

\>>> dualH.nodes(data=True)

NodeDataView({1: {'name': 'LINE 1'}, 2: {'name': 'LINE 2'},…,24: {'name': 'YIZHUANG LINE'}})

\# return the edges

\>>> dualH.edges(data=True)

MultiEdgeDataView([(1, 9, {'sid': 18, 'crossing': 'MILITARY MUSEUM'}), (1, 3, {'sid': 16, 'crossing': 'XIDAN'}), …, (20, 23, {'sid': 312, 'crossing': 'YANCUNDONG'})])



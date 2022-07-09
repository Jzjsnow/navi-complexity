# Code description 
Codes for paper "Quantifying navigation complexity in transportation networks".
## Content
- [Setup](#setup)
- [Route matching](#route-matching)
  * [Data requirements](#data-requirements)
  * [Code requirements](#code-requirements)
  * [Usage](#usage)
- [Calculate the empirical search information(ESI)](#calculate-the-empirical-search-informationesi)
  * [From the matched paths](#from-the-matched-paths)
    + [Data requirements](#data-requirements-1)
    + [Code requirements](#code-requirements-1)
    + [Usage](#usage-1)
  * [From the k shortest paths](#from-the-k-shortest-paths)
    + [Data requirements](#data-requirements-2)
    + [Code requirements](#code-requirements-2)
    + [Usage](#usage-2)
- [Calculate the theoretical search information(TSI)](#calculate-the-theoretical-search-informationtsi)
  * [Data requirements](#data-requirements-3)
  * [Code requirements](#code-requirements-3)
  * [Usage](#usage-3)


## Setup
The codes are based on Python 3.7.2. They have been tested on Ubuntu 18.04.3 LTS.

**Dependencies:** 
- networkx 2.5
- numpy 1.20.2
- pandas 1.2.4

## Route matching
Calculate the matched paths from the OD records.

### Data requirements

- station list:
	* stations_[bj/sh/sz].csv
- subway/information networks:
	* PrimalGraph_[bj/sh/sz]_card.gml
	* DualGraph_[bj/sh/sz]_card.gml	
- Euclidean distances between stations:
	* Eudistance_[bj/sh/sz].csv
- smart card data:
	* smart_card_data/[bj/sh/sz]_yyyy.csv

### Code requirements
- route_matching.py
- funcs.py
- iofiles.py

### Usage

To generate the route matching results (data/output/ESI/matrix_matched_path_[suffix]) using the provided scripts, run in the terminal:
```linux
$ python route_matching.py # The target city can be changed by modifying the file
```
The output will be in `output/ESI`.

Load the output in python
```python
>>> from iofiles import *
>>> [matrix_matched_path] = load_variable(
    'output/ESI/matrix_matched_path_2019_402_284.pkl') # results for Beijing subway
```

View the match paths between the station pair sid1-sid2(stations 1-15 for example)
```python
>>> matrix_matched_path[1-1][15-1] # return a dataframe of matched paths between the station pair.
```

## Calculate the empirical search information(ESI) 

### From the matched paths

#### Data requirements
- subway line list:
	* lines_[bj/sh/sz].csv
- subway/information networks:
	* PrimalGraph_[bj/sh/sz]_card.gml
	* DualGraph_[bj/sh/sz]_card.gml
- Euclidean distances between stations:
	* Eudistance_[bj/sh/sz].csv
- matched paths:
	* matrix_matched_path_[suffix].pkl
	
#### Code requirements
- ESI_from_matching.py
- funcs.py
- iofiles.py


#### Usage

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_matching.py
```
The output will be in `output/ESI`.


View the output of the station-level ESI in python
```python
>>> from iofiles import *
>>> [df_matched_paths, df_Ss_i_j] = load_variable(
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


### From the k shortest paths

#### Data requirements

- station list:
	* stations_[bj/sh/sz].csv	
- line list:
	* lines_[bj/sh/sz].csv
- subway/information networks:
	* PrimalGraph_[bj/sh/sz]_yyyy.gml
	* DualGraph_[bj/sh/sz]_yyyy.gml
- Euclidean distances between stations:
	* Eudistance_[bj/sh/sz].csv

	
#### Code requirements
- ESI_from_ksp.py
- funcs.py
- iofiles.py


#### Usage

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python ESI_from_ksp.py
```
The output will be in `output/ESI`.


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

View the station-level ESI for each OD station pair
```python
>>> matrix_Ss_sub
```

View the line-level ESI between each line pair with C=2 transfers
```python
>>> matrix_S_sub_nid_C2
```	


## Calculate the theoretical search information(TSI) 
Reproduce the amount of theoretical global search information according to [Gallotti et al, 2016](https://www.science.org/doi/10.1126/sciadv.1500445).

### Data requirements

- station list:
	* stations_[bj/sh/sz].csv	
- line list:
	* lines_[bj/sh/sz].csv
- subway/information networks:
	* PrimalGraph_[bj/sh/sz]_yyyy.gml
	* DualGraph_[bj/sh/sz]_yyyy.gml

	
### Code requirements
- TSI.py
- funcs.py
- iofiles.py


### Usage

To generate the route matching results using the provided scripts, run in the terminal:
```linux
$ python TSI.py
```
The output will be in `output/TSI`.


Load the output in python
```python
>>> from iofiles import *
>>> [matrix_Ss,
	 matrix_nroutes,
	 matrix_pathlength,
	 matrix_pathdist,
	 G_sub,
 	 dualG_sub,
	 dualG_nodes_sub,
	 dualG_edges_sub,
	 N_sub,
	 N_Ktot,
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




Contact: snow.jiangzj@gmail.com


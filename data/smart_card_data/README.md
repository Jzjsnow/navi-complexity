# Data description for smart card data
7 days of smart card records in Beijing and Shanghai, and 5 days in Shenzhen (all for Shenzhen) are shared in this data set.

- **bj_2019.csv**: Beijing subway from 2019/5/15-2019/5/21.

- **sh_2015.csv**: Shanghai subway from 2015/4/15-2015/4/21.

- **sz_2017.csv**: Shenzhen subway from 2017/10/16-2017/10/20.

|**Column**|**Definition**|**Data type**|
| :-: | :-: | :-: |
|card\_id|card identication|string|
|f\_line|identication of the starting subway line|int|
|sid1|identication of the starting subway station|int|
|fst\_name|name of the starting subway station|string|
|t\_line|identication of the terminal subway line|int|
|sid2|identication of the terminal subway station|int|
|tst\_name|name of the terminal subway station|string|
|f\_tm|time stamp for entering the subway station|string|
|t\_tm|time stamp for exiting the subway station|string|
|d\_time|interval between the entry and exit timestamps|int|


**Data example:**

$ head -5 bj\_2019.csv

card\_id,f\_line,sid1,fst\_name,t\_line,sid2,tst\_name,f\_tm,t\_tm,d\_time

6c7d1477fff3ea19f1225d779cd681fb,10,68,HAIDIANHUANGZHUANG,6,92,CAOFANG,2019-05-20 21:20:00,2019-05-20 22:15:21,3321

597625ea7857ee67967d0a2b0fb74226,5,75,TIANTONGYUAN NORTH,1,19,GUOMAO,2019-05-20 07:42:00,2019-05-20 08:36:33,3273

597625ea7857ee67967d0a2b0fb74226,1,19,GUOMAO,5,75,TIANTONGYUAN NORTH,2019-05-20 17:10:00,2019-05-20 18:01:30,3090

620997c5c0d36c14e25248b991a7e09b,13,223,HUILONGGUAN,10,188,TAIYANGGONG,2019-05-20 09:51:00,2019-05-20 10:26:54,2154


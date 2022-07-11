-- PostgreSQL 10.1


-- Group the smart card records by the starting/terminal subway stations , starting/terminal lines, and the travel time.
copy (   
	select 
		lineid_o 				-- identication of the starting subway line
		,stationid_o      			-- identication of the starting subway station
		,stationname_o			-- name of the starting subway station
		,lineid_d				-- identication of the terminal subway line
		,stationid_d				-- identication of the terminal subway station
		,stationname_d		-- name of the terminal subway station
	    ,d_time				-- interval between the entry and exit timestamps (in seconds)
		,count(*) as count	-- number of trips with a d_time travel time between the station pair
	from
	card_bj_2019.od_substation_org ss -- card_bj_2019/card_sh_2015/card_sz_2017
	where stationid_o <> stationid_d
	group by lineid_o,stationid_o,stationname_o,lineid_d,stationid_d,stationname_d,d_time

) TO  'navigation_complexity/data/bj_2019.csv' with csv header

-- PostgreSQL 10.1


-- Group the smart card records by the starting/terminal subway stations , starting/terminal lines, and the travel time.
copy (   
	select 
		f_line 				-- identication of the starting subway line
		,sid1      			-- identication of the starting subway station
		,fst_name			-- name of the starting subway station
		,t_line				-- identication of the terminal subway line
		,sid2				-- identication of the terminal subway station
		,tst_name			-- name of the terminal subway station
	    ,d_time				-- interval between the entry and exit timestamps (in seconds)
		,count(*) as count	-- number of trips with a d_time travel time between the station pair
	from
	card_bj_2019.od_substation_org ss -- card_bj_2019/card_sh_2015/card_sz_2017
	where sid1 <> sid2
	group by f_line,sid1,fst_name,t_line,sid2,tst_name,d_time

) TO  'navigation_complexity/src_data/bj_2019.csv' with csv header
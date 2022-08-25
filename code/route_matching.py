# -*- coding: utf-8 -*-
"""
Functions for route matching (in Results section 1)

"""

import math
import pandas as pd
import numpy as np
from funcs import *
from iofiles import *


def route_cost(df_records_sub, df_ksp, buffer, args):
    """
    Match each record to the candidate path with the closest travel time and
    return the matched paths

    Parameters
    ----------
    df_records_sub : a pandas dataframe of the records.
    df_ksp : a pandas dataframe of the candidate paths to match.
    buffer : time buffer for filtering candidate paths.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    
    Returns
    -------
    df_ksp : the dataframe of the matched paths where the numbers of trips on each
    matched paths are added.

    """

    arr = np.sort(list(set(df_ksp['duration'].values)))
    
    t_start = int(arr[0]-buffer)
    t_end = int(arr[-1]+buffer)
    path_arr =np.zeros(t_end-t_start+1)
    path_arr[list((arr-t_start).astype(int))]=1
    
    ti = t_start
    left0 = ti-buffer if ti-buffer> t_start else t_start
    right0 = ti+buffer if ti+buffer < t_end else t_end
    cut_time =[ti]
    n_path = []
    
    for ti in range(t_start,t_end+1):
        left = ti-buffer if ti-buffer> t_start else t_start
        right = ti+buffer if ti+buffer < t_end else t_end    
        if(path_arr[left-t_start]-path_arr[left0-t_start]==-1 
           or path_arr[right-t_start]-path_arr[right0-t_start]==1):
            cut_time.append(ti)
            n_path.append(sum(path_arr[left0-t_start:right0 - t_start +1]))
        left0 = left
        right0 = right

    n_path.append(sum(path_arr[left0-t_start:right0 - t_start +1]))        
    cut_time.append(t_end+1)
    
    if df_records_sub[0].min()<=arr[0]:
        cut_time.append(df_records_sub[0].min())
    if df_records_sub[0].max()>arr[-1]:
        cut_time.append(df_records_sub[0].max())
    
    cut_time = list(set(cut_time))
    rbins = np.sort(cut_time)
    
    df_records_sub = df_records_sub.reset_index().drop(columns=['index'])
    cut1 = pd.cut(df_records_sub[0], bins=rbins, include_lowest=True,right=False)

    count1 = cut1.value_counts()
    count1_s = count1.sort_index()

    beta = args
    
    df_path_all = pd.DataFrame()
    for idx in count1_s[count1_s>0].index:
        ti = idx.left
        left0 = ti-buffer if ti-buffer> t_start else t_start
        ti = idx.right
        right0 = ti+buffer if ti+buffer < t_end else t_end
        df_path = df_ksp[(df_ksp['duration']>=left0)&(df_ksp['duration']<right0)].copy()
        
        df_path = df_path.reset_index().drop(columns=['index'])
        df_path['C'] = df_path['nroutes']-1
        df_path['Cmin'] = df_path['C'].min()
        df_path['deltaC'] = df_path['C']-df_path['Cmin']

        df_path['category'] = idx
        
        df_path.loc[:,'cost'] = beta[0]*df_path['duration'] + \
                          beta[1]*(1-np.exp(-df_path['C']))/df_path['eudistance']*1000 # eudistance unit: km        
        df_path['cost_max'] = df_path['cost'].max()

        # The path with the largest probability of being chosen is the matched path
        df_path['prob'] = 0
        df_path.loc[np.abs(df_path['cost'] - df_path['cost_max'])<0.000001,'prob'] = 1
        df_path = df_path[df_path['prob']==1]
        df_path['prob'] /= len(df_path)
        df_path['avg_counts'] = count1_s[idx]*df_path['prob']
        df_path_all = df_path_all.append(df_path)

    # count the number of trips on each matched path
    df_path_all = df_path_all.groupby(by = [df_path_all['seq_stops'].astype(np.str_)
                                          ,'duration'
                                          ,'distance'
                                          ,'nroutes'
                                          ,df_path_all['seq_lines'].astype(np.str_)]
                                      ,as_index=False
                       ).apply(lambda x : pd.Series([
                            x['seq_stops'].iloc[0]
                            ,x['seq_lines'].iloc[0]
                            ,np.sum(x['avg_counts'])
                        ])).rename(columns={0:'seq_stops'
                                            ,1:'seq_lines'
                                            ,2:'avg_counts' })
                                            
    df_path_all['avg_counts'] = df_path_all['avg_counts'].astype(int)
    df_path_all = df_path_all[df_path_all['avg_counts']>=0]
    
    return df_path_all


def matching_OD_stations(G_relabeled, sid1, sid2, df_records, line_dict, dict_eudist, buffer, args):
    """
    Match the records with the paths between the origin station sid1 and
    destination station sid2 in the network.

    Parameters
    ----------
    G_relabeled : the networkx graph of the subway network (nodes are labeled
    by 'lineid-stationid' in the graph).
    sid1 : the  orgin stations.
    sid2 : the destination stations.
    df_records : a pandas dataframe of records between each pair of stations.
    line_dict : a dictionary that maps the line IDs in the network to the line
    IDs in the records.
    dict_eudist : a dictionary that return the euclidean distance between each 
    station pair.
    buffer : time buffer for filtering candidate paths.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    
    Returns
    -------
    df_od_paths : a pandas dataframe containing all the matched paths between
    stations sid1 and sid2.

    """

    o_stations = [node for node in G_relabeled.nodes if node.split(
        '-')[1] == str(sid1)]
    d_stations = [node for node in G_relabeled.nodes if node.split(
        '-')[1] == str(sid2)]
    o_stations = list(set(o_stations))
    d_stations = list(set(d_stations))

    if(sid1 == sid2):
        return

    df_od_paths = pd.DataFrame()
    for o_label in o_stations:
        for d_label in d_stations:
            line1 = int(o_label.split('-')[0])
            line2 = int(d_label.split('-')[0])

            # Filter all records between station sid1 on line1 to station sid2 to line2
            list_records = []
            try:
                df_od_records = df_records[(df_records['sid1'] == sid1)
                                           & (df_records['sid2'] == sid2)
                                           & (df_records['lineid_o'].isin(line_dict[line1]))
                                           & (df_records['lineid_d'].isin(line_dict[line2]))]
                for idx in df_od_records.index:
                    list_records.extend(df_od_records['d_time'][idx])
            except Exception as e:
                print(o_label, d_label, e)
            df_records_sub = pd.DataFrame(
                {0: list_records})
            if(len(df_records_sub) == 0):
                continue

            # get the candidate paths in the network
            list_path, list_plen, list_dist, list_nroutes, list_lines, kpath = get_od_ksp_attr_all(
                o_label, d_label, G_relabeled, kmax, max(list_records)+buffer)
            df_ksp = pd.DataFrame({
                'seq_stops': list_path,
                'duration': list_plen,
                'distance': list_dist,
                'nroutes': list_nroutes,
                'seq_lines': list_lines,
                'k': kpath,
                'eudistance':dict_eudist[(sid1,sid2)]
            })
            if(len(df_ksp) == 0):
                continue
            try:
                # route matching
                df_ksp = route_cost(df_records_sub, df_ksp, buffer, args)
                df_od_paths = df_od_paths.append(df_ksp, ignore_index=True)
            except Exception as e:
                print(o_label, d_label, e, 'route_cut')

    if(len(df_od_paths) > 0):
        try:
            df_od_paths = df_od_paths.reset_index().drop(columns=['index'])
            df_od_paths['total'] = sum(df_od_paths['avg_counts'])
            df_od_paths['pathturns'] = None
            df_od_paths['pathturns'] = df_od_paths['pathturns'].astype(object)
            for idx in df_od_paths.index:
                list_path = df_od_paths['seq_stops'][idx]
                list_lines = [key for i in range(0, len(
                    list_path) - 1) for key in G_relabeled.get_edge_data(list_path[i], list_path[i + 1]).keys()]  # line id
                list_pathturns = [list_path[k] for k in range(len(list_lines))
                                  if k > 0 and list_lines[k] != list_lines[k - 1] and
                                  int(list_path[k].split('-')[1]) != sid1 and
                                  int(list_path[k].split('-')[1]) != sid2]
                df_od_paths.loc[idx,'pathturns'] = pd.DataFrame({'pathturns':[list_pathturns]})['pathturns'].values

        except Exception as e:
            print("%s,%s,%s" % (o_label, d_label, e))
            pass

    return df_od_paths


def matching(
        G_relabeled,
        kmax,
        df_records,
        mat_width,
        line_dict,
        dict_eudist,
        buffer,
        args,
        filename='log.txt'):
    """
    Match the records between each station pair in the network.

    Parameters
    ----------
    G_relabeled : the networkx graph of the subway network.
    kmax :The number of the shortest paths that are generated to match the
    records between a OD station pair at most. This value can be as large as
    possible, because the final number of selected paths needs to meet the
    travel time threshold of the records.
    df_records : a pandas dataframe of records between each pair of stations.
    mat_width : the width of the result matrix.
    line_dict : A dictionary that maps the line ID in the network to the line ID
    in the records.
    dict_eudist : a dictionary that return the euclidean distance between each 
    station pair.
    buffer : time buffer for filtering candidate paths.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    filename : the file name of the output log. The default is 'log.txt'.

    Returns
    -------
    matrix_matched_path : for each station pair i-j, matrix_matched_path[i][j] 
    contains the dataframe of matched paths between the station pair.

    """

    counts = 0
    progress = 0
    list_stationid = [int(node.split('-')[1]) for node in G_relabeled.nodes]

    matrix_matched_path = np.empty((mat_width, mat_width), dtype=object)

    for sid1 in list_stationid:
        for sid2 in list_stationid:
            counts += 1

            # print progress
            current_progress = int(
                (10 * counts) / (len(list_stationid) * len(list_stationid)))
            if(current_progress > progress):
                progress = current_progress
                with open(filename, "a") as f:
                    print('processing %.2f %%'
                          % (progress * 10), file=f)
                print('processing %.2f %%'
                      % (progress * 10))
            if(sid1 == sid2):
                continue

            # get the matched path between OD stations sid1 and sid2
            df_od_paths = matching_OD_stations(
                G_relabeled, sid1, sid2, df_records, line_dict, dict_eudist, buffer, args)


            # save in a matrix
            matrix_matched_path[sid1 - 1][sid2 - 1] = df_od_paths

    return matrix_matched_path


if __name__ == "__main__":

    kmax = 200
    files=[['bj','2019_402_284',[-0.00629 , -30.9936]],
        ['sh','2015_431_320',[-0.00228 , -127.7]],
        ['sz','2017_376_248',[-0.00311 , -113.2]]]
    city_idx = 0
    city_abbr = files[city_idx][0]
    suffix = files[city_idx][1]
    args = files[city_idx][2]

    # import data
    
    # read the subway network
    H = nx.read_gml('src_data/networks/PrimalGraph_'+city_abbr+'_card.gml') 
    
    # read the information network
    dualH = nx.read_gml('src_data/networks/DualGraph_'+city_abbr+'_card.gml', destringizer=int)  # the network is used for route matching and the transfer delay is set specifically based on the smart card data (Beijing: 402s, Shanghai: 431s, Shenzhen: 376s).


    dualH_nodes = list(dualH.nodes(data=True))
    dualH_edges = list(dualH.edges(data=True,keys=True))
    
    # read the station list
    tb = pd.read_csv('src_data/subway_info/stations_'+city_abbr+'.csv')
    dict_stations = {tb['stationid'].iloc[i]:tb['stationname'].iloc[i] for i in range(len(tb))}

    # read the Euclidean distances between stations
    tb = pd.read_csv('src_data/subway_info/Eudist_'+city_abbr+'.csv') 
    dict_eudist = {(tb['stationid_o'].iloc[i],tb['stationid_d'].iloc[i]):tb['Eudistance'].iloc[i]  for i in range(len(tb))} # Generate a dict() object
    
    # read the smart card data
    tb = pd.read_csv('src_data/smart_card_data/'+city_abbr+'_'+snapshot+'.csv') 
    Tconst = int(suffix[-3:]) # access/egress delay

    # group the records by the starting/terminal stations and store the sequence of travel times in the 'd_time' column
    df_records = tb.groupby(by = ['stationid_o','lineid_o','stationid_d','lineid_d']
                   ,as_index=False) \
                   .apply(lambda x : pd.Series([
                   [x['d_time'].values[i] * 60 - Tconst  # subtract the access/egress delay in advance 
                       for i in range(len(x))
                       for j in range(x['count'].values[i])
                   ]
                   ])) \
                   .rename(columns={0:'d_time','stationid_o':'sid1','stationid_d':'sid2'})  
    
    print('data loaded')

    list_nodeid = [x for x in dict_stations]
    mat_width = max(list_nodeid)

    # a dictionary that maps the line ID in the network to the line ID in the
    # records.
    if city_abbr=='bj':
        line_dict = {1: [1], 2: [2], 3: [4,93], 4: [5], 5: [6], 6: [7], 7: [8],
        8: [8], 9: [9], 10: [10,90], 11: [13], 12: [14], 13: [14], 14: [15],
        15: [16], 16: [91], 17: [97], 18: [94], 20: [95], 21: [98], 22: [89],
        23: [92], 24: [96]}  # for Beijing
    else:
        line_dict = {n[0]: [n[0]] for n in dualH_nodes} # for Shanghai, Shenzhen

    buffer = 600 # seconds
    matrix_matched_path = matching(
        H,
        kmax,
        df_records,
        mat_width,
        line_dict,
        dict_eudist,
        buffer,
        args,
        'log.txt')
    save_variable(
        [matrix_matched_path],
        'output/matrix_matched_path_' +
        city_abbr + '_' + suffix[:4] +
        '.pkl')

# -*- coding: utf-8 -*-
"""
Functions for route matching (in Results section 1)

"""

import math
import pandas as pd
import numpy as np
from funcs import *
from iofiles import *


def route_cut(df_records_sub, df_ksp):
    """
    Match each record to the candidate path with the closest travel time and
    return the matched paths

    Parameters
    ----------
    df_records_sub : a pandas dataframe of the records.
    df_ksp : a pandas dataframe of the candidate paths to match.

    Returns
    -------
    df_ksp : the dataframe of the paths where the numbers of trips on each
    matched paths are added.

    """

    arr = np.sort(df_ksp['duration'].values)
    arr = arr[(arr >= df_records_sub[0].min()) &
              (arr <= df_records_sub[0].max())]
    midtime = [(arr[i] + arr[i + 1]) / 2 for i in range(len(arr) - 1)
               if arr[i + 1] - arr[i] > 0.000001]
    bounds = [df_records_sub[0].min(), df_records_sub[0].max()]
    rbins = np.append(midtime, bounds)
    rbins = np.sort(rbins)

    cut1 = pd.cut(df_records_sub[0], bins=rbins, include_lowest=True)
    cut2 = pd.cut(df_ksp['duration'], bins=rbins, include_lowest=True)

    count1 = cut1.value_counts()
    count2 = cut2.value_counts()
    count1_s = count1.sort_index()
    count2_s = count2.sort_index()

    df_ksp['category'] = pd.cut(
        df_ksp['duration'],
        bins=rbins,
        include_lowest=True)
    df_ksp['bindex'] = pd.cut(
        df_ksp['duration'],
        bins=rbins,
        include_lowest=True,
        labels=False)
    df_ksp = df_ksp.merge(
        pd.DataFrame(
            {
                'category': (count1_s / count2_s).index,
                'avg_counts': (count1_s / count2_s).values}),
        how='inner',
        on='category')
    df_ksp['avg_counts'] = df_ksp['avg_counts'].astype(np.int)
    df_ksp = df_ksp[df_ksp['avg_counts'] > 0]

    return df_ksp


def matching_OD_stations(G_relabeled, sid1, sid2, df_records, line_dict):
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
            list_recordid = []
            try:
                df_od_records = df_records[(df_records[0] == sid1)
                                           & (df_records[2] == sid2)
                                           & (df_records[1].isin(line_dict[line1]))
                                           & (df_records[3].isin(line_dict[line2]))]
                for idx in df_od_records.index:
                    list_records.extend(df_od_records[4][idx])
                    list_recordid.extend(df_od_records[5][idx])
            except Exception as e:
                print(o_label, d_label, e)
            df_records_sub = pd.DataFrame(
                {0: list_records, 'idx': list_recordid})
            if(len(df_records_sub) == 0):
                continue

            # get the candidate paths in the network
            list_path, list_plen, list_dist, list_nroutes, list_lines, kpath = get_od_ksp_attr_all(
                o_label, d_label, G_relabeled, kmax, max(list_records))
            df_ksp = pd.DataFrame({
                'seq_stops': list_path,
                'duration': list_plen,
                'distance': list_dist,
                'nroutes': list_nroutes,
                'seq_lines': list_lines,
                'k': kpath
            })
            if(len(df_ksp) == 0):
                continue
            try:
                # route matching
                df_ksp = route_cut(df_records_sub, df_ksp)
                df_od_paths = df_od_paths.append(df_ksp, ignore_index=True)
            except Exception as e:
                print(o_label, d_label, e, 'route_cut')

    if(len(df_od_paths) > 0):
        try:
            df_od_paths['total'] = sum(df_od_paths['avg_counts'])
            df_od_paths['pathturns'] = None
            for idx in df_od_paths.index:
                list_path = df_od_paths['seq_stops'][idx]
                list_lines = [key for i in range(0, len(
                    list_path) - 1) for key in G_relabeled.get_edge_data(list_path[i], list_path[i + 1]).keys()]  # line id
                list_pathturns = [list_path[k] for k in range(len(list_lines))
                                  if k > 0 and list_lines[k] != list_lines[k - 1] and
                                  int(list_path[k].split('-')[1]) != sid1 and
                                  int(list_path[k].split('-')[1]) != sid2]
                df_od_paths['pathturns'][idx] = list_pathturns

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
                G_relabeled, sid1, sid2, df_records, line_dict)

            # save in a matrix
            matrix_matched_path[sid1 - 1][sid2 - 1] = df_od_paths

    return matrix_matched_path


if __name__ == "__main__":

    kmax = 200
    files=[['bj','2019_402_284'],['sh','2015_431_320'],['sz','2017_376_248']]
    city_idx = 0
    city_abbr = files[city_idx][0]
    suffix = files[city_idx][1]
    

    # import data
    [G, G_relabeled, dualG, dual_nodes, dual_edges, H, H_relabeled, dualH, dualH_nodes, dualH_edges,
        df_records] = load_variable('src_data/networks_with_records/data_G_'+city_abbr+'_card_' + suffix + '.pkl')
    print(
        'data',
        'src_data/networks_with_records/data_G_'+city_abbr+'_card_' + suffix,
        'loaded')

    list_nodeid = [x for x in G.nodes]
    mat_width = max(list_nodeid)

    # a dictionary that maps the line ID in the network to the line ID in the
    # records.
    line_dict = {1: [1], 2: [2], 3: [4,93], 4: [5], 5: [6], 6: [7], 7: [8],
        8: [8], 9: [9], 10: [10,90], 11: [13], 12: [14], 13: [14], 14: [15],
        15: [16], 16: [91], 17: [97], 18: [94], 20: [95], 21: [98], 22: [89],
        23: [92], 24: [96]}  # for Beijing
    # line_dict = {n[0]: [n[0]] for n in dualH_nodes} # for Shanghai, Shenzhen

    matrix_matched_path = matching(
        H_relabeled,
        kmax,
        df_records,
        mat_width,
        line_dict,
        'log.txt')
    save_variable(
        [matrix_matched_path],
        'output/matrix_matched_path_' +
        suffix +
        '.pkl')

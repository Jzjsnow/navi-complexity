# -*- coding: utf-8 -*-

"""
Functions for calculating LSI from matched paths (in Results section 2)
Steps:
    1. Construct the sub-network for each OD station pair and calculate the
    entropy of all the matched paths between the OD.
    2. Get the station-level LSI by aggregating the entropy of all the matched
    paths between station pairs.
    3. Get the line-level LSI by aggregating the entropy of all the matched
    paths between line pairs.

"""

import numpy as np
import networkx as nx
import pandas as pd
import math
from funcs import *
from iofiles import *


def merge_paths(df_all_paths):
    """
    Merge matched paths between a station pair by the sequence of lines and 
    transfer stations

    Parameters
    ----------
    df_all_paths : a dataframe containing all the matched paths (with possible
    duplication).

    Returns
    -------
    df_od_paths : a dataframe containing all the matched paths without duplication.

    """
    df_od_paths = df_all_paths[['avg_counts','nroutes','duration']] \
        .groupby(by=[df_all_paths['seq_lines'].astype(np.str_),df_all_paths['pathturns'].astype(np.str_)]) \
        .apply(lambda x: pd.Series([np.sum(x['avg_counts']),
                                    np.median(x['nroutes']),
                                    np.sum(x['duration'] * x['avg_counts']) / np.sum(x['avg_counts'])]))
    df_od_paths.rename(
        columns={
            0: 'avg_counts',
            1: 'nroutes',
            2: 'duration'},
        inplace=True)
    df_od_paths = df_od_paths.reset_index(level=[0, 1])
    df_od_paths['perc_counts'] = df_od_paths['avg_counts'] / \
        df_all_paths['total'][0]
    df_od_paths = df_od_paths[df_od_paths['perc_counts'] > 0]

    return df_od_paths


def LSI_btw_ij(
        df_all_paths,
        sid1,
        sid2,
        G_relabeled,
        dualG_nodes,
        dualG_edges):
    """
    Calculate the search information of each matched path between stations sid1
    and sid2 in the sub-network.

    Parameters
    ----------
    df_all_paths : a dataframe containing all the matched paths between stations
    sid1 and sid2.
    sid1 : orgin station.
    sid2 : destination station.
    G_relabeled : the networkx graph of the global subway network (nodes are 
    labeled by 'lineid-stationid' in the graph).
    dualG_nodes : the list of nodes in the global information network.
    dualG_edges : the list of edges in the global information network.

    Returns
    -------
    df_matched_paths : the search information of each matched path is added to
    column 'S_sub'.

    """
    df_od_paths = merge_paths(df_all_paths)
    if(len(df_od_paths) > 0 and df_od_paths['avg_counts'].sum() > 0):
        df_matched_paths = df_od_paths.copy(deep=True)
        df_matched_paths['i'] = sid1
        df_matched_paths['j'] = sid2

        list_paths = df_all_paths[df_all_paths['seq_lines'].astype(
            np.str_).isin(df_od_paths['seq_lines'])]['seq_stops']
        paths = [eval(idx) for idx in df_od_paths['seq_lines']]

        # construct the sub-network(G_sub)
        G_sub = G_relabeled.subgraph(
            list(set([x for j in list_paths for x in j]))).copy()

        # construct the information network (dualG_sub)
        dualG_sub, dualG_nodes_sub, dualG_edges_sub = get_sub_dualG_relabeled(
            G_sub, dualG_nodes, dualG_edges)
        N_Ktot_k = len(nx.Graph(dualG_sub).edges())

        # calculate the search information and other attributes
        # of each matched path
        E_k0 = [
            cal_entropy_in_dualG(
                [list_lines],
                dualG_sub) for list_lines in paths]
        df_matched_paths['S_sub'] = E_k0
        df_matched_paths['Ktot_sub'] = N_Ktot_k
        df_matched_paths['diff_nroutes'] = df_od_paths['nroutes'] - \
            df_od_paths['nroutes'].min()
        return df_matched_paths
    return None


def LSI_from_matching(
        G_relabeled,
        dualG_nodes,
        dualG_edges,
        matrix_matched_path,
        filename='log.txt'):
    """
    Calculate the search information of the matched paths between each station
    pair in the subway network.

    Parameters
    ----------
    G_relabeled : the networkx graph of the global subway network (nodes are
    labeled by 'lineid-stationid' in the graph).
    dualG_nodes : the list of nodes in the global information network.
    dualG_edges : the list of edges in the global information network.
    matrix_matched_path : a matrix of matched paths between each station pair.
    filename : the file name of the output log. The default is 'log.txt'.

    Returns
    -------
    df_matched_paths : the search information of all matched paths.

    """
    list_stationid = [int(node.split('-')[1]) for node in G_relabeled.nodes]

    df_matched_paths = pd.DataFrame(
        columns=[
            'seq_lines',
            'avg_counts',
            'perc',
            'i',
            'j',
            'nroutes',
            'S_sub',
            'diff_nroutes',
            'Ktot_sub',
            'diff_dura'])

    for sid1 in list_stationid:
        for sid2 in list_stationid:
            try:
                df_all_paths = matrix_matched_path[sid1 - 1][sid2 - 1]
                df_matched_paths0 = LSI_btw_ij(
                    df_all_paths, sid1, sid2, G_relabeled, dualG_nodes, dualG_edges)
                df_matched_paths = df_matched_paths.append(df_matched_paths0)

            except Exception as e:
                with open(filename, "a") as f:
                    print('%d,%d,%s' % (sid1, sid2, e), file=f)
                pass

    df_matched_paths['i'] = df_matched_paths['i'].astype(np.int)
    df_matched_paths['j'] = df_matched_paths['j'].astype(np.int)
    df_matched_paths['nroutes'] = df_matched_paths['nroutes'].astype(np.int)
    df_matched_paths['diff_nroutes'] = df_matched_paths['diff_nroutes'].astype(
        np.int)
    return df_matched_paths


def weighted_avg_and_std(values, weights):
    """ Return the weighted average and standard deviation """
    average = np.average(values, weights=weights)
    variance = np.average((values - average)**2, weights=weights)

    return (average, math.sqrt(variance))


def merge_2_ij_matching(df_matched_paths):
    """
    Get the station-level search information (LSI).
    The aggregation uses the entropy and flow weights of all the
    matched paths between station pairs

    Parameters
    ----------
    df_matched_paths : the dataframe containing all the matched paths and
    their search information between station pairs.

    Returns
    -------
    df_Ss_i_j : station-level LSI for each OD station pair.
    
    """
    df_Ss_i_j = df_matched_paths.groupby(
        ['i', 'j'], as_index=False) .apply(
        lambda x: pd.Series(
            [
                np.sum(
                    x['S_sub'] * x['avg_counts']) / np.sum(
                    x['avg_counts']), np.sum(
                    x['avg_counts']), len(
                    x['seq_lines']), np.sum(
                    x['nroutes'] * x['avg_counts']) / np.sum(
                    x['avg_counts']), np.min(
                    x['nroutes']), weighted_avg_and_std(
                    x['duration'], x['avg_counts'])[0]]))
    df_Ss_i_j.rename(
        columns={
            0: 'S_sub',
            1: 'avg_counts',
            2: 'k_paths',
            3: 'nroutes',
            4: 'min_nroutes',
            5: 'duration'},
        inplace=True)
    df_Ss_i_j['k_paths'] = df_Ss_i_j['k_paths'].astype(np.int)

    return df_Ss_i_j


def merge_2_st_matching(
        G_relabeled,
        df_matched_paths,
        thres_C=None,
        count_weighted=False):
    """
    Get the line-level search information (LSI).
    The aggregation uses the entropy and flow weights of all the
    matched paths between line pairs

    Parameters
    ----------
    G_relabeled : the subway network.
    df_matched_paths : the dataframe containing all the matched paths and
    their search information between station pairs.
                            ('S_sub': entropy of the path calculated in the
                            sub-network.
                            'avg_counts': the number of trips (records)
                            matching the path.)
    thres_C : if only paths with specific number of transfers C are used in the
    calculation, thres_C is set to the number of transfers included in the
    path. The default is None.
    count_weighted : True if the average values need to be weighted by the flow
    of the paths. The default is False.

    Returns
    -------
    matrix_S_nid : line-level LSI between each line pair.

    """

    list_nid = list(set([int(node.split('-')[0])
                         for node in G_relabeled.nodes]))
    list_sids = [list(set([int(node.split('-')[1])
                           for node in G_relabeled.nodes if int(node.split('-')[0]) == nid])) for nid in list_nid]

    matrix_S_nid = np.zeros((max(list_nid), max(list_nid))) * np.nan
    for i in range(0, len(list_nid)):
        for j in range(0, len(list_nid)):
            sort_paths = df_matched_paths[(df_matched_paths['i'].isin(np.array(
                list_sids[i]) - 1)) & (df_matched_paths['j'].isin(np.array(list_sids[j])))]
            list_S = np.array(sort_paths['S_sub'].tolist())
            list_nlines = np.array(sort_paths['nroutes'].tolist())

            if(count_weighted):
                list_count = np.array(sort_paths['avg_counts'].tolist())
                list_count = list_count[list_nlines > 0]
                
            list_S = list_S[list_nlines > 0]
            list_nlines = list_nlines[list_nlines > 0]
            
            if(thres_C is None):
                if(count_weighted):
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = np.sum(
                        list_S * list_count) / np.sum(list_count[list_nlines > 0])
                else:
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S) / list_S.size
            else:
                list_S = list_S[(list_nlines > 0) & (list_nlines == thres_C + 1)]

                if(count_weighted):
                    list_count = list_count[(list_nlines > 0) & (list_nlines == thres_C + 1)]
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S * list_count) / np.sum(list_count)
                else:
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S) / list_S.size

    return matrix_S_nid


if __name__ == "__main__":

    suffix = '2019_402_284'

    [G,
     G_relabeled,
     dualG,
     dualG_nodes,
     dualG_edges,
     H,
     H_relabeled,
     dualH,
     dualH_nodes,
     dualH_edges,
     df_records] = load_variable('src_data/networks_with_records/data_G_bj_card_' + suffix)
    print('data loaded')

    # import the matched paths
    [matrix_matched_path] = load_variable(
        'output/matrix_matched_path_' + suffix + '.pkl')

    # calculate the LSI of the matched paths
    df_matched_paths = LSI_from_matching(
        H_relabeled,
        dualH_nodes,
        dualH_edges,
        matrix_matched_path,
        filename='log.txt')

    # calculate the station-level LSI
    df_Ss_i_j = merge_2_ij_matching(df_matched_paths)

    # save
    save_variable([df_matched_paths, df_Ss_i_j],
                  'output/LSI/res_stationlevel_bj_card_' + suffix + '.pkl')

    # calculate the line-level LSI
    matrix_S_sub_nid = merge_2_st_matching(
        H_relabeled,
        df_matched_paths,
        count_weighted=True)
    matrix_S_sub_nid_C1 = merge_2_st_matching(
        H_relabeled,
        df_matched_paths,
        thres_C=1,
        count_weighted=True)
    matrix_S_sub_nid_C2 = merge_2_st_matching(
        H_relabeled,
        df_matched_paths,
        thres_C=2,
        count_weighted=True)
    matrix_S_sub_nid_C3 = merge_2_st_matching(
        H_relabeled,
        df_matched_paths,
        thres_C=3,
        count_weighted=True)

    # save
    save_variable([matrix_S_sub_nid,
                   matrix_S_sub_nid_C1,
                   matrix_S_sub_nid_C2,
                   matrix_S_sub_nid_C3,
                   ], 'output/LSI/res_linelevel_card_' + suffix + '.pkl')

# -*- coding: utf-8 -*-
"""
Functions for calculating global search information (TSI) according to ref. [1]
(in Results section 2, 3)

[1] Gallotti, R., Porter,  M.  A.  & Barthelemy, M. Lost in transportation:
    Information measures and cognitive limits in multilayer navigation. Science
    Advances 2, e1500445 (2016).

"""

from itertools import islice
import networkx as nx
import numpy as np
import pandas as pd
from networkx.classes.function import path_weight
from funcs import *
from iofiles import *


def shortest_simplest_path(
        sid1,
        line1,
        sid2,
        line2,
        G_relabeled,
        dualG,
        dualG_nodes):
    """
    Get the entropy of finding the fastest simplest path between stations sid1
    and sid2.

    Parameters
    ----------
    sid1 : the id of the origin station.
    line1 : the id of the line where the origin station is located.
    sid2 : the id of the destination station.
    line2 : the id of the line where the destination station is located.
    G_relabeled : the networkx graph of the subway network.
    dualG : the networkx graph of the information network.
    dualG_nodes : the list of nodes in dualG.

    Returns
    -------
    list_paths0 : the fastest simplest path.
    list_pathsturns0 : the transfer stations along the fastest simplest path.
    E : the entropy needed to locate the fastest simplest path in the 
    information network.
    duration : the travel time of the fastest simplest path.
    distance : the travel distance of the fastest simplest path.

    """
    list_paths, list_pathsturns, E0 = dual_shortest_path(dualG, line1, line2)
    for i in range(len(list_paths)):
        list_lines = list_paths[i]
        o_label = str(list_lines[0]) + '-' + str(sid1)
        d_label = str(list_lines[-1]) + '-' + str(sid2)
        if(len(list_paths[i]) == 1):
            stops = get_stops_relabeled(
                o_label, d_label, [list_lines], [
                    list_pathsturns[i]], G_relabeled)
            duration = path_weight(G_relabeled, stops, weight='duration')
            distance = path_weight(G_relabeled, stops, weight='distance')
            list_paths0 = list_paths
            list_pathsturns0 = [list_pathsturns[i]]
        for j in range(len(list_pathsturns[i])):
            list_transfer = list_pathsturns[i][j]
            stops = get_stops_relabeled(
                o_label, d_label, [list_lines], [
                    [list_transfer]], G_relabeled)
            duration0 = path_weight(G_relabeled, stops, weight='duration')
            distance0 = path_weight(G_relabeled, stops, weight='distance')
            if(i == 0 and j == 0 or
               duration > duration0 or
               duration == duration0 and distance > distance0
               ):
                list_paths0 = [list_lines]
                list_pathsturns0 = [[list_transfer]]
                duration = duration0
                distance = distance0
    # Calculate the entropy of finding the fastest simplest path [list_paths0]
    # in dualG
    E = cal_entropy_in_dualG(list_paths0, dualG)
    return list_paths0, list_pathsturns0, E, duration, distance


def network_analysis(
        G_relabeled,
        dualG,
        dualG_nodes,
        mat_width,
        filename=''):
    """
    Get the station-level TSI.
    The station-level TSI measures the information needed to locate the fastest
    simplest paths between station pairs.
    Simplest path: the path with the fewest transfers.

    Parameters
    ----------
    G_relabeled : the subway network.
    dualG : the networkx graph of the information network.
    dualG_nodes : the list of nodes in the dualG.
    mat_width : the width of the result matrix.
    filename : output log name. The default is ''.

    Returns
    -------
    matrix_S : the TSI between each station pair.
    matrix_nroutes : the number of lines included in the fastest simplest path
    of each station pair.
    matrix_pathlength : the travel time of the fastest simplest path of each
    station pair.
    matrix_pathdist : the travel distance of the fastest simplest path of each
    station pair.

    """

    S = 0  # average search information
    matrix_S = np.zeros((mat_width, mat_width)) - 1
    matrix_pathlength = np.zeros((mat_width, mat_width)) - 1
    matrix_pathdist = np.zeros((mat_width, mat_width)) - 1
    matrix_nroutes = np.zeros((mat_width, mat_width)) - 1
    counts = 0
    process = 0
    if(filename == ''):
        filename = "log/dual_sub_simple.txt"
    list_nodes = G_relabeled.nodes()

    for o_label in G_relabeled.nodes:
        for d_label in G_relabeled.nodes:
            counts += 1
            if(int((10 * counts) / (len(list_nodes) * len(list_nodes))) > process):
                process = int((10 * counts) /
                              (len(list_nodes) * len(list_nodes)))
                with open(filename, "a") as f:
                    print(
                        'processing %.2f %%' %
                        (counts * 100 / len(list_nodes) / len(list_nodes)), file=f)
                print('processing %.2f %%'
                      % (counts * 100 / len(list_nodes) / len(list_nodes)))
            try:
                i_s = [int(o_label.split('-')[1]), int(o_label.split('-')[0])]
                j_t = [int(d_label.split('-')[1]), int(d_label.split('-')[0])]
                list_paths, list_pathsturns, E, length, dist = shortest_simplest_path(
                    i_s[0], i_s[1], j_t[0], j_t[1], G_relabeled, dualG, dualG_nodes)
                # number of routes in the shortest path
                nroutes = len(list_paths[0])

                # Store the results of each pair of stations in a matrix with
                # subscripts
                is_update = False
                # If the OD stations have not been calculated, record directly
                if(matrix_pathlength[i_s[0] - 1][j_t[0] - 1] < 0):
                    is_update = True
                # Update if the new path has fewer transfers
                elif(matrix_nroutes[i_s[0] - 1][j_t[0] - 1] > nroutes):
                    is_update = True
                # Update if the new path is shorter in time
                elif(matrix_nroutes[i_s[0] - 1][j_t[0] - 1] == nroutes
                     and matrix_pathlength[i_s[0] - 1][j_t[0] - 1] > length):
                    is_update = True
                # Update if the new path is shorter in distance
                elif(matrix_nroutes[i_s[0] - 1][j_t[0] - 1] == nroutes
                     and matrix_pathlength[i_s[0] - 1][j_t[0] - 1] == length
                     and matrix_pathdist[i_s[0] - 1][j_t[0] - 1] > dist):
                    is_update = True

                if(is_update):
                    matrix_S[i_s[0] - 1][j_t[0] - 1] = E
                    matrix_pathlength[i_s[0] - 1][j_t[0] - 1] = length
                    matrix_pathdist[i_s[0] - 1][j_t[0] - 1] = dist
                    matrix_nroutes[i_s[0] - 1][j_t[0] - 1] = nroutes

            except Exception as e:
                with open(filename, "a") as f:
                    print('(%s,%s): %s'
                          % (o_label, d_label, e), file=f)

    return matrix_S, matrix_nroutes, matrix_pathlength, matrix_pathdist


def get_TSI_snapshot(city_abbr, mat_width, max_line_id, snapshot):
    """
    Get the station-level TSI and line-level TSI under each time snapshot and
    save the results

    Parameters
    ----------
    city_abbr : abbreviation of the city name.
    mat_width : width of result matrix (station-level search information).
    max_line_id :  width of result matrix (line-level search information).
    snapshot : string of a specific year.

    Returns
    -------
    None.

    """
    
    # read the subway network
    G_sub = nx.read_gml('src_data/networks/PrimalGraph_'+city_abbr+'_'+snapshot+'.gml') 
    dualG_sub = nx.read_gml('src_data/networks/DualGraph_'+city_abbr+'_'+snapshot+'.gml', destringizer=int) # read the information network
    print(snapshot, 'data', 'loaded')

    dualG_nodes_sub = list(dualG_sub.nodes(data=True))
    dualG_edges_sub = list(dualG_sub.edges(data=True,keys=True))   

    N_sub = len(set([node.split('-')[1] for node in G_sub.nodes()]))
    N_Ktot = len(nx.Graph(dualG_sub).edges())
    matrix_Ss, matrix_nroutes, matrix_pathlength, matrix_pathdist = network_analysis(
        G_sub, dualG_sub, dualG_nodes_sub, mat_width, filename="log/dual_sub_simple_" + snapshot + ".txt")
    matrix_S_nid = merge_2_st_const_width(
        G_sub,
        matrix_Ss,
        matrix_nroutes,
        max_line_id,
        thres_C=None,
        matrix_Ktot_sub=None)
    matrix_S_nid_C1 = merge_2_st_const_width(
        G_sub, matrix_Ss, matrix_nroutes, max_line_id, thres_C=1)
    matrix_S_nid_C2 = merge_2_st_const_width(
        G_sub, matrix_Ss, matrix_nroutes, max_line_id, thres_C=2)
    matrix_S_nid_C3 = merge_2_st_const_width(
        G_sub, matrix_Ss, matrix_nroutes, max_line_id, thres_C=3)

    save_variable([matrix_Ss,
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
                   matrix_S_nid_C3],
                  'output/TSI/'+city_abbr+'_' + snapshot + '.pkl')

    print('save in', 'output/TSI/'+city_abbr+'_' + snapshot)


if __name__ == "__main__":

    # import network data
    timelines = [
        ['2003', '2004', '2007', '2008', '2009', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'],
        ['2000','2003','2004','2005','2006','2007','2008','2009','2010', '2011','2012','2013','2014','2015','2016','2017','2018','2020'], 
        ['2004','2007','2009','2010','2011','2016','2019','2020']
    ]
    
    files=[['bj','2019_402_284',[-0.00629 , -30.9936]],
        ['sh','2015_431_320',[-0.00228 , -127.7]],
        ['sz','2017_376_248',[-0.00311 , -113.2]]]
        
    city_idx = 0
    city_abbr = files[city_idx][0]
    timeline = timelines[city_idx]
    

    # read the line list
    tb = pd.read_csv('src_data/subway_info/lines_'+city_abbr+'.csv')
    dict_lines = {tb['lineid'].iloc[i]:tb['linename'].iloc[i] for i in range(len(tb))}

    max_line_id = max(dict_lines)
    
    # read the station list
    tb = pd.read_csv('src_data/subway_info/stations_'+city_abbr+'.csv')
    dict_stations = {tb['stationid'].iloc[i]:tb['stationname'].iloc[i] for i in range(len(tb))}
    
    list_nodeid = [x for x in dict_stations]
    mat_width = max(list_nodeid)


    # get TSI under each snapshot and save the results
    for snapshot in timeline:
        get_TSI_snapshot(city_abbr, mat_width, max_line_id, snapshot)

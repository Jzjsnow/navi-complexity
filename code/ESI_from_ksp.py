# -*- coding: utf-8 -*-
"""
Functions for calculating ESI from k shortest paths (in Results section 3)
Steps:
    1. Construct the sub-network for an OD station pair based on k shortest paths.
    2. Calculate the entropy of the path with the largest probability of being 
    chosen (among the k paths) between the OD stations.
    3. The entropy of the chosen path is the station-level ESI of the
    OD stations.
    4. Get the line-level ESI by aggregating the entropy of all the matched paths
    between line pairs.

"""
import networkx as nx
import numpy as np
import pandas as pd
from networkx.classes.function import path_weight
from funcs import *
from iofiles import *


def get_sub_dualG_relabeled(G, dualG_nodes, dualG_edges):
    """
    Map the input subway's sub-network G to an information network.

    Parameters
    ----------
    G : the (sub-)network to map.
    dualG_nodes : the total nodes in the global information network.
    dualG_edges : the total edges in the global information network.

    Returns
    -------
    dualG : the local information network transformed from the sub-network G.
    dualG_nodes_sub : the list of nodes in dualG.
    dualG_edges_sub : the list of edges in dualG.

    """
    H = G.to_undirected()
    dualG_nodes_sub = [x for x in dualG_nodes if x[0] in list(
        set([key for u, v, key in H.edges(keys=True)]))]
    dualG_edges_sub = []
    for sid in H.nodes():
        incident_lines = list(set([int(y.split('-')[0])
                                   for y in list(H[sid])]))
        sid = int(sid.split('-')[1])
        if(len(incident_lines) > 1):  # sid: transfer station
            add_edges = [x for x in dualG_edges if x[2] == sid 
                         and x[0] in incident_lines 
                         and x[1] in incident_lines 
                         and x not in dualG_edges_sub]
            dualG_edges_sub = dualG_edges_sub + add_edges
    dualG = nx.MultiGraph()
    dualG.add_nodes_from(dualG_nodes_sub)
    keys = dualG.add_edges_from(dualG_edges_sub)
    return dualG, dualG_nodes_sub, dualG_edges_sub


def shortest_cost_path_sub(
        o_label,
        d_label,
        G_relabeled,
        dualG,
        dualG_nodes,
        dualG_edges,
        eudistance,
        kmax,
        args):
    """
    Get the entropy of finding the path with minimum cost in kmax shortest paths
    between stations o_label and d_label.

    Parameters
    ----------
    o_label : the origin station identified by the string of "lineid-stationid".
    d_label : the destination station identified by the string of "lineid-
    stationid".
    G_relabeled : the networkx graph of the subway network.
    dualG : the networkx graph of the information network.
    dualG_nodes : the list of nodes in dualG.
    dualG_edges : the list of edges in dualG.
    eudistance : the euclidean distance between origin-destination stations
    kmax : the number of the shortest paths that construct the sub-network.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    
    Returns
    -------
    [list_lines_min] : contains the list of node sequence on the fastest
    simplest path.
    list_pathturns_min : the edge list along the fastest simplest path in
    list_paths.
    E_k : the entropy needed to locate the fastest simplest path in list_paths
    in the local information network tranformed from the sub-network.
    duration : the travel time of the fastest simplest path.
    distance : the travel distance of the fastest simplest path.
    N_Ktot_k : the number of connections in the sub-network.

    """
    list_paths = []  # sequence of stops
    k = 0
    for path in k_shortest_paths(
            nx.DiGraph(G_relabeled),
            o_label,
            d_label,
            kmax,
            weight='duration'):
        k += 1

        list_paths.append(path)
        paths = [key for i in range(0, len(
            path) - 1) for key in G_relabeled.get_edge_data(path[i], path[i + 1]).keys()]  # line id

        list_lines = [paths[i] for i in range(len(paths)) if (
            i == 0 or i > 0 and paths[i] != paths[i - 1])and paths[i] != 0]
        list_pathturns = [path[i] for i in range(
            len(paths)) if i > 0 and paths[i] != paths[i - 1]]

        # get the sub-network and network attributes
        G_sub = G_relabeled.subgraph(
            list(set([x for j in list_paths for x in j]))).copy()

        duration0 = path_weight(G_sub, path, weight='duration')
        distance0 = path_weight(G_sub, path, weight='distance')
        len_path0 = len(list_lines)  # number of lines on the path

        beta = args
        path_cost0 = beta[0]*duration0 + \
                    beta[1]*(1-np.exp(-(len_path0-1)))/eudistance*1000 # eudistance unit: km 
        
        # If the k-th shortest path is a path with fewer costs/transfers(same costs)/distance(same
        # costs & transfers), then the chosen path is updated to this path
        if(k == 1 or
           path_cost0 > path_cost
           ):
            duration = duration0
            distance = distance0
            path_cost = path_cost0
            len_path = len_path0
            list_lines_min = list_lines
            list_pathturns_min = list_pathturns


    dualG_sub, dualG_nodes_sub, dualG_edges_sub = get_sub_dualG_relabeled(
        G_sub, dualG_nodes, dualG_edges)
    N_Ktot_k = len(dualG_sub.edges()) 
    E_k = cal_entropy_in_dualG([list_lines_min], dualG_sub)

    return [list_lines_min], list_pathturns_min, E_k, duration, distance, N_Ktot_k





def subnetwork_analysis(
        G_relabeled,
        dualG,
        dualG_nodes,
        dualG_edges,
        mat_width,
        k,
        dist_dict,
        args,
        filename='dual_log.txt'):
    """
    Get the station-level ESI.
    The station-level ESI measures the information needed to locate the fastest
    simplest paths in the sub-networks between station pairs

    Parameters
    ----------
    G_relabeled : the subway network.
    dualG : the networkx graph of the information network.
    dualG_nodes : the list of nodes in the dualG.
    dualG_edges : the list of edges in dualG.
    mat_width : the width of the result matrix.
    k : the number of the shortest paths that construct the sub-network.
    dist_dict : a dictionary that return the euclidean distance between each 
    station pair.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    filename : output log name. The default is ''.
    
    Returns
    -------
    matrix_S : the ESI between each station pair.
    matrix_nroutes : the number of lines included in the fastest simplest path
    of each station pair.
    matrix_pathlength : the travel time of the fastest simplest path of each
    station pair.
    matrix_pathdist : the travel distance of the fastest simplest path of each
    station pair.
    matrix_Ktot: the number of connections in the sub-networks of each station
    pair.

    """

    S = 0  # average search information
    matrix_S = np.zeros((mat_width, mat_width)) - 1
    matrix_pathlength = np.zeros((mat_width, mat_width)) - 1
    matrix_pathdist = np.zeros((mat_width, mat_width)) - 1
    matrix_nroutes = np.zeros((mat_width, mat_width)) - 1
    matrix_Ktot = np.zeros((mat_width, mat_width)) - 1
    counts = 0
    process = 0

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
                eudistance = dist_dict[(i_s[0],j_t[0])]
    
                list_paths, list_pathsturns, E, length, dist, N_Ktot_k = shortest_cost_path_sub(
                        o_label,
                        d_label,
                        G_relabeled,
                        dualG,
                        dualG_nodes,
                        dualG_edges,
                        eudistance,
                        k,
                        args)
                        
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
                    matrix_Ktot[i_s[0] - 1][j_t[0] - 1] = N_Ktot_k
            except Exception as e:
                with open(filename, "a") as f:
                    print('(%s,%s): %s'
                          % (o_label, d_label, e), file=f)

    return matrix_S, matrix_nroutes, matrix_pathlength, matrix_pathdist, matrix_Ktot


def get_ESI_snapshot(city_abbr, mat_width, max_line_id, snapshot, kmax, dist_dict, args, suffix):
    """
    Get the station-level ESI and line-level GSI under each time snapshot and
    save the results

    Parameters
    ----------
    city_abbr : abbreviation of the city name.
    mat_width : width of result matrix (station-level search information).
    max_line_id :  width of result matrix (line-level search information).
    snapshot : string of a specific year.
    kmax : size of the choice set.   
    dist_dict : a dictionary that return the euclidean distance between each 
    station pair.
    args : the parameters of the choice model (i.e., [beta0,beta1]).
    suffix : suffix of filename
    
    
    """

    G_sub = nx.read_gml('src_data/networks/PrimalGraph_'+city_abbr+'_'+snapshot+'.gml') # read the subway network
    dualG_sub = nx.read_gml('src_data/networks/DualGraph_'+city_abbr+'_'+snapshot+'.gml', destringizer=int) # read the information network
    print(snapshot, 'data', 'loaded')

    dualG_nodes_sub = list(dualG_sub.nodes(data=True))
    dualG_edges_sub = list(dualG_sub.edges(data=True,keys=True))

    matrix_Ss_sub, matrix_nroutes_sub, matrix_pathlength_sub, matrix_pathdist_sub, matrix_Ktot_sub = subnetwork_analysis(
        G_sub, dualG_sub, dualG_nodes_sub, dualG_edges_sub, mat_width, kmax, dist_dict, args, filename="log/log.txt")

    matrix_S_sub_nid, matrix_Ktot_st_sub = merge_2_st_const_width(
        G_sub, matrix_Ss_sub, matrix_nroutes_sub, max_line_id, thres_C=None, matrix_Ktot_sub=matrix_Ktot_sub)
    matrix_S_sub_nid_C1, matrix_Ktot_st_C1_sub = merge_2_st_const_width(
        G_sub, matrix_Ss_sub, matrix_nroutes_sub, max_line_id, thres_C=1, matrix_Ktot_sub=matrix_Ktot_sub)
    matrix_S_sub_nid_C2, matrix_Ktot_st_C2_sub = merge_2_st_const_width(
        G_sub, matrix_Ss_sub, matrix_nroutes_sub, max_line_id, thres_C=2, matrix_Ktot_sub=matrix_Ktot_sub)
    matrix_S_sub_nid_C3, matrix_Ktot_st_C3_sub = merge_2_st_const_width(
        G_sub, matrix_Ss_sub, matrix_nroutes_sub, max_line_id, thres_C=3, matrix_Ktot_sub=matrix_Ktot_sub)

    save_variable([matrix_Ss_sub,
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
                   ],
                  'output/ESI/ksp_' + str(kmax) + '_'+city_abbr+'_' + suffix)
    print('save in', 'output/ESI/ksp_' + str(kmax) + '_'+city_abbr+'_' + suffix)


if __name__ == "__main__":


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
    suffix = files[city_idx][1]
    args = files[city_idx][2]
    timeline = timelines[city_idx]
    
    
    # read the line list
    tb = pd.read_csv('src_data/subway_info/lines_'+city_abbr+'.csv')
    dict_lines = {tb['nid'].iloc[i]:tb['name'].iloc[i] for i in range(len(tb))}
    max_line_id = max(dict_lines)
    
    # read the station list
    tb = pd.read_csv('src_data/subway_info/stations_'+city_abbr+'.csv')
    dict_stations = {tb['sid'].iloc[i]:tb['name'].iloc[i] for i in range(len(tb))}
    list_nodeid = [x for x in dict_stations]
    mat_width = max(list_nodeid)

    
    # read the Euclidean distances between stations
    tb = pd.read_csv('src_data/subway_info/Eudistance_'+city_abbr+'.csv') 
    dict_eudist = {(tb['sid1'].iloc[i],tb['sid2'].iloc[i]):tb['Eudistance'].iloc[i]  for i in range(len(tb))} # Generate a dict() object

    # get ESI under each snapshot and save the results
    for snapshot in timeline:
        get_ESI_snapshot(city_abbr, mat_width, max_line_id, snapshot, 11, dict_eudist, args, snapshot + '.pkl')
        get_ESI_snapshot(city_abbr, mat_width, max_line_id, snapshot, 13, dict_eudist, args, snapshot + '.pkl')
        get_ESI_snapshot(city_abbr, mat_width, max_line_id, snapshot, 15, dict_eudist, args, snapshot + '.pkl')

# -*- coding: utf-8 -*-
"""
Basic functions for calculations in the network.

"""

import math
import pandas as pd
import numpy as np
import networkx as nx
from networkx.classes.function import path_weight
from itertools import islice


def k_shortest_paths(G, source, target, k, weight=None):
    """
    Get the k shortest paths from source to target in G

    Parameters
    ----------
    G : a networkx graph.
    source : the orgin node.
    target : the destination node.
    k : the number of shortest paths.
    weight : the name of the edge attribute to be used as a weight when
    calculating the path length. The default is None.

    Returns
    -------
    A generator that produces lists of the k shortest paths, in order from
    shortest to longest.

    """
    return list(
        islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
    )


def get_od_ksp_attr_all(
        o_label,
        d_label,
        G_relabeled,
        kmax,
        dura_thres):
    """
    Get the attributes of all the shortest paths from station o_label to
    station d_label in the subway network [G_relabeled] whose travel time is
    within the threshold [dura_thres].

    Parameters
    ----------
    o_label : the origin station identified by the string of "lineid-stationid".
    d_label : the destination station identified by the string of "lineid-
    stationid".
    G_relabeled : the networkx graph of the subway network.
    kmax : the max number of shortest paths to get.
    dura_thres : the threshold of the travel time of the paths, exceed which no
    more shortest paths are calculated.

    Returns
    -------
    list_paths : a list of the shortest paths whose travel time is within the threshold.
    list_plen : a list of the travel time of the returned paths.
    list_dist : a list of the path distances of the returned paths.
    list_nroutes : a list of the number of lines on each returned path.
    list_list_lines : a list contains the list of lines on each returned path.
    k : the number of the returned paths.

    """
    list_paths = []
    list_plen = []
    list_dist = []
    list_nroutes = []
    list_list_lines = []
    k = 0
    for path in k_shortest_paths(
            nx.DiGraph(G_relabeled),
            o_label,
            d_label,
            kmax,
            weight='duration'):
        duration = path_weight(G_relabeled, path, weight='duration')
        if(duration > dura_thres):
            break
        k += 1
        list_paths.append(path)
        paths = [key for i in range(0, len(
            path) - 1) for key in G_relabeled.get_edge_data(path[i], path[i + 1]).keys()]  # line ID

        list_lines = [paths[i] for i in range(len(paths)) if (
            i == 0 or i > 0 and paths[i] != paths[i - 1])and paths[i] != 0]
        list_pathturns = [path[i] for i in range(
            len(paths)) if i > 0 and paths[i] != paths[i - 1]]
        distance = path_weight(G_relabeled, path, weight='distance')
        len_path = len(list_lines)
        list_plen.append(duration)
        list_nroutes.append(len_path)
        list_dist.append(distance)
        list_list_lines.append(list_lines)

    return list_paths, list_plen, list_dist, list_nroutes, list_list_lines, k


def dual_shortest_path(G, source, target, ifgetturnseq=True):
    """
    Get all the shortest paths between source and target in the information
    network (dual graph).

    Parameters
    ----------
    G : the networkx graph of the information network.
    source : the origin node in G.
    target : the destination node in G.
    ifgetturnseq : True if the edges along the paths are returned. The default
    is True.

    Returns
    -------
    list_paths : a list of all the shortest paths and the node sequence of each
    path is saved in a list in list_paths.
    list_pathsturns : the edge list along each path in list_paths.
    E : the entropy needed to locate any of the path in list_paths in the
    information network.

    """
    list_paths = list(nx.all_shortest_paths(G, source, target, weight=None))
    p_st_sum = 0
    p_st = 1
    list_pathsturns = []  # edge(transfer station) sequences
    for path in list_paths:  # e.g. path = [1,7,12]
        n_turns = len(path) - 1  # number of transfers
        list_turnsid = []
        # get the transfer sequence of a single path
        if(ifgetturnseq):
            for i in range(0, n_turns):
                # interchange station for Line path[i] and line path[i+1]
                crossings = dict(G[path[i]][path[i + 1]])
                n_crossing_per_line = len(crossings)  # number of transfers
                if(i == 0):
                    for crossing in crossings:
                        list_turnsid.append([crossings[crossing]['sid']])
                else:
                    n_index = 0
                    while(n_index < len(list_turnsid)):
                        list_id = list_turnsid[n_index]
                        # If there is only one path, add the transfer station
                        # directly
                        if(n_crossing_per_line == 1):
                            for crossing in crossings:
                                list_id.append(crossings[crossing]['sid'])
                         # If there are multiple paths, add the transfer
                         # station for each line
                        elif(n_crossing_per_line > 1):
                            for crossing in crossings:
                                list_turnsid.insert(
                                    n_index, list_id + [crossings[crossing]['sid']])
                            del list_turnsid[n_index + n_crossing_per_line]
                        n_index += n_crossing_per_line
            list_pathsturns.append(list_turnsid)
        # the search information for each path
        if(n_turns > 0):
            p_st = 1 / len(G[path[0]])
            for i in range(0, n_turns - 1):
                k_options = len(G[path[i + 1]]) - \
                    1 if len(G[path[i + 1]]) - 1 > 0 else 1
                p_st *= 1 / k_options
        p_st_sum += p_st
    E = -np.log2(p_st_sum)
    return list_paths, list_pathsturns, E


def get_stops_relabeled(
        o_label,
        d_label,
        list_paths,
        list_pathsturns,
        G_relabeled):
    """
    Transform the path in the information network to the path in the subway
    network which is encoded by the sequence of stations.

    Parameters
    ----------
    o_label : the origin station identified by the string of "line number-
    station number".
    d_label : the destination station identified by the string of "line
    number-station number".
    list_paths : the node sequence of the path in the information network.
    list_pathsturns : the edge sequence of the path in the information network.
    G_relabeled : the networkx graph of the subway network.


    Returns
    -------
    stops : the sequences of stations along the path.

    """
    sid1 = int(o_label.split('-')[1])
    sid2 = int(d_label.split('-')[1])
    line1 = int(o_label.split('-')[0])
    line2 = int(d_label.split('-')[0])

    lineid = line1
    G_sub = G_relabeled.edge_subgraph(
        [edge for edge in G_relabeled.edges if edge[2] == lineid])

    if(line1 == line2):
        stops = nx.shortest_path(G_sub, o_label, d_label)

    else:
        lineid = line1
        G_sub = G_relabeled.edge_subgraph(
            [edge for edge in G_relabeled.edges if edge[2] == lineid])
        transfer = list_pathsturns[0][0][0]
        stops = nx.shortest_path(
            G_sub, o_label, str(line1) + '-' + str(transfer))
        for i in range(1, len(list_paths[0]) - 1):
            lineid = list_paths[0][i]
            s1 = list_pathsturns[0][0][i - 1]
            s2 = list_pathsturns[0][0][i]
            G_sub = G_relabeled.edge_subgraph(
                [edge for edge in G_relabeled.edges if edge[2] == lineid])
            stops += nx.shortest_path(G_sub,
                                      str(lineid) + '-' + str(s1),
                                      str(lineid) + '-' + str(s2))

        lineid = line2
        G_sub = G_relabeled.edge_subgraph(
            [edge for edge in G_relabeled.edges if edge[2] == lineid])
        transfer = list_pathsturns[0][0][-1]
        stops += nx.shortest_path(G_sub, str(line2) +
                                  '-' + str(transfer), d_label)
    return stops


def cal_entropy_in_dualG(list_paths, dualG):
    """
    Calculate the entropy of finding a path in the information network (dual
    graph)

    Parameters
    ----------
    list_paths : contains the list of sequence nodes on the path.
    dualG :  a networkx graph of the information network.

    Returns
    -------
    E : the entropy of finding the path.

    """
    path = list_paths[0]
    n_turns = len(path) - 1
    p_st = 1
    if(n_turns > 0):
        p_st = 1 / len(dualG[path[0]])
        for i in range(0, n_turns - 1):
            k_options = len(dualG[path[i + 1]]) - 1 if path[i] != path[i + 2] \
                else len(dualG[path[i + 1]])
            # avoid the cases where the denominator is 0 due to a circular path
            # in the matched paths
            p_st *= 1 / k_options
    E = -np.log2(p_st)
    return E


def merge_2_st_const_width(
        G_relabeled,
        matrix_Ss,
        matrix_nroutes,
        mat_width,
        thres_C=None,
        matrix_Ktot_sub=None):
    """
    Get the line-level GSI by aggregating from the station-level search
    information.
    The aggregation uses the station-level entropy of the fastest simplest
    paths between line pairs and the flow weights are set to 1

    Parameters
    ----------
    G_relabeled : subway network.
    matrix_Ss : station-level search information.
    matrix_nroutes : number of subway lines included in the simplest path from
    station i to j (= number of transfers C + 1).
    mat_width : width of result matrix (line-level search information).
    thres_C : if only the simplest paths with specific number of transfers C
    are used in the calculation, thres_C is set to the number of transfers
    included in the path.
              None - does not filter the number of transfers of the simplest
              paths (all the simplest paths between a pair of subway lines are
              used for averaging).
              The default is None.
    matrix_Ktot_sub : optional. Number of connections in the sub-networks. The
    default is None.

    Returns
    -------
    matrix_S_nid: line-level search information between each line pair.
    matrix_Ktot_sub: average number of connections in the sub-networks of all
    the OD stations between the line pair.

    """

    # line id
    list_nid = list(set([int(node.split('-')[0])
                         for node in G_relabeled.nodes]))
    # station id
    list_sids = [list(set([int(node.split('-')[1])
                           for node in G_relabeled.nodes if int(node.split('-')[0]) == nid])) for nid in list_nid]

    matrix_S_nid = np.zeros((mat_width, mat_width)) * np.nan
    matrix_Ktot_st_sub = np.zeros((mat_width, mat_width)) * np.nan
    for i in range(0, len(list_nid)):
        for j in range(0, len(list_nid)):
            list_sid1 = np.array(list_sids[i]) - 1
            list_sid2 = np.array(list_sids[j]) - 1
            list_S = matrix_Ss[list_sid1, :]
            list_S = list_S[:, list_sid2]
            list_nlines = matrix_nroutes[list_sid1, :]
            list_nlines = list_nlines[:, list_sid2]
            if(matrix_Ktot_sub is not None):
                list_Ktot = matrix_Ktot_sub[list_sid1, :]
                list_Ktot = list_Ktot[:, list_sid2]
                list_Ktot = list_Ktot[list_nlines > 0]
            list_S = list_S[list_nlines > 0]
            list_nlines = list_nlines[list_nlines > 0]
            if(thres_C is None):
                matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                    np.sum(list_S) / (list_S.size)
                if(matrix_Ktot_sub is not None):
                    matrix_Ktot_st_sub[list_nid[i] - 1][list_nid[j] - 1] =  \
                        np.sum(list_Ktot) / list_Ktot.size

            else:
                list_S = list_S[list_nlines == thres_C + 1]
                matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                    np.sum(list_S) / (list_S.size)
                if(matrix_Ktot_sub is not None):
                    list_Ktot = list_Ktot[list_nlines == thres_C + 1]
                    matrix_Ktot_st_sub[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_Ktot) / list_Ktot.size

    if(matrix_Ktot_sub is not None):
        return matrix_S_nid, matrix_Ktot_st_sub
    else:
        return matrix_S_nid


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


def get_matrixC(dualG, dual_nodes, mat_width):
    """
    Get the minimum number of transfers between two subway lines.

    Parameters
    ----------
    dualG :  a networkx graph of the information network.
    dualG_nodes : nodes in the information network dualG.
    mat_width : width of result matrix.

    Returns
    -------
    matrix_C : the minimum number of transfers between each two
    subway lines in dualG.

    """

    list_nodes = list(max(nx.connected_components(dualG), key=len))
    list_cols = []
    for col in np.arange(0, len(dual_nodes)):
        if(dual_nodes[col][0] in list_nodes):
            list_cols.append(col)

    matrix_C = np.zeros((mat_width, mat_width)) - 1
    is_connected = nx.is_connected(dualG)
    p = dict(nx.shortest_path_length(dualG))
    for i in range(0, len(dual_nodes)):
        for j in range(0, len(dual_nodes)):
            if(is_connected is True or dual_nodes[i][0] in list_nodes and dual_nodes[j][0] in list_nodes):
                matrix_C[dual_nodes[i][0] - 1][dual_nodes[j][0] -
                                               1] = p[dual_nodes[i][0]][dual_nodes[j][0]]
    return matrix_C


def merge_2_st_matching_C(
        G_relabeled,
        df_matched_paths,
        max_width,
        thres_C=None,
        count_weighted=False):
    """
    Get the average number of transfers between each two subway
    lines. The aggregation uses the number of transfers and flow
    weights of all the matched paths between line pairs.

    Parameters
    ----------
    G_relabeled : the subway network.
    df_matched_paths : the dataframe containing all the matched paths and
    their search information between station pairs.
                            ('S_sub': entropy of the path calculated in the
                            sub-network.
                            'avg_counts': the number of trips (records)
                            matching the path.)
    max_width : width of result matrix.
    thres_C : if only paths with specific number of transfers C are used in the
    calculation, thres_C is set to the number of transfers included in the
    path. The default is None.
    count_weighted : True if the average values need to be weighted by the flow
    of the paths. The default is False.

    Returns
    -------
    matrix_C : the average number of transfers between each two subway lines.

    """

    list_nid = list(set([int(node.split('-')[0])
                         for node in G_relabeled.nodes]))
    list_sids = [list(set([int(node.split('-')[1])
                           for node in G_relabeled.nodes if int(node.split('-')[0]) == nid])) for nid in list_nid]

    matrix_S_nid = np.zeros((max_width, max_width)) * np.nan
    matrix_C = np.zeros((max_width, max_width)) * np.nan

    for i in range(0, len(list_nid)):
        for j in range(0, len(list_nid)):
            sort_paths = df_matched_paths[(df_matched_paths['i'].isin(np.array(
                list_sids[i]) - 1)) & (df_matched_paths['j'].isin(np.array(list_sids[j]) - 1))]
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
                    matrix_C[list_nid[i] - 1][list_nid[j] - 1] = np.sum(
                        list_nlines * list_count) / np.sum(list_count[list_nlines > 0])

                else:
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S) / list_S.size
                    matrix_C[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_nlines) / list_nlines
            else:
                list_S = list_S[(list_nlines > 0) & (
                    list_nlines == thres_C + 1)]
                list_nlines = list_nlines[(list_nlines > 0) & (
                    list_nlines == thres_C + 1)]

                if(count_weighted):
                    list_count = list_count[(list_nlines > 0) & (
                        list_nlines == thres_C + 1)]
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S * list_count) / np.sum(list_count)
                    matrix_C[list_nid[i] - 1][list_nid[j] -
                                              1] = np.sum(list_nlines * list_count) / np.sum(list_count)
                else:
                    matrix_S_nid[list_nid[i] - 1][list_nid[j] - 1] = \
                        np.sum(list_S) / list_S.size
                    matrix_C[list_nid[i] - 1][list_nid[j] -
                                              1] = np.sum(list_nlines) / list_nlines
    return matrix_C - 1

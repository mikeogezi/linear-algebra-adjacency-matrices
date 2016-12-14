#! /usr/bin/env python
# -*- coding: utf-8 -*-

# metadata
__AUTHOR__ = 'Michael Ogezi'
__DATE__ = '7/12/16'

# constants
NO_ERROR = 0
ERROR = 1
LAMBDA = 'λ'
EPS = 1e-12

import sys
import os
import string
import json

import math as mt
import logging as lg
import warnings as wn

try:
    import numpy as np
except ImportError:
    print 'You need to install numpy to run this script. To install numpy try `pip install numpy`'

    sys.exit(ERROR)

try:
    import networkx as nx
except ImportError:
    print 'You need to install networkx to run this script. To install networkx try `pip install networkx`'

    sys.exit(ERROR)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print 'You need to install matplotlib to run this script. To install matplotlib try `pip install matplotlib`'

    sys.exit(ERROR)

# configuration
np.set_printoptions(
    suppress = True,
    threshold = np.inf
)

# converts the data from the dict into the corresponding adjacency matrix
def get_adjacency_matrix_from_dict (dict_obj):
    total_members = 0
    members = {}
    members_arr = []

    for member_dept in dict_obj['data']:
        for member_name in dict_obj['data'][member_dept]:
            members_arr.append(member_name)

            members[member_name] = {
                # 'name': member_name,
                'dept': member_dept,
                'acquaintances': dict_obj['data'][member_dept][member_name]
            }

        total_members += len(dict_obj['data'][member_dept])

    adjacency_matrix = np.zeros(
        (total_members, total_members),
        dtype = np.uint8
    )

    for count, member in enumerate(members_arr):
        for acquaintance in members[member]['acquaintances']:
            acquaintance_index = members_arr.index(acquaintance)

            # no self loops
            if acquaintance_index == count:
                pass

            if acquaintance_index is not -1:
                # since the matrix is symmetric and the edges are undirected i can do this
                adjacency_matrix[acquaintance_index][count] = 1
                adjacency_matrix[count][acquaintance_index] = 1

    print

    lg.info('The group has %i members\n', total_members)

    lg.info('MEMBERS:\n %s\n', members_arr)
    lg.info('MEMBER DATA:\n %s\n', members)
    lg.info('ADJACENCY MATRIX:\n %s\n', adjacency_matrix)

    return adjacency_matrix, members, members_arr

# read json data file and return as adjacency_matrix dict
def read_json_file (file_path = 'data.json'):
    file_obj = None
    json_data = None
    dict_data = None

    try:
        file_obj = open(file_path)
        lg.info('Successfully opened file %s', file_path)
    except Exception as ex:
        lg.fatal('Error occured while opening file %s: %s', file_path, ex)

        sys.exit(ERROR)

    try:
        json_data = file_obj.read()
        lg.info('Successfully read file')
    except Exception as ex:
        lg.fatal('Error occured while reading file %s: %s', file_path, ex)

        sys.exit(ERROR)

    try:
        dict_data = json.loads(json_data)
        lg.info('Successfully loaded json data into dict')
    except Exception as ex:
        lg.fatal('Error occured while loading json data: %s', ex)

        sys.exit(ERROR)

    return dict_data

# sum eigenvalues
def sum_eig_vals (eig_vals):
    sum = 0

    for i in eig_vals:
        sum += i

    if abs(sum) < EPS and sum < 0:
        return abs(round(sum, 12))

    return round(sum, 12)

# sum squares of eigenvalues
def sum_squares_eig_vals (eig_vals):
    sum = 0

    for i in eig_vals:
        sum += mt.pow(i, 2)

    if abs(sum) < EPS and sum < 0:
        return abs(round(sum, 12))

    return round(sum, 12)

if __name__ == '__main__':
    wn.filterwarnings('ignore')

    lg.basicConfig(
        level = lg.DEBUG,
        format = '%(levelname)s: %(message)s'
    )

    # read json file and generate adjacency matrix from it
    dict_obj = read_json_file('data.json')
    adjacency_matrix, members, members_arr = get_adjacency_matrix_from_dict(dict_obj)

    # compute eigenvalues
    eig_vals, eig_vecs = np.linalg.eig(adjacency_matrix)

    labels = {}
    for i, j in enumerate(members_arr):
        if i >= len(adjacency_matrix):
            break

        labels[i] = j

    # graph
    graph = nx.from_numpy_matrix(adjacency_matrix)
    pos = nx.spring_layout(graph)

    color_dict = {
        'computer_science': '#33a1c9',
        'chemistry': '#ffa500',
        'mathematics': '#dd3232',
        'statistics': '#32cd32',
        'mathematics_education': '#ffc0cb'
    }

    color_dict_darker = {
        'computer_science': '#4682b4',
        'chemistry': '#ff8c00',
        'mathematics': '#ff1010',
        'statistics': '#008000',
        'mathematics_education': '#ffb2b2'
    }

    for index, member_name in enumerate(members_arr):
        # nodes
        node = nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist = [index],
            node_color = color_dict[members[member_name]['dept']],
            node_size = 2000,
            alpha = 1.0
        )

        node.set_edgecolor(color_dict_darker[members[member_name]['dept']])

    # edges
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist = graph.edges(),
        width = 1.0,
        alpha = 1.0,
        edge_color = '#000000'
    )

    # draw
    nx.draw_networkx_labels(
        graph,
        pos,
        labels,
        font_size = 11,
        cmap = plt.get_cmap('jet')
    )

    dp = 3
    for i, eig_val in enumerate(eig_vals):
        if abs(eig_val) < EPS and eig_val < 0:
            eig_val = abs(eig_val)

        lg.info('%s%i = %f', LAMBDA, i + 1, eig_val)
        # lg.info('%s%i = %f, X%i = %s\n', LAMBDA, i + 1, eig_val, i + 1, [round(eig_vec, dp) if abs(eig_vec) > EPS else abs(round(eig_vec, dp))  for eig_vec in eig_vecs[i]])

    print

    lg.info('Sum of Eigenvalues (Trace): %.2f', sum_eig_vals(eig_vals))
    lg.info('Sum of Squares Eigenvalues: %.2f', sum_squares_eig_vals(eig_vals))
    lg.info('Diameter of Graph: %i', nx.diameter(graph))
    lg.info('RMS of Eigenvalues: %.2f', mt.sqrt(sum_squares_eig_vals(eig_vals)))
    lg.info('Frobenius Norm: %.2f', np.linalg.norm(adjacency_matrix, 'fro'))
    lg.info('Number of Nodes: %i', len(graph.nodes()))
    lg.info('Number of Edges: %i', len(graph.edges()))

    fontsize = 15
    plt.text(-0.175, -0.175, 'Sum of Eigenvalues (Trace): %.2f' % sum_eig_vals(eig_vals), fontsize = fontsize)
    plt.text(-0.175, -0.125, 'Sum of Squares Eigenvalues: %.2f' % sum_squares_eig_vals(eig_vals), fontsize = fontsize)
    plt.text(-0.175, -0.075, 'Diameter of Graph: %i' % nx.diameter(graph), fontsize = fontsize)
    plt.text(-0.175, -0.025, 'RMS of Eigenvalues: %.2f' % mt.sqrt(sum_squares_eig_vals(eig_vals)), fontsize = fontsize)
    plt.text(-0.175, +0.025, 'Frobenius Norm: %.2f' % np.linalg.norm(adjacency_matrix, 'fro'), fontsize = fontsize)
    plt.text(-0.175, +0.075, 'Number of Nodes: %i' % len(graph.nodes()), fontsize = fontsize)
    plt.text(-0.175, +0.125, 'Number of Edges: %i' % len(graph.edges()), fontsize = fontsize)

    fig = plt.gcf()
    fig.canvas.set_window_title('Adjacency Graph')
    fig.subplots_adjust(
        bottom = 0.0,
        left = 0.0,
        top = 1.0,
        right = 1.0,
    )

    # display graph
    plt.axis('off')
    plt.show('Adjacency Graph')

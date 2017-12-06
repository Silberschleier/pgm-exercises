# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 14:19:38 2017

@author: Maren
"""


import h5py
import numpy as np
from pprint import pprint
from itertools import product
from copy import deepcopy


def read_data():
    # read pot data
    pot_table = []
    with h5py.File("pot.mat") as f:
        for column in f['pot_table']:
            for row_number in range(len(column)):
                pot_table.append(f[column[row_number]][:])

    #pprint(np.transpose(pot_table))


    # read pot_variables data
    pot_variables = []
    with h5py.File("pot.mat") as f:
        for column in f['pot_variables']:
            for row_number in range(len(column)):
                pot_variables.append(f[column[row_number]][:])

    #pprint(np.transpose(pot_variables))

    # fill a list with variable names
    variables = []
    for i in range(1,21):
        variables.append('d'+str(i))
    for i in range(1,41):
        variables.append('s'+str(i))

    #pprint(variables)

    return pot_table, pot_variables, variables


def moralize(pot_variables):
    new_pot_variables = pot_variables
    for i in range(20,60):
        for pot_var_1 in pot_variables[i]:
            for pot_var_2 in pot_variables[i]:
                if np.in1d(pot_var_2, pot_variables[int(pot_var_1[0])-1], invert=True) and pot_var_2 not in range(21,60):
                    new_pot_variables[int(pot_var_1[0])-1] = np.append(new_pot_variables[int(pot_var_1[0])-1], pot_var_2)
    return new_pot_variables


def clique_graph(pot_variables):
    cliques = {}
    sepsets = {}
    # find all cliques
    ind = 1
    for variable1 in range(len(pot_variables)):
        clique_candidate = []
        clique_candidate.append(variable1+1)
        for variable2 in range(len(pot_variables)):
            # add variable2 to the clique iff it has an edge with every variable already in the clique
            for clique_member in clique_candidate:
                is_member = True
                if np.in1d(variable2+1, pot_variables[int(clique_member)-1], invert=True):
                    is_member = False
                    break
            if is_member:
                clique_candidate.append(variable2+1)
        cliques.update({ str(ind): np.unique(clique_candidate) })
        ind += 1
    # find all sepsets
    for key1 in cliques:
        for key2 in cliques:
            if key1 != key2:
                if np.intersect1d(cliques[key1], cliques[key2]).size != 0:
                    sepsets[(key1, key2)] = np.intersect1d(cliques[key1], cliques[key2])
    return { 'cliques': cliques, 'sepsets': sepsets }


def clique_potentials(cliques, pot_table, pot_variables):
    clique_potentials = {}
    for key in cliques:
        prod = 1
        for var in cliques[key]:
            prod = np.multiply(prod, pot_table[var-1])
        clique_potentials[key] = prod
    return clique_potentials


def pass_messages(cliques, sepsets, clique_potentials):
    updated_clique_potentials = deepcopy(clique_potentials)
    downward_message = pass_downward('1', set(), cliques, sepsets, updated_clique_potentials)
    pass_upward('1', downward_message, set(), cliques, sepsets, updated_clique_potentials)
    return updated_clique_potentials


def get_neighbours(clique_id, sepsets):
    neighbours = []
    for key, value in sepsets.items():
        if key[0] == clique_id:
            neighbours.append(key[1])
        elif key[1] == clique_id:
            neighbours.append(key[0])

    return neighbours


def pass_downward(clique_id, visited, cliques, sepsets, clique_potentials):
    neighbours = get_neighbours(clique_id, sepsets)
    message = clique_potentials[clique_id]
    visited.add(clique_id)
    for neighbour_id in neighbours:
        if neighbour_id in visited:
            continue
        temp_msg = pass_downward(neighbour_id, visited, cliques, sepsets, clique_potentials)
        message = np.multiply(message, temp_msg)

    clique_potentials[clique_id] = message

    return message


def pass_upward(clique_id, message, visited, cliques, sepsets, clique_potentials):
    temp_message = np.multiply(clique_potentials[clique_id], message)
    clique_potentials[clique_id] = temp_message

    neighbours = get_neighbours(clique_id, sepsets)
    visited.add(clique_id)
    for neighbour_id in neighbours:
        if neighbour_id in visited:
            continue
        pass_upward(neighbour_id, temp_message, visited, cliques, sepsets, clique_potentials)


def compute_marginal(var, cliques, clique_potentials):
    for key in cliques:
        if var in cliques[key]:
            return np.sum(np.sum(clique_potentials[key], axis=(0,1)), axis=0)


pot_table, pot_variables, variables = read_data()

#moralize the graph
new_pot_variables_after_moralization = moralize(pot_variables)

# construct junction tree from clique graph
junction_tree = clique_graph(new_pot_variables_after_moralization)

# assign potentials to the cliques
clique_potentials = clique_potentials(junction_tree['cliques'], pot_table, pot_variables)

# pass messages and update clique potentials
updated_clique_potentials = pass_messages(junction_tree['cliques'], junction_tree['sepsets'], clique_potentials)

#return marginals
for var in range(20,60):
    print("Marginal for " + str(variables[var]) + ": " + str(compute_marginal(var, junction_tree['cliques'], clique_potentials)))



# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:55:52 2018

@author: Maren
"""
import numpy as np
from itertools import product

table = { 'fuse': np.array((0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1)),
          'drum': np.array((0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0)),
          'toner': np.array((1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0)),
          'paper': np.array((1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0)),
          'roller': np.array((0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1)),
          'burning': np.array((0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0)),
          'quality': np.array((1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0)),
          'wrinkled': np.array((0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1)),
          'mult_pages': np.array((0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1)),
          'paper_jam': np.array((0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0)),
        }

def learn_prob(var):
    pos = 0
    for val in var:
        if val == 1:
            pos += 1
    return float(pos) / len(var)

def learn_prob_with_one_parent(var, par):
    probs = []
    for val_par in [0, 1]:
        sublist = []
        for i in range(len(var)):
            if par[i] == val_par:
                sublist.append(var[i])
        pos = 0
        for val in sublist:
            if val == 1:
                pos += 1
        if len(sublist) == 0:
            probs.append(0.0)
        else:
            probs.append((np.round((float(pos) / len(sublist)), decimals=4), val_par))
    return probs

def learn_prob_with_two_parents(var, par1, par2):
    probs = []
    for val_par1, val_par2 in product([0, 1], [0, 1]):
        sublist = []
        for i in range(len(var)):
            if par1[i] == val_par1 and par2[i] == val_par2:
                sublist.append(var[i])
        pos = 0
        for val in sublist:
            if val == 1:
                pos += 1
        if len(sublist) == 0:
            probs.append(0.0)
        else:
            probs.append((np.round((float(pos) / len(sublist)), decimals=4), val_par1, val_par2))
    return probs

def learn_prob_with_three_parents(var, par1, par2, par3):
    probs = []
    for val_par1, val_par2, val_par3 in product([0, 1], [0, 1], [0, 1]):
        sublist = []
        for i in range(len(var)):
            if par1[i] == val_par1 and par2[i] == val_par2 and par3[i] == val_par3:
                sublist.append(var[i])
        pos = 0
        for val in sublist:
            if val == 1:
                pos += 1
        if len(sublist) == 0:
            probs.append(0.0)
        else:
            probs.append((np.round((float(pos) / len(sublist)), decimals=4), val_par1, val_par2, val_par3))
    return probs

def backward_probability_one_parent(ev, par, prior, probs):
    for prob in probs:
        if prob[1] == ev:
            likelihood = prob[0]
    evidence = (1-prior)*probs[0][0] + prior*probs[1][0]
    return (likelihood * prior) / evidence

# The first parent variable is the one we want the posterior for
def backward_probability_two_parents(ev, par1, par2, prior1, prior2, probs):
    likelihood = 0
    for prob in probs:
        if prob[1] == ev:
            if prob[2] == 0:
                likelihood += prob[0]*(1-prior2)
            else:
                likelihood += prob[0]*prior2
    evidence = (1-prior1)*(1-prior2)*probs[0][0] + (1-prior1)*prior2*probs[1][0] + prior1*(1-prior2)*probs[2][0] + prior1*prior2*probs[3][0]
    return (likelihood * prior1) / evidence

def prob_fuse_given_evidence():
    prob_burning_given_fuse = learn_prob_with_one_parent(table['burning'], table['fuse'])[1][0]
    prob_paper_jam_given_fuse = learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[2][0]*(1-learn_prob(table['roller'])) + learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[3][0]*learn_prob(table['roller'])
    prob_wrinkled_given_fuse = 1 - (learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[2][0]*(1-learn_prob(table['paper'])) + learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[3][0]*learn_prob(table['paper']))
    likelihood = prob_burning_given_fuse * prob_paper_jam_given_fuse * prob_wrinkled_given_fuse
    prior = learn_prob(table['fuse'])
    prob_burning = learn_prob_with_one_parent(table['burning'], table['fuse'])[0][0]*(1-learn_prob(table['fuse'])) + learn_prob_with_one_parent(table['burning'], table['fuse'])[1][0]*learn_prob(table['fuse'])
    prob_paper_jam = learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[2][0]*(1-learn_prob(table['roller']))*learn_prob(table['fuse']) + learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[3][0]*learn_prob(table['roller'])*learn_prob(table['fuse']) + learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[0][0]*(1-learn_prob(table['roller']))*(1-learn_prob(table['fuse'])) + learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller'])[1][0]*learn_prob(table['roller'])*(1-learn_prob(table['fuse']))
    prob_wrinkled = 1 - (learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[0][0]*(1-learn_prob(table['paper']))*(1-learn_prob(table['fuse'])) + learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[1][0]*learn_prob(table['paper'])*(1-learn_prob(table['fuse'])) + learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[2][0]*(1-learn_prob(table['paper']))*learn_prob(table['fuse']) + learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper'])[3][0]*learn_prob(table['paper'])*learn_prob(table['fuse']))
    evidence = prob_burning * prob_paper_jam * prob_wrinkled
    return (likelihood * prior) / evidence

def _print_table(header, table):
    print "-" * 10 * len(header)
    row_format = "{:>10}" * len(header)
    print row_format.format(*header)
    print "-" * 10 * len(header)

    for row in table:
        print row_format.format(*row)

    print "-" * 10 * len(header)
    print "\n"

if __name__ == '__main__':
    print('\nPart 1\n')
    print('P(Fuse=1): ' + str(learn_prob(table['fuse'])))
    print('P(Drum=1): ' + str(learn_prob(table['drum'])))
    print('P(Toner=1): ' + str(learn_prob(table['toner'])))
    print('P(Paper=1): ' + str(learn_prob(table['paper'])))
    print('P(Roller=1): ' + str(learn_prob(table['roller'])) + '\n')
    
    print('P(Burning | Fuse):')
    _print_table(('Burning=1', 'Fuse'), learn_prob_with_one_parent(table['burning'], table['fuse']))
    print('P(Quality | Drum, Toner, Paper):')
    _print_table(('Quality=1', 'Drum', 'Toner', 'Paper'), learn_prob_with_three_parents(table['quality'], table['drum'], table['toner'], table['paper']))
    print('P(Wrinkled | Fuse, Paper):')
    _print_table(('Wrinkled=1', 'Fuse', 'Paper'), learn_prob_with_two_parents(table['wrinkled'], table['fuse'], table['paper']))
    print('P(Mult_Pages | Paper, Roller):')
    _print_table(('P(M_P=1)', 'Paper', 'Roller'), learn_prob_with_two_parents(table['mult_pages'], table['paper'], table['roller']))
    print('P(Paper_Jam | Fuse, Roller):')
    _print_table(('P(P_J=1)', 'Fuse', 'Roller'), learn_prob_with_two_parents(table['paper_jam'], table['fuse'], table['roller']))
    
    print('\nPart 2\n')
    print('P(Fuse=1 | Burning=Paper_Jam=1, Wrinkled=0):')
    print(prob_fuse_given_evidence())
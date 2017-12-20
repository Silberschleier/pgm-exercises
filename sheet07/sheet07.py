# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 12:32:34 2017

@author: Maren
"""

import random
import numpy as np

def _sample_r(ran):
    if ran <= 0.2:
        return 1
    else:
        return 0
    
def _sample_s(ran):
    if ran <= 0.1:
        return 1
    else:
        return 0

def _sample_j(ran, r):
    if r:
        return 1
    else:
        if ran <= 0.2:
            return 1
        else:
            return 0
    
def _sample_t(ran, r, s):
    if r and s:
        return 1
    elif r and not s:
        return 1
    elif not r and s:
        if ran <= 0.9:
            return 1
        else:
            return 0
    else:
        return 0


# create a sample consistent with the given probability distribution
def create_sample_forward():
    ran_r = random.uniform(0,1)
    ran_s = random.uniform(0,1)
    ran_j = random.uniform(0,1)
    ran_t = random.uniform(0,1)
    sample_r = _sample_r(ran_r)
    sample_s = _sample_s(ran_s)
    sample_j = _sample_j(ran_j, sample_r)
    sample_t = _sample_t(ran_t, sample_r, sample_s)    
    
    return { "r": sample_r, "s": sample_s, "j": sample_j, "t": sample_t }

    
"""
create 1000 samples from the distribution while rejecting all samples
not matching the evidence
"""
def forward_sampling_with_rejection(ev_var, ev_value, no_samples):
    # v: number of valid samples
    v = 0
    # i: number iterations
    i = 0
    samples = []
    while v < no_samples:
        sample = create_sample_forward()
        i += 1
        if sample[ev_var] == ev_value:
            v += 1
            samples.append(sample)
    probs = {}
    for key in ["r", "s", "j", "t"]:
        probs.update({ key : obtain_probability_from_samples(samples, key, 1) })
    return probs, i


"""
modified methods for Gibbs sampling
"""

def _sample_rs_with_probs(ran,prob):
    if ran <= prob:
        return 1
    else:
        return 0

def _sample_j_with_probs(ran, r, probs):
    if r:
        if ran <= probs[1]:
            return 1
        else:
            return 0
    else:
        if ran <= probs[0]:
            return 1
        else:
            return 0
    
def _sample_t_with_probs(ran, r, s, probs):
    if r and s:
        if ran <= probs[3]:
            return 1
        else:
            return 0
    elif r and not s:
        if ran <= probs[2]:
            return 1
        else:
            return 0
    elif not r and s:
        if ran <= probs[1]:
            return 1
        else:
            return 0
    else:
        if ran <= probs[0]:
            return 1
        else:
            return 0


# create a sample consistent with the given probability distribution
def create_sample_forward_with_probs(probs):
    ran_r = random.uniform(0,1)
    ran_s = random.uniform(0,1)
    ran_j = random.uniform(0,1)
    ran_t = random.uniform(0,1)
    sample_r = _sample_rs_with_probs(ran_r, probs['r'])
    sample_s = _sample_rs_with_probs(ran_s, probs['s'])
    sample_j = _sample_j_with_probs(ran_j, sample_r, probs['j'])
    sample_t = _sample_t_with_probs(ran_t, sample_r, sample_s, probs['t'])    
    
    return { "r": sample_r, "s": sample_s, "j": sample_j, "t": sample_t }

"""
modified forward sampling method for gibbs sampling
"""
def forward_sampling_with_variable_probability(ev_var, ev_value, probs):
    # v: valid sample found?
    v = False
    while v == False:
        sample = create_sample_forward_with_probs(probs)
        if sample[ev_var] == ev_value:
            v = True
    return sample

"""
methods for calculating the conditional probabilities
"""

def _prob_r(r,prob):
    """
    :return: p(R=r)
    """
    if r:
        return prob
    return 1-prob


def _prob_s(s,prob):
    """
    :return: p(S=s)
    """
    if s:
        return prob
    return 1-prob


def _prob_j(j, r, probs):
    """
    :param r:
    :return: p(J=j|R=r)
    """
    if r:
        prob = probs[1]
    else:
        prob = probs[0]
    if j:
        return prob
    return 1 - prob


def _prob_t(t, r, s, probs):
    if r and s:
        prob = probs[3]
    elif r and not s:
        prob = probs[2]
    elif not r and s:
        prob = probs[1]
    else:
        prob = probs[0]
    if t:
        return prob
    return 1 - prob


def _clamped_probability(var, ev, probs):
    if var == 'r':
        num = _prob_r(1,probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],1,probs['j'])*_prob_t(ev['t'],1,ev['s'],probs['t'])
        denom = num + (_prob_r(0,probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],0,probs['j'])*_prob_t(ev['t'],0,ev['s'],probs['t']))
        return num / denom
    elif var == 's':
        num = _prob_r(ev['r'],probs['r'])*_prob_s(1,probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])*_prob_t(ev['t'],ev['r'],1,probs['t'])
        denom = num + (_prob_r(ev['r'],probs['r'])*_prob_s(0,probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])*_prob_t(ev['t'],ev['r'],0,probs['t']))
        return num / denom
    elif var == 'j':
        num_a = _prob_j(1,0,probs['j'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_t(ev['t'],ev['r'],ev['s'],probs['t'])
        denom_a = num_a + _prob_j(0,0,probs['j'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_t(ev['t'],ev['r'],ev['s'],probs['t'])
        num_b = _prob_j(1,1,probs['j'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_t(ev['t'],ev['r'],ev['s'],probs['t'])
        denom_b = num_b + _prob_j(0,1,probs['j'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_t(ev['t'],ev['r'],ev['s'],probs['t'])
        a = num_a / denom_a
        b = num_b / denom_b
        if ev['r'] == 0:
            return [(a/(a+b)), probs['j'][1]]
        else:
            return [probs['j'][0], (b/(a+b))]
    else:
        a = _prob_t(1,0,0,probs['t'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])
        b = _prob_t(1,0,1,probs['t'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])
        c = _prob_t(1,1,0,probs['t'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])
        d = _prob_t(1,1,1,probs['t'])*_prob_r(ev['r'],probs['r'])*_prob_s(ev['s'],probs['s'])*_prob_j(ev['j'],ev['r'],probs['j'])
        if ev['r'] == 0 and ev['s'] == 0:
            return [a/(a+b+c+d), probs['t'][1], probs['t'][2], probs['t'][3]]
        if ev['r'] == 0 and ev['s'] == 1:
            return [probs['t'][0], b/(a+b+c+d), probs['t'][2], probs['t'][3]]
        if ev['r'] == 1 and ev['s'] == 0:
            return [probs['t'][0], probs['t'][1], c/(a+b+c+d), probs['t'][3]]
        if ev['r'] == 1 and ev['s'] == 1:
            return [probs['t'][0], probs['t'][1], probs['t'][2], d/(a+b+c+d)]
    
"""
create a probability distribution using Gibbs sampling with evidence
(same parameters as above)
"""
def gibbs_sampling(ev_var, ev_value, iterations):
    # intialize the conditional probablities
    probs = {}
    probs.update({'r': 0.2})
    probs.update({'s': 0.1})
    probs.update({'j': [0.2, 1]})
    probs.update({'t': [0, 0.9, 1, 1]})
    # marginal probabilities
    samples = []
    for i in range(iterations):
        # create a sample using forward sampling, with the current probabilities
        current_sample = forward_sampling_with_variable_probability(ev_var, ev_value, probs)
        samples.append(current_sample)
        for key in probs:
            # the evidential variable is not to be sampled
            if key != ev_var:
                #print("probs:" + str(probs))
                probs.update({key: _clamped_probability(key, current_sample, probs)})
    probs = {}
    for key in ["r", "s", "j", "t"]:
        probs.update({ key : obtain_probability_from_samples(samples, key, 1) })
    return probs

"""
obtain the probability of a variable being a certain value, using the
samples drawn before
"""
def obtain_probability_from_samples(samples, var, value):
    tr = 0
    fa = 0
    for sample in samples:
        if sample[var] == value:
            tr += 1
        else:
            fa += 1
    if tr + fa == 0:
        return 0
    else:
        return (float(tr) / (tr + fa))


if __name__ == '__main__':
    overall_probs_forward = []
    overall_probs_gibbs = []
    for i in range(1,10):
        print("Run: " + str(i))
        print("\nForward sampling:")
        probs, i = forward_sampling_with_rejection("t", 1, 1000)  
        print("\nNumber iterations until 1000 valid samples are completed: " + str(i))
        print("\nP(S = 1 | T = 1) = " + str(probs["s"]))
        overall_probs_forward.append(probs["s"])
        
        print("\n-----------------------------------------")
        print("Gibbs sampling:")
        probs = gibbs_sampling("t", 1, 1000)
        print("\nP(S = 1 | T = 1) = " + str(probs["s"]))
        overall_probs_gibbs.append(probs["s"])
        print("\n-----------------------------------------")
    print("\nMean of all runs:\n")
    print("\nForward sampling:")
    print("\nP(S = 1 | T = 1) = " + str(np.mean(overall_probs_forward)))
    print("\nGibbs sampling:")
    print("\nP(S = 1 | T = 1) = " + str(np.mean(overall_probs_gibbs)))
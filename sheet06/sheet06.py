# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 14:19:38 2017

@author: Maren
"""


import h5py
import csv
import numpy as np

# read pot data
data = []
with h5py.File("pot.mat") as f:
    for column in f['pot_table']:
        for row_number in range(len(column)):             
            data.append(f[column[row_number]][:])

print data
print np.transpose(data)




# read pot_variables data
data = []
with h5py.File("pot.mat") as f:
    for column in f['pot_variables']:
        for row_number in range(len(column)):            
            data.append(f[column[row_number]][:])
print data
print np.transpose(data)

with open('pot_variables.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(data)
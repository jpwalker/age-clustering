'''
Created on Aug 22, 2013

@author: jpwalker
'''

from IO import *
import numpy as np
from compute_nu import *
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcdefaults
import os

if __name__ == '__main__':
    h = 0.73
    z = 0 #Update the redshift
    #Cosmology for MS and MS2
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} 
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/snap67/attempt1_fof_form_jp/'.format(home)
    ifile = 'properties.dat'
    agelabel = 'Sub-Max_tree-Assem. Age'
    data = readfile('{0}{1}'.format(direc, ifile), col = 28, delim = ' ', skip = 1)
    age_bins = 5
    mass_bins = 7
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
    for age_i in range(0, age_bins + 1):
        bias = []
        mass = []
        for mass_i in range(1, mass_bins + 1):
            b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
            idx1 = np.where(np.logical_and(b_data[0] >= 5, b_data[0] <= 25))[0]
            idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
            bias.append(np.sum(b_data[1][idx1]) / len(b_data[1][idx1]))
            mass.append(data[4][idx2][0])
        bias = np.array(bias)
        mass = np.array(mass)
        plt.plot(compute_nu(mass * massconv / h, z, cosmo), bias, color = col_j[age_i], label = '{0}_{1}'.format(agelabel, age_i))
    rc('text', usetex = True)
    plt.xlabel('$\\nu$')
    plt.ylabel('$b$')
    rcdefaults()
    plt.legend()
    plt.show()
    plt.show()
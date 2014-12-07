'''
Created on Aug 22, 2013

@author: jpwalker
'''

from IO import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import rcdefaults
import os

def plot_b_M(k, direc, prop_fname, agelabel):
    data = readfile('{0}{1}'.format(direc, prop_fname), col = 28, delim = '    ', skip = 1)
    age_bins = 5
    mass_bins = 8
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
    for age_i in range(0, age_bins + 1):
        bias = []
        mass = []
        for mass_i in range(1, mass_bins + 1):
            b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), 
                              col = 2, delim = ',', skip = 1)
            idx1 = np.where(np.logical_and(b_data[0] >= 5, b_data[0] <= 15))[0]
            idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
            bias.append(np.sum(b_data[1][idx1]) / len(b_data[1][idx1]))
            mass.append(data[4][idx2][0])
        bias = np.array(bias)
        mass = np.array(mass)
        k.semilogx(mass * massconv / h, bias, color = col_j[age_i], 
                     label = '{0}_{1}'.format(agelabel, age_i))
    rc('text', usetex = True)
    k.set_xlabel('Mass [M$_\\odot$]',size = 'large')
    k.set_ylabel('$b$', size = 'large')
    rcdefaults()
    k.legend(fontsize = 12.0)

if __name__ == '__main__':
    h = 0.73
    massconv = 6.885E6 #Mass conversion reports mass in M_sun/h
    home = '{0}/'.format(os.environ['HOME'])
    base_dir = '{0}Desktop/age-clustering-data/'.format(home)
    snap = '67'
    ident = '-1'
    snap_dir = '{0}snap{1}{2}/'.format(base_dir, snap, ident)
    direcs = ('{0}attempt1_fof_form_gao/'.format(snap_dir), 
              '{0}attempt1_fof_form_jp/'.format(snap_dir),
              '{0}attempt1_sub_form_jp/'.format(snap_dir),
              '{0}attempt1_sub_assem_jp/'.format(snap_dir))
    agelabels = ('FOF-Form. Age-Root', 'FOF-Form. Age-Max', 
                 'Sub-Form. Age-Max', 'Sub-Assem.-Max')
    ifile = 'properties.dat'
    (fig, ax) = plt.subplots(2, 2)
    for (i, l) in enumerate(ax):
        for (j, k) in enumerate(l):
            idx = i + 2 * j
            k.set_ylim([0.35, 1.65])
            k.set_xlim([5E9, 4E12])
            plot_b_M(k ,direcs[idx], ifile, agelabels[idx])
    plt.show()
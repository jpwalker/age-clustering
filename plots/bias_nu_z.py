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
from matplotlib import axes
import os

def plot_seljak_warren(M_low, M_high, cosmo):
    M = np.logspace(M_low, M_high, 1000)
    M_star = compute_Mstar(0, cosmo)
    x = M * 1.5 / M_star
    b = 0.53 + 0.39 * x**0.45 + 0.13 / (40 * x + 1) + 5E-4 * x**1.5 + np.log10(x) * \
    (0.4 * (cosmo['omega_M_0'] - 0.3 + cosmo['n'] - 1) + 0.3 * (cosmo['sigma_8'] - 0.9 + cosmo['h'] -.7))
    
    nu = compute_nu(M, 0, cosmo)
    return (nu, b)

if __name__ == '__main__':
    h = 0.73
    snaps = (22, 27, 36, 40, 45, 51, 67)
    symbs = ('o', '^', 'v', 'D', 's', '*', 'p')
    snap_id = '-1'
    z = (6.196857, 4.179475, 2.0700316, 1.5036374, 0.98870987, 0.5641763, 0) #Update the redshift
    ##Create figure and axes to create both the regular plot and the subpanel
    fig = plt.figure()
    st_ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    sp_ax = fig.add_axes([0.17, 0.45, 0.40, 0.45])
    #Cosmology for MS and MS2
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} 
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    home = '{0}/'.format(os.environ['HOME'])
    (nu, b) = plot_seljak_warren(9, 15.45, cosmo)
    st_ax.plot(nu, b, 'k--')
    sp_ax.plot(nu, b, 'k--')
    age_bins = 5
    mass_bins = 7
    ifile = 'properties.dat'
    agelabel = 'Sub-Max-Form. Age'
    for (i, s) in enumerate(snaps):
        snap_dir = 'snap{0}{1}'.format(s, snap_id)
        direc = '{0}Desktop/age-clustering-data/{1}/attempt1_sub_form_jp/'.format(home, snap_dir)
        data = readfile('{0}{1}'.format(direc, ifile), col = 28, delim = '    ', skip = 1)
        col_j = ['k', 'b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
        for age_i in range(0, age_bins + 1):
            bias = []
            mass = []
            for mass_i in range(1, mass_bins + 1):
                b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
                idx1 = np.where(np.logical_and(b_data[0] >= 5, b_data[0] <= 15))[0]
                idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
                bias.append(np.sum(b_data[1][idx1]) / len(b_data[1][idx1]))
                mass.append(data[4][idx2][0])
            bias = np.array(bias)
            mass = np.array(mass)
            st_ax.plot(compute_nu(mass * massconv / h, z[i], cosmo), bias, symbs[i], color = col_j[age_i], \
                     label = '{0}, Q: {1}, z:{2}'.format(agelabel, age_i, z[i]))
            sp_ax.plot(compute_nu(mass * massconv / h, z[i], cosmo), bias, symbs[i], color = col_j[age_i])
    sp_ax.set_xlim([0.3, 1.22])
    sp_ax.set_ylim([0.25, 1.75])
    st_ax.set_xlim([0.3, 3.1])
    st_ax.set_ylim([0.25, 8.5])
    rc('text', usetex = True)
    st_ax.set_xlabel('$\\nu$')
    st_ax.set_ylabel('$b$')
    #st_ax.legend()
    rcdefaults()
    plt.show()
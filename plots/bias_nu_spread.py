'''
Created on Jan 13, 2015

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

#Cosmology for MS and MS2
cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
         'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}

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
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    home = '{0}/'.format(os.environ['HOME'])
#     (nu, b) = plot_seljak_warren(9, 15.45, cosmo)
#     st_ax.plot(nu, b, 'k--')
#     sp_ax.plot(nu, b, 'k--')
    age_bins = 5
    mass_bins = 7
    ifile = 'properties.dat'
    agelabel = 'Sub-Max-Form. Age'
    age_dir = 'attempt1_sub_form_jp'
    bias_upper = np.empty(0)
    bias_lower = np.empty(0)
    nu = np.empty(0)
    for (i, s) in enumerate(snaps):
        snap_dir = 'snap{0}{1}'.format(s, snap_id)
        direc = '{0}Desktop/age-clustering-data/{1}/{2}/'.format(home, snap_dir,
                                                                 age_dir)
        data = readfile('{0}{1}'.format(direc, ifile), col = 28, 
                        delim = '    ', skip = 1)
        for mass_i in range(1, mass_bins + 1):
            bias_temp = []
            for age_i in range(0, age_bins + 1):
                b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, 
                                                                age_i), col = 2,
                                   delim = ',', skip = 1)
                idx1 = np.where(np.logical_and(b_data[0] >= 5,
                                                b_data[0] <= 15))[0]
                idx2 = np.where(np.logical_and(data[0] == mass_i,
                                                data[1] == age_i))[0]
                if age_i != 0:
                    bias_temp.append(np.sum(b_data[1][idx1]) / len(b_data[1][idx1]))
                else:
                    n = compute_nu(data[4][idx2][0] * massconv / h, z[i], 
                                         cosmo)
                    nu = np.append(nu, n)
                    cent_bias = np.sum(b_data[1][idx1]) / len(b_data[1][idx1])
            bias_upper = np.append(bias_upper, max(bias_temp))
            bias_lower = np.append(bias_lower, min(bias_temp))
            if symbs[i] == 'p' or symbs[i] == '*':
                symsize = 5.
            else:
                symsize = 4.  
            st_ax.plot(nu[-1], 
                       cent_bias, symbs[i], color = 'k', 
                       label = '{0}, Q: {1}, z:{2}'.format(agelabel, age_i, z[i]), 
                       ms = symsize)
            sp_ax.plot(nu[-1], 
                       cent_bias, symbs[i], color = 'k', ms = symsize)
    sp_ax.set_xlim([0.3, 1.22])
    sp_ax.set_ylim([0.25, 1.75])
    st_ax.set_xlim([0.3, 3.1])
    st_ax.set_ylim([0.25, 8.5])
    idx = np.argsort(nu)
    nu = nu[idx]
    bias_upper = bias_upper[idx]
    bias_lower = bias_lower[idx]
    sp_ax.fill_between(nu, bias_upper, bias_lower, color = 'k', alpha = 0.05)
    st_ax.fill_between(nu, bias_upper, bias_lower, color = 'k', alpha = 0.05)
    rc('text', usetex = True)
    st_ax.set_xlabel('$\\nu$', fontsize = 18)
    st_ax.set_ylabel('$b$', fontsize = 18)
    rcdefaults()
    plt.show()
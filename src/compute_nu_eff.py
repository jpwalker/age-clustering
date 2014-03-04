'''
Created on Feb 18, 2014

@author: jpwalker
'''

import numpy as np
import compute_nu as n
import os
from IO import readfile

def calc_nu_eff(nu, bias, nu_med, bias_med):
    

def calc_seljak_warren(num, cosmo):
    M_low = 1E9
    M_high = 1E15
    M = np.logspace(M_low, M_high, num)
    M_star = n.compute_Mstar(0, cosmo)
    x = M * 1.5 / M_star
    b = 0.53 + 0.39 * x**0.45 + 0.13 / (40 * x + 1) + 5E-4 * x**1.5 + np.log10(x) * \
    (0.4 * (cosmo['omega_M_0'] - 0.3 + cosmo['n'] - 1) + 0.3 * (cosmo['sigma_8'] - 0.9 + cosmo['h'] -.7))
    nu = n.compute_nu(M, 0, cosmo)
    return (nu, b)
    

if __name__ == '__main__':
    mass_i = (1) ##INPUT
    age_i = (5) ##INPUT
    home = '{0}/'.format(os.environ['HOME'])
    finaldir = 'snap67/attempt1_sub_form_gao/' ##INPUT
    curr_age_dir = '{0}/Desktop/age-clustering-data/{1}'.format(home, finaldir)
    propfile = 'properties.dat'
    agelabel = 'Sub-Max_tree-Form. Age' ##INPUT
    ##Read in Properties file
    data = readfile('{0}{1}'.format(curr_age_dir, propfile), col = 28, delim = '    ', skip = 1)
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
    (nu_no_age, bias_no_age)  = calc_seljak_warren(10000, cosmo)
    calc_nu_eff()
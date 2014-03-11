'''
Created on Feb 18, 2014

@author: jpwalker
'''

import numpy as np
import compute_nu as n
import os
from IO import readfile
import scipy.interpolate as inter
import matplotlib.pyplot as plt

def calc_nu_eff(nu, bias, nu_med, bias_med):
    if not (nu < min(nu_med) or nu > max(nu_med) or bias < min(bias_med) or bias > max(bias_med)):
        if len(bias_med) == len(nu_med):
            #Produce Spline function 
            nu_func = inter.interp1d(bias_med, nu_med, kind = 'slinear')
            return nu_func(bias)
        else:
            print 'Check your median bias and nu vectors.'
            raise IndexError
    else:
        print 'Given nu and bias are out of bounds.'
        return None

def calc_seljak_warren(num, cosmo):
    M_low = 9
    M_high = 15
    M = np.logspace(M_low, M_high, num)
    M_star = n.compute_Mstar(0, cosmo)
    x = M * 1.5 / M_star
    b = 0.53 + 0.39 * x**0.45 + 0.13 / (40 * x + 1) + 5E-4 * x**1.5 + np.log10(x) * \
    (0.4 * (cosmo['omega_M_0'] - 0.3 + cosmo['n'] - 1) + 0.3 * (cosmo['sigma_8'] - 0.9 + cosmo['h'] -.7))
    nu = n.compute_nu(M, 0, cosmo)
    return (nu, b)

def calc_bias(direc, mass_i, age_i):
    b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
    #Find the bias values between 5 and 15 Mpc / h
    idx1 = np.where(np.logical_and(b_data[0] >= 5, b_data[0] <= 15))[0]
    return np.sum(b_data[1][idx1]) / len(b_data[1][idx1])

def nu_eff(finaldir, age_i, age_label, massbins, cosmo, z):
    h = 0.73
    mass_conv = 6.8e6
    propfile = 'properties.dat'
    home = '{0}/'.format(os.environ['HOME'])
    curr_age_dir = '{0}/Desktop/age-clustering-data/{1}'.format(home, finaldir)
    ##Read in Properties file
    data = readfile('{0}{1}'.format(curr_age_dir, propfile), col = 28, delim = '    ', skip = 1)
    (nu_no_age, bias_no_age)  = calc_seljak_warren(1000, cosmo)
    ret_array = ([],[],[],[])
    for mass_i in range(1, massbins + 1):
        idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
        med_mass = data[4][idx2][0]
        nu_age = n.compute_nu(med_mass * mass_conv, z, cosmo)
        bias_age = calc_bias(curr_age_dir, mass_i, age_i)
        ret_array[0].append(nu_age)
        ret_array[1].append(bias_age)
        ret_array[2].append(calc_nu_eff(nu_age, bias_age, nu_no_age, bias_no_age))
        ret_array[3].append()
        
        
         
if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    z = 0 #INPUT
    
    finaldir = 'snap67/attempt1_sub_form_gao/' ##INPUT
    
    
    agelabel = 'Sub-Max_tree-Form. Age' ##INPUT
    
    
    
    
    
    
    plt.plot(nu_no_age, bias_no_age, '+')
    plt.plot(nu_age, bias_age, '*k')
    plt.hlines(bias_age, plt.xlim()[0], plt.xlim()[1])
    plt.vlines(nu_age, plt.ylim()[0], plt.ylim()[1])
    plt.vlines(nu_eff, plt.ylim()[0], plt.ylim()[1])
    plt.show()
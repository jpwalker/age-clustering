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
            try:
                return nu_func(bias)
            except ValueError:
                print 'Check (nu, bias) values: ({0}, {1})'.format(nu, bias)
                return None
        else:
            print 'Check your median bias and nu vectors.'
            raise IndexError
    else:
        print 'Given nu and bias are out of bounds.'
        return None

def calc_seljak_warren(num, cosmo):
    M_low = 9
    M_high = 16
    M = np.logspace(M_low, M_high, num)
    M_star = n.compute_Mstar(0, cosmo)
    x = M * 1.5 / M_star
    b = 0.53 + 0.39 * x ** 0.45 + 0.13 / (40. * x + 1.) + 5E-4 * x ** 1.5 
    #b = 0.53 + 0.39 * x**0.45 + 0.13 / (40 * x + 1) + 5E-4 * x**1.5 + np.log10(x) * \
    #(0.4 * (cosmo['omega_M_0'] - 0.3 + cosmo['n'] - 1) + 0.3 * (cosmo['sigma_8'] - 0.9 + cosmo['h'] -.7)) ##modified Seljak and Warren
    nu = n.compute_nu(M, 0, cosmo)
    return (nu, b)

def calc_bias(direc, mass_i, age_i):
    b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
    #Find the bias values between 5 and 15 Mpc / h
    idx1 = np.where(np.logical_and(b_data[0] >= 5, b_data[0] <= 15))[0]
    return np.sum(b_data[1][idx1]) / len(b_data[1][idx1])

def nu_eff(finaldir, age_i, massbins, cosmo, z):
    h = 0.73
    mass_conv = 6.8e6
    propfile = 'properties.dat'
    ##Read in Properties file
    data = readfile('{0}{1}'.format(finaldir, propfile), col = 28, delim = '    ', skip = 1)
    (nu_no_age, bias_no_age)  = calc_seljak_warren(1000, cosmo)
    ret_array = [[], [], [], [], [], []]
    for mass_i in range(1, massbins + 1):
        idx1 = np.where(np.logical_and(data[0] == mass_i, data[1] == 0))[0]
        median_age_no_age = data[25][idx1][0] ##Median age without age selection in one mass bin
        idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
        med_age = data[25][idx2][0] ##median age of mass-age selection
        med_mass = data[4][idx2][0] ##median mass of mass bin 
        nu_age = n.compute_nu(med_mass * mass_conv / h, z, cosmo)
        bias_age = calc_bias(finaldir, mass_i, age_i)
        nu_ef = calc_nu_eff(nu_age, bias_age, nu_no_age, bias_no_age)
        if nu_ef != None:
            ret_array[0].append(mass_i)
            ret_array[1].append(age_i)
            ret_array[2].append(nu_age) ##nu of age-mass selection
            ret_array[3].append(bias_age) ## bias of age-mass selection
            ret_array[4].append(nu_ef) ##nu-eff for age-mass
            ret_array[5].append(med_age)# / median_age_no_age)
    for i in range(6):
        ret_array[i] = np.array(ret_array[i])
    return (ret_array[0], ret_array[1], ret_array[2], ret_array[3], ret_array[4], ret_array[5])
         
if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    z =  2.0700316 #INPUT
    home = '{0}/'.format(os.environ['HOME'])
    finaldir = '{0}Desktop/age-clustering-data/snap36/attempt1_sub_form_gao/'.format(home) ##INPUT
    agelabel = 'Sub-Root-Form. Age' ##INPUT
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
    (nu_no_age, bias_no_age)  = calc_seljak_warren(1000, cosmo)
    nu_res = []
    for age_i in range(1,6):
        nu_res.append(nu_eff(finaldir, age_i, 7, cosmo, z))
#         plt.plot(nu_no_age, bias_no_age, 'k')
#         plt.plot(nu_res[-1][0], nu_res[-1][1], color = col_j[age_i], 
#                  label = '{0}_{1}'.format(agelabel, age_i))
#         plt.hlines(nu_res[-1][1], nu_res[-1][0], nu_res[-1][2])
#         plt.vlines(nu_res[-1][0], plt.ylim()[0], plt.ylim()[1])
#         plt.vlines(nu_res[-1][2], plt.ylim()[0], plt.ylim()[1])
        x = nu_res[-1][2]
        y = nu_res[-1][4]# - nu_res[-1][2]
        plt.plot(x, y, '+',
                 color = col_j[age_i], label = '{0}_{1}'.format(agelabel, age_i))
        for (i, txt) in enumerate(nu_res[-1][0]):
            plt.text(x[i], y[i], txt)
    plt.xlabel('nu')
    plt.ylabel('nu_eff')
    plt.legend()
    plt.show()
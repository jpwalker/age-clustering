'''
Created on Feb 18, 2014

@author: jpwalker
'''

import numpy as np
import compute_nu as n
import os
from IO import readfile
import scipy.interpolate as inter
from scipy.stats import linregress
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

def nu_eff(finaldir, age_i, massbins, cosmo, z, nu_no_age, bias_no_age):
    h = 0.73
    mass_conv = 6.8e6
    propfile = 'properties.dat'
    ##Read in Properties file
    data = readfile('{0}{1}'.format(finaldir, propfile), col = 28, delim = '    ', skip = 1)
    ret_array = np.array([[],[],[],[],[],[]])
    for mass_i in range(1, massbins + 1):
        idx2 = np.where(np.logical_and(data[0] == mass_i, data[1] == age_i))[0]
        med_age = data[25][idx2][0] ##median age of mass-age selection
        med_mass = data[4][idx2][0] ##median mass of mass bin 
        nu_age = n.compute_nu(med_mass * mass_conv / h, z, cosmo) #Calculate nu for the median  mass
        bias_age = calc_bias(finaldir, mass_i, age_i) #Calculate bias from crosscorrelations 
        nu_ef = calc_nu_eff(nu_age, bias_age, nu_no_age, bias_no_age) #Calculate nu effective based on nu and bias(nu) without age
        if nu_ef != None:
            nu_ef = -100000 #If nu effective is not found then it is set to a large negative number 
        ret_array[0].append(mass_i)
        ret_array[1].append(age_i)
        ret_array[2].append(nu_age) # nu of age-mass selection
        ret_array[3].append(bias_age) # bias for age-mass selection
        ret_array[4].append(nu_ef) # nu-eff for age-mass
        ret_array[5].append(med_age)# median age for age-mass
    for i in range(6):
        ret_array[i] = np.array(ret_array[i])
    return (ret_array[0], ret_array[1], ret_array[2], ret_array[3], ret_array[4], ret_array[5])
         
if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    zs =  [6.196857, 4.179475, 2.0700316, 0.98870987, 0] #INPUT
    home = '{0}/'.format(os.environ['HOME'])
    snaps = [22, 27, 36, 45, 67]
    xtot = []
    ytot = []
    (nu_no_age, bias_no_age)  = calc_seljak_warren(1000, cosmo)
    for (t, s) in enumerate(snaps):
        z = zs[t]
        finaldir = '{0}Desktop/age-clustering-data/snap{1}/attempt1_sub_form_jp/'.format(home, s) ##INPUT
        agelabel = 'Sub-Root-Form. Age' ##INPUT
        col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
        
        nu_res = []
        for age_i in range(0,6):
            x = np.array([])
            if age_i == 0:
                temp = nu_eff(finaldir, age_i, 7, cosmo, z, nu_no_age, bias_no_age)
                median_age = temp[5]
                mass_i_median_age = temp[0]
            else:
                nu_res.append(nu_eff(finaldir, age_i, 7, cosmo, z, nu_no_age, bias_no_age))
                print nu_res[-1][5]
                print median_age
                for (idx, x_temp) in enumerate(nu_res[-1][5]):
                    idx2 = np.where(mass_i_median_age == nu_res[-1][0][idx])[0]
                    x = np.append(x, x_temp / median_age[idx2]) #nu_res[-1][2] 
                    y = (nu_res[-1][4] - nu_res[-1][2]) / nu_res[-1][2] # - nu_res[-1][2]
                xtot.extend(x)
                ytot.extend(y)
                txt = nu_res[-1][0]
                plt.plot(x, y, '+', 
                         color = col_j[age_i], label = '{0}_{1}_{2}'.format(agelabel, s, age_i))
                for (i, txt) in enumerate(nu_res[-1][0]):
                    plt.text(x[i], y[i], txt)
    #xtot = np.array(xtot)
    #ytot = np.array(ytot)
    #(slope, intercept, rval, pval, stderr) = linregress(xtot, ytot)
    #plt.plot(xtot, xtot * slope + intercept , 'r')
    #plt.plot([0, 0], [10, 0], '--k')
    plt.xlabel('nu')
    plt.ylabel('(nu_eff - nu)  / nu')
    #plt.legend()
    plt.show()
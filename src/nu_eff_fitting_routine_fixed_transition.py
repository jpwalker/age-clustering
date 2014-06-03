'''
Created on Apr 20, 2014
Fit nu_eff(nu) with a fixed transition in the break off.
@author: jpwalker
'''

import numpy as np
import os
import compute_nu_eff as cmpn
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from math import exp

def fitting_func1((A, B), ls, rs, B1, ages):
    print A, B
    nu0 = A * np.exp(B * ages)
    #ls =nu and rs=nu_eff
    ret = []
    for i in range(len(ls)):
        x = ls[i] - nu0[i]
        y = rs[i] - nu0[i]
        try:
            e = exp(-B1 * x)
        except OverflowError:
            e = 1E100
        ret.append(y - x / (1. + e))
    return ret

def fitting_func2((m1, b1, m2, b2), ls, rs, B):
    #ls =nu and rs=nu_eff
    ret = np.zeros(len(ls), dtype = np.float64)
    if (m2 - m1) != 0:
        nu0 = (b1 - b2) / (m2 - m1)
    else:
        nu0 = 20.
    x = ls - nu0
    for i in range(len(ls)):
        g = 1. / (1. + exp(-B * x[i]))
        ret[i] = rs[i] - (m2 * ls[i] + b2 + ((m1 - m2) * ls[i] + b1 - b2) * g)
    return ret

def param_fit_func((A, B, C), x, y):
    ret = np.zeros(len(x), dtype = np.float64)
    for i in range(len(x)):
        ret[i] = y[i] - (A * exp(B * x[i]) + C)
    return ret
    
if __name__ == '__main__':
    fixed_transition_model = 300.
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    zs =  [6.196857, 4.179475, 2.0700316, 0.98870987, 0] #INPUT
    z_points = ['o', '^', 'v', 's', 'p'] ##Predefined points for redshift
    snaps = [22, 27, 36, 45, 67]
    home = '{0}/'.format(os.environ['HOME'])
    snap_identifier = '-1'
    (nu_no_age, bias_no_age)  = cmpn.calc_seljak_warren(1000, cosmo)
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
    
    ##Folowing variables are used to find the median age of a mass_i, snap sample.
    median_age = np.empty(0, dtype = float)
    mass_i_median_age = np.empty(0, dtype = float)
    snap_median_age = np.empty(0, dtype = int)
    
    #Properties for the mass-age sample across all redshifts.
    param = [] 
    tot_age = np.empty(0, dtype = float)
    tot_nueff = np.empty(0, dtype = float)
    tot_nu = np.empty(0, dtype = float)
    tot_z = np.empty(0, dtype = float)
    for age_i in range(0,6): #Step through age_i
        #Properties for each age_i seperately
        medianage_agei = np.empty(0, dtype = float)
        ages_agei = np.empty(0, dtype = float)
        nu_agei = np.empty(0, dtype = float) 
        nueff_agei = np.empty(0, dtype = float)
        z_agei = np.empty(0, dtype = float)
        for (t, s) in enumerate(snaps): #Step through redshift
            z = zs[t]
            pnt = z_points[t]
            finaldir = '{0}Desktop/age-clustering-data/snap{1}{2}/attempt1_sub_form_gao/'.format(home, s, snap_identifier) ##INPUT
            agelabel = 'Sub-Root-Form. Age' ##INPUT ##Label for age definition
            if age_i == 0:
                temp = cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age)
                median_age = np.append(median_age, temp[5])
                mass_i_median_age = np.append(mass_i_median_age, temp[0])
                snap_median_age = np.append(snap_median_age, np.ones(len(temp[0])) * s)
            else:
                nu_res = cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age)
                for (idx, x_temp) in enumerate(nu_res[5]): #Step through mass_i and enumerate the age
                    if nu_res[4][idx] > -100: ##If there is a nu_eff calculated for this object
                        idx2 = np.where(np.logical_and(mass_i_median_age == nu_res[0][idx], snap_median_age == s))[0][0]
                        #agei parameters
                        ages_agei = np.append(ages_agei, (x_temp - median_age[idx2]) / median_age[idx2])
                        nu_agei = np.append(nu_agei, nu_res[2][idx])
                        nueff_agei = np.append(nueff_agei, nu_res[4][idx])
                        z_agei = np.append(z_agei, t) #this is the index of the redshift for this sample
                        #parameters for all mass-age samples
                        tot_age = np.append(tot_age, ages_agei[-1]) #Calculate the fractional age 
                        tot_nu = np.append(tot_nu, nu_res[2][idx])
                        tot_nueff = np.append(tot_nueff, nu_res[4][idx])
                        tot_z = np.append(tot_z, t) #this is the index of the redshift for this sample
        #done running through all snapshots for each age_i
        if age_i != 0:
            medianage_agei = np.append(medianage_agei, np.median(ages_agei))
            nu0 = 0.0865870010439 * np.exp(5.63860426154 * ages_agei) + 0.774929306168
            #param = leastsq(fitting_func1, (0.08, 5.6, 0.77), args = (xtot, ytot, fixed_transition_model, ages))
            #param1.append(best_fit_param[0][:])
            #nu0 = param1[-1][0] * np.exp(param1[-1][1] * ages) + param1[-1][2]
            #param2.append(best_fit_param[0][1])
            #print 'Fitted age_i: {0}, snapshots: {1}, A1 = {3}, Parameters: {4}, {5}, {6}'.format(age_i, snaps, fixed_transition_model, param1[-1][0], param1[-1][1], param1[-1][2])            
            x = nu_agei - nu0
            y = nueff_agei - nu0
            pltx = x / (1. + np.exp(-fixed_transition_model * x))
            plty = y
            sort_idx = np.argsort(pltx)
            plt.plot(pltx[sort_idx], plty[sort_idx], '{0}-'.format(col_j[age_i]))
            #plt.plot(x, x / (1.+ np.exp(-fixed_transition_model * x)), '{0}+'.format(col_j[age_i]))
            #plt.plot(x / (1. + np.exp(-best_fit_param[0][0] * x)), y, '{0}*'.format(col_j[age_i]), label = str(age_i))
            #plt.xlabel('(nu - {1}) / (1 + e^(-{0} * (nu - {1})))'.format(fixed_transition_model, param1[-1]))
            #plt.ylabel('nu_eff - {0}'.format(param1[-1]))
    temp = [min(plt.xlim()[0], plt.ylim()[0]), max(plt.xlim()[1], plt.ylim()[1])]
    plt.plot(temp, temp, 'k--') #Plot y=x line
    plt.xlabel('x * g(x)')
    plt.ylabel('y')
    plt.show()
    
    param = leastsq(fitting_func1, (1., 1.), args = (tot_nu, tot_nueff, fixed_transition_model, tot_age))
    nu0 = param[0][0] * np.exp(param[0][1] * tot_age)
    x = tot_nu - nu0
    y = tot_nueff - nu0
    pltx = x / (1. + np.exp(-fixed_transition_model * x))
    plty = y
    sort_idx = np.argsort(pltx)
    plt.plot(pltx[sort_idx], plty[sort_idx], '{0}-'.format(col_j[age_i]))
    temp = [min(plt.xlim()[0], plt.ylim()[0]), max(plt.xlim()[1], plt.ylim()[1])]
    plt.plot(temp, temp, 'k--') #Plot y=x line
    plt.xlabel('x * g(x)')
    plt.ylabel('y')
    plt.show()
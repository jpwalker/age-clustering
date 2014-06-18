'''
Created on Apr 20, 2014
Fit nu_eff(nu) with a fixed transition in the break off.
@author: jpwalker
'''

import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D

import numpy as np
import os
import compute_nu_eff as cmpn
from scipy.optimize import leastsq
from math import exp

def fitting_func1((A, B, C, D), ls, rs, ages):
    nu0 = A * np.exp(B * ages) + C
    #ls =nu and rs=nu_eff
    ret = []
    for i in range(len(ls)):
        x = ls[i] - nu0[i]
        y = rs[i] - nu0[i]
        try:
            e = exp(-D * x)
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

def fitting_func3((A,), ls, rs, B1):
    print A
    #ls =nu and rs=nu_eff
    ret = []
    for i in range(len(ls)):
        x = ls[i] - A
        y = rs[i] - A
        try:
            e = exp(-B1 * x)
        except OverflowError:
            e = 1E100
        ret.append(y - x / (1. + e))
    return ret

def param_fit_func((A, B, C), x, y):
    print A, B, C
    ret = np.zeros(len(x), dtype = np.float64)
    for i in range(len(x)):
        ret[i] = y[i] - (A * exp(B * x[i]) + C)
    return ret

def index_nu_eff(data, a_i, m_i):
    idx = set()
    idx2 = set()
    for age_i in a_i:
        idx = idx.union(set(np.where(data[1] == age_i)[0]))
    for mass_i in m_i:
        idx2 = idx2.union(set(np.where(data[0] == mass_i)[0]))
    ret = idx2.intersection(idx)
    return np.array(list(ret))
    
if __name__ == '__main__':
    fixed_transition_model = 300.
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    zs = [6.196857, 4.179475, 2.0700316, 0.98870987, 0] #INPUT
    z_points = ['o', '^', 'v', 's', 'p'] ##Predefined points for redshift
    snaps = [22, 27, 36, 45, 67]
    home = '{0}/'.format(os.environ['HOME'])
    snap_identifier = '-1'
    (nu_no_age, bias_no_age)  = cmpn.calc_seljak_warren(1000, cosmo)
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
    p1 = np.empty(len(snaps), dtype = np.object)
    #Properties for the mass-age sample across all redshifts
    best_fits = []
    for (t, s) in enumerate(snaps): #Step through redshift
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')
        z = zs[t]
        pnt = z_points[t]
        finaldir = '{0}Desktop/age-clustering-data/snap{1}{2}/attempt1_sub_form_jp/'.format(home, s, snap_identifier) ##INPUT
        agelabel = 'Sub-Root-Form. Age' ##INPUT ##Label for age definition
        nu_res = cmpn.nu_eff(finaldir, range(0, 6), range(1, 8), cosmo, z, nu_no_age, bias_no_age)
        fit_age = np.empty(0, dtype = float)
        fit_nu = np.empty(0, dtype = float)
        fit_nueff = np.empty(0, dtype = float)
        for age_i in range(1, 6): #Step through mass_i and enumerate the age
            tot_agei = np.empty(0, dtype= int)
            tot_massi = np.empty(0, dtype = int)
            tot_age = np.empty(0, dtype = float)
            tot_nueff = np.empty(0, dtype = float)
            tot_nu = np.empty(0, dtype = float)
            tot_z = np.empty(0, dtype = float)
            color = col_j[age_i]
            for mass_i in range(1, 8):
                idx = index_nu_eff(nu_res, [age_i], [mass_i])[0]
                if nu_res[4][idx] > -100: ##If there is a nu_eff calculated for this object
                    idx2 = index_nu_eff(nu_res, [0], [mass_i])[0]
                    #Calculated values for mass_i and age_i sample
                    tot_agei = np.append(tot_agei, nu_res[1][idx])
                    tot_massi = np.append(tot_massi, nu_res[0][idx])
                    tot_age = np.append(tot_age, (nu_res[5][idx] - nu_res[5][idx2]) / nu_res[5][idx2]) #Calculate the fractional age 
                    tot_nu = np.append(tot_nu, nu_res[2][idx])
                    tot_nueff = np.append(tot_nueff, nu_res[4][idx])
                    tot_z = np.append(tot_z, t) #this is the index of the redshift for this sample
            #p1[t] = ax1.plot(tot_nu, tot_nueff, '{0}{1}'.format(pnt, color))[0]
            ax.scatter(fit_age, fit_nu, fit_nueff, marker = pnt, color = color)
            fit_age = np.append(fit_age, tot_age)
            fit_nu = np.append(fit_nu, tot_nu)
            fit_nueff = np.append(fit_nueff, tot_nueff)
        best_fits.append(leastsq(fitting_func1, (0.01, 10., 5., 50.), args = (fit_nu, fit_nueff, fit_age)))
    ax.set_xlabel('age')
    ax.set_ylabel('nu')
    ax.set_zlabel('nu_eff')
    plt.show()
    for i in best_fits:
        i[0]
#     plt.legend(p1, zs, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.)
#     plt.xlabel('(age - <age>) / <age>')
#     plt.ylabel('nu_eff')
#     fig1.show()
        
        
        
        
        #done running through all snapshots for each age_i
#         nu0 = 0.03390915 * np.exp(10.491329 * ages_agei) + 0.74143699
#         #param1.append(best_fit_param[0][:])
#             #nu0 = param1[-1][0] * np.exp(param1[-1][1] * ages) + param1[-1][2]
#             #param2.append(best_fit_param[0][1])
#             #print 'Fitted age_i: {0}, snapshots: {1}, A1 = {3}, Parameters: {4}, {5}, {6}'.format(age_i, snaps, fixed_transition_model, param1[-1][0], param1[-1][1], param1[-1][2])            
#             x = nu_agei - nu0
#             y = nueff_agei - nu0
#             pltx = x / (1. + np.exp(-fixed_transition_model * x))
#             plty = y
#             sort_idx = np.argsort(pltx)
#             plt.plot(pltx[sort_idx], plty[sort_idx], '{0}-'.format(col_j[age_i]))
# 
#     temp = [min(plt.xlim()[0], plt.ylim()[0]), max(plt.xlim()[1], plt.ylim()[1])]
#     plt.plot(temp, temp, 'k--') #Plot y=x line
#     plt.xlabel('x * g(x)')
#     plt.ylabel('y')
#     plt.show()
#     
#     plt.plot(medianage_agei, testnu0, '*k')
#     nu0_params = leastsq(param_fit_func, (0.01, 10., 5.), args = (medianage_agei, testnu0))[0]
#     plt.plot(medianage_agei, nu0_params[0] * np.exp(medianage_agei * nu0_params[1]) + nu0_params[2], '-k')
#     plt.xlabel('median_age')
#     plt.ylabel('nu0')
#     plt.show()
#     
#     param = leastsq(fitting_func1, (1., 1., 1.), args = (tot_nu, tot_nueff, fixed_transition_model, tot_age))
#     nu0 = param[0][0] * np.exp(param[0][1] * tot_age) + param[0][2]
#     x = tot_nu - nu0
#     y = tot_nueff - nu0
#     pltx = x + nu0 #/ (1. + np.exp(-fixed_transition_model * x))
#     plty = y + nu0
#     sort_idx = np.argsort(pltx)
#     plt.plot(pltx, plty - (x / (1. + np.exp(-fixed_transition_model * x)) + nu0), 'k*')
#     #plt.plot(pltx, x / (1. + np.exp(-fixed_transition_model * x)) + nu0, 'r*')
#     temp = [min(plt.xlim()[0], plt.ylim()[0]), max(plt.xlim()[1], plt.ylim()[1])]
#     plt.plot(temp, temp, 'k--') #Plot y=x line
#     plt.xlabel('x * g(x)')
#     plt.ylabel('y')
#     plt.show()
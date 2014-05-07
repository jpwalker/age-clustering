'''
Created on Apr 20, 2014

@author: jpwalker
'''

import numpy as np
import os
import compute_nu_eff as cmpn
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from math import exp

def fitting_func((A, B), ls, rs):
    #ls is x and rs is y
    ret = []
    for i in range(len(ls)):
        x = ls[i] - B
        y = rs[i] - B
        ret.append(y - x / (1. + exp(-A * x)))
    return ret

if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    zs =  [6.196857, 4.179475, 2.0700316, 0.98870987, 0] #INPUT
    home = '{0}/'.format(os.environ['HOME'])
    snaps = [22, 27, 36, 45, 67]
    (nu_no_age, bias_no_age)  = cmpn.calc_seljak_warren(1000, cosmo)
    xtot = []
    ytot = []
    for (t, s) in enumerate(snaps):
        z = zs[t]
        finaldir = '{0}Desktop/age-clustering-data/snap{1}/attempt1_sub_form_gao/'.format(home, s) ##INPUT
        agelabel = 'Sub-Root-Form. Age' ##INPUT
        col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
        nu_res = []
        for age_i in range(0,6):
            x = np.array([])
            y = np.array([])
            txt = np.array([],dtype = int)
            if age_i == 0:
                temp = cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age)
                median_age = temp[5]
                mass_i_median_age = temp[0]
            else:
                nu_res.append(cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age))
                for (idx, x_temp) in enumerate(nu_res[-1][5]):
                    if nu_res[-1][4][idx] > -100:
                        idx2 = np.where(mass_i_median_age == nu_res[-1][0][idx])[0]
                        x = np.append(x, nu_res[-1][2][idx]) 
                        y = np.append(y, nu_res[-1][4][idx])
                        txt = np.append(txt, nu_res[-1][0][idx])
                xtot.extend(x)
                ytot.extend(y)
                #plt.plot(x, y, '+', 
                #         color = col_j[age_i], label = '{0}_{1}_{2}'.format(agelabel, s, age_i))
                #for (i, txt_i) in enumerate(txt):
                #    plt.text(x[i], y[i], txt_i)
    plt.plot([0,10],[0,10], '--')
    best_fit_param = leastsq(fitting_func, (1.0, 0.8), args = (xtot, ytot))
    x = np.array(xtot) - best_fit_param[0][1]
    y = np.array(ytot) - best_fit_param[0][1]
    plt.plot(x / (1. + np.exp(-best_fit_param[0][0] * x)), y, 'k+')
    plt.xlabel('(nu - {1}) / (1 + e^(-{0} * (nu - {1})))'.format(best_fit_param[0][0], best_fit_param[0][1]))
    plt.ylabel('nu_eff - {0}'.format(best_fit_param[0][1]))
    #plt.legend()
    plt.show()
    plt.plot(xtot, ytot, 'k+')
    plt.plot(xtot, x / (1.+ np.exp(-best_fit_param[0][0] * x)) + best_fit_param[0][1], 'r+')
    plt.xlabel('nu')
    plt.ylabel('nu_eff')
    plt.show()
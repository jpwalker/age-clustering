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
    identifier = '-1'
    (nu_no_age, bias_no_age)  = cmpn.calc_seljak_warren(1000, cosmo)
    col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
    nu_res = []
    fractional_age = []
    param1 = []
    param2 = []
    for age_i in range(0,6): #Step through age_i
        ages = np.array([], dtype = float)
        xtot = []
        ytot = []
        for (t, s) in enumerate(snaps): #Step through redshift
            z = zs[t]
            finaldir = '{0}Desktop/age-clustering-data/snap{1}{2}/attempt1_sub_form_gao/'.format(home, s, identifier) ##INPUT
            agelabel = 'Sub-Root-Form. Age' ##INPUT
            x = np.array([])
            y = np.array([])
            txt = np.array([], dtype = int)
            if age_i == 0:
                temp = cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age)
                median_age = temp[5]
                mass_i_median_age = temp[0]
            else:
                nu_res.append(cmpn.nu_eff(finaldir, age_i, range(1, 8), cosmo, z, nu_no_age, bias_no_age))
                for (idx, x_temp) in enumerate(nu_res[-1][5]): #Step trhough mass_i
                    if nu_res[-1][4][idx] > -100:
                        idx2 = np.where(mass_i_median_age == nu_res[-1][0][idx])[0][0]
                        ages = np.append(ages, (x_temp  - median_age[idx2]) / median_age[idx2])
                        print s, nu_res[-1][0][idx], nu_res[-1][1][idx], ages[-1]
                        x = np.append(x, nu_res[-1][2][idx])
                        y = np.append(y, nu_res[-1][4][idx])
                        txt = np.append(txt, nu_res[-1][0][idx])
                xtot.extend(x)
                ytot.extend(y)
                #plt.plot(x, y, '+', 
                #         color = col_j[age_i], label = '{0}_{1}_{2}'.format(agelabel, s, age_i))
                #for (i, txt_i) in enumerate(txt):
                #    plt.text(x[i], y[i], txt_i)
        #done running through all snapshots for each age_i
        if age_i != 0:
            plt.plot([0,10],[0,10], 'k--')
            fractional_age.append(np.median(ages))
            best_fit_param = leastsq(fitting_func, (1.0, 0.8), args = (xtot, ytot))
            param1.append(best_fit_param[0][0])
            param2.append(best_fit_param[0][1])
            x = np.array(xtot) - best_fit_param[0][1]
            y = np.array(ytot) - best_fit_param[0][1]
            plt.plot(x + best_fit_param[0][1], y + best_fit_param[0][1], '{0}*'.format(col_j[age_i]), label = str(age_i))
            plt.plot(x + best_fit_param[0][1], x / (1.+ np.exp(-best_fit_param[0][0] * x)) + best_fit_param[0][1], '{0}+'.format(col_j[age_i]))
            #plt.plot(x / (1. + np.exp(-best_fit_param[0][0] * x)), y, '{0}*'.format(col_j[age_i]), label = str(age_i))
            plt.xlabel('(nu - {1}) / (1 + e^(-{0} * (nu - {1})))'.format(best_fit_param[0][0], best_fit_param[0][1]))
            plt.ylabel('nu_eff - {0}'.format(best_fit_param[0][1]))
    plt.legend()
    plt.show()
    plt.plot(fractional_age, param1, '*')
    plt.xlabel('(age - <age>) / <age>')
    plt.ylabel('param_1')
    plt.show()
    plt.plot(fractional_age, param2, '*')
    plt.xlabel('(age - <age>) / <age>')
    plt.ylabel('param_2')
    plt.show()
#     plt.plot(xtot, ytot, 'k+')
#     plt.plot(xtot, x / (1.+ np.exp(-best_fit_param[0][0] * x)) + best_fit_param[0][1], 'r+')
#     plt.xlabel('nu')
#     plt.ylabel('nu_eff')
#     plt.show()
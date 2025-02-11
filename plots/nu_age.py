'''
Created on Apr 20, 2014

@author: jpwalker
'''

import numpy as np
import os
from compute_nu_eff import calc_seljak_warren_w_cut, nu_eff
import matplotlib.pyplot as plt
from matplotlib import rc

if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0} # INPUT
    zs =  [6.196857, 4.179475, 3.0604243, 2.0700316, 1.5036374, 0.98870987, 
           0.564176, 0] #INPUT
    home = '{0}/'.format(os.environ['HOME'])
    snaps = [22, 27, 31, 36, 40, 45, 51, 67]
    suffix = '-1'
    xtot = []
    ytot = []
    (nu_no_age, bias_no_age, _)  = calc_seljak_warren_w_cut(1000, 0.75, cosmo)
    for (t, s) in enumerate(snaps):
        z = zs[t]
        finaldir = '{0}Desktop/age-clustering-data/snap{1}{2}/attempt1_sub_form_jp/'.format(home, s, suffix) ##INPUT
        agelabel = 'Sub-Max-Form. Age' ##INPUT
        col_j = ['k', 'b', 'c', 'g', 'm', 'r'] ##Predefined colors for age_i
        
        nu_res = []
        for age_i in range(0,6):
            x = np.array([])
            y = np.array([])
            txt = np.array([],dtype = int)
            if age_i == 0:
                temp = nu_eff(finaldir, (age_i,), range(1, 9), cosmo, z, nu_no_age, bias_no_age)
                median_age = temp[5]
                mass_i_median_age = temp[0]
            else:
                nu_res.append(nu_eff(finaldir, (age_i,), range(1, 9), cosmo, z, nu_no_age, bias_no_age))
                for (idx, x_temp) in enumerate(nu_res[-1][5]):
                    idx2 = np.where(mass_i_median_age == nu_res[-1][0][idx])[0]
                    x = np.append(x, (x_temp - median_age[idx2]) / median_age[idx2]) 
                    y = np.append(y, nu_res[-1][2][idx])
                    txt = np.append(txt, nu_res[-1][0][idx])    
                xtot.extend(x)
                ytot.extend(y)
                plt.plot(x, y, '+', 
                         color = col_j[age_i], label = '{0}_{1}_{2}'.format(agelabel, s, age_i))
#                 for (i, txt_i) in enumerate(txt):
#                     plt.text(x[i], y[i], txt_i)
    #xtot = np.array(xtot)
    #ytot = np.array(ytot)
    #(slope, intercept, rval, pval, stderr) = linregress(xtot, ytot)
    #plt.plot(xtot, xtot * slope + intercept , 'r')
    #plt.plot([0, 0], [10, 0], '--k')
    rc('text', usetex = True)
    plt.xlabel('$\\alpha$')
    plt.ylabel('$\\nu$')
    #plt.legend()
    plt.show()
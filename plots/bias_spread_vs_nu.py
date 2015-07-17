'''
Created on Mar 4, 2015

@author: jpwalker
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from compute_nu_eff import calc_seljak_warren_w_cut
from compute_nu_eff import reverse_calc_nu_eff


if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
    seljak = calc_seljak_warren_w_cut(1000, 0.65, cosmo)
    best_fit = (0.62564927,  0.57876966,  0.47245533, -5.23972499,  1.08041045)
    alpha = (0, -0.5, -0.25, 0.25, 0.5)
    color = ('blue', 'red', 'green', 'black')
    nu0 = [best_fit[0] * np.exp(best_fit[1] * a) + best_fit[2] for a in alpha]
    m = [best_fit[3] * a + best_fit[4] for a in alpha]
    nu = np.linspace(0.5, 3.5, 1000)
    nu_eff = [(nu-nu0[i]) * m[i] + nu0[i] for i in range(len(m))]
    bias = [reverse_calc_nu_eff(i, seljak) for i in nu_eff]
    for (i, y) in enumerate(bias):
        if i !=0:
            plt.plot(nu, y - bias[0], color[i - 1])
    #plt.plot(seljak[0], seljak[1], 'k--')
    rc('text', usetex=True)
    plt.xlabel('$\\nu$')
    plt.ylabel('$\\Delta b$')
    plt.show()
'''
Created on Aug 4, 2015

@author: jpwalker
'''
from numpy import linspace, exp, concatenate
from compute_nu_eff import calc_seljak_warren_w_cut, reverse_calc_nu_eff
from matplotlib.pyplot import plot, xlabel, ylabel, legend, show

def calc_nu_eff(nu, m, nu_0):
    return concatenate(((nu[nu<nu_0] - nu_0) * m + nu_0, nu[nu>=nu_0]))

if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
    seljak = calc_seljak_warren_w_cut(1000, 0.75, cosmo)
    nu = linspace(0.3, 3.5, 1000)
    best_fit = (0.11189464,  4.21471345,  0.92813833, -2.90082599,  0.77097244)
    alpha = (0, -0.15, -0.1, 0.1, 0.5)
    color = ('black', 'blue', 'cyan', 'magenta', 'red')
    nu0 = [best_fit[0] * exp(best_fit[1] * a) + best_fit[2] for a in alpha]
    m = [best_fit[3] * a + best_fit[4] for a in alpha]
    nu_eff = [calc_nu_eff(nu, m[i], nu0[i]) for i in range(len(m))]
    bias = [reverse_calc_nu_eff(i, seljak) for i in nu_eff]
    for i in range(len(nu_eff)):
        plot(bias[i], nu_eff[i] - nu, color[i], 
             label='$\\alpha={0}$'.format(alpha[i]))
    xlabel('$b$')
    ylabel('$\\nu_\\mathrm{eff}-\\nu$')
    legend()
    show()
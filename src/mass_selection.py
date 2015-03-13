'''
Created on Mar 24, 2014

@author: jpwalker
'''

import compute_nu as n 
from IO import *
from MillenniumII import *
import numpy as np

cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}

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

def calc_SNR(halos, z):
    nu_halos = n.compute_nu(get_col_halo_table(halos, 'fof_np'), z, cosmo)

if __name__ == '__main__':
    ##Setup Seljak and Warren for later
    SW = calc_seljak_warren(1000, cosmo)
    direc = '/Volumes/DATA/age-clustering-data-original/'
    prefix_filename = 'attempt1millenniumIIsnap'
    file_nums = [22, 27, 36, 45, 67]
    z = [6.196857, 4.179475, 2.0700316, 0.98870987, 0]
    postfix_filename = '_1057_sub.txt'
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,17,x,21,22,23,24,27,25,28,26,29'
    for (i, fns) in file_nums:
        file_name = '{0}{1}{2}{3}'.format(direc, prefix_filename, fns, 
                                          postfix_filename)
        halos = read_halo_table_ascii(file_name, fmt)
        if i == 0:
        #Running the high z for loop to find the best SNR
            fofnp = get_col_halo_table(halos, 'fof_np')
            med_fofnp = np.median(fofnp)
            lower_idx = np.where(fofnp <= med_fofnp)[0]
            upper_idx = np.where(fofnp > med_fofnp)[0]
            temphalo_lower = select_halo_table(halos, lower_idx)
            temphalo_upper = select_halo_table(halos, upper_idx)
            SNR = [calc_SNR(temphalo_lower, z[i]), calc_SNR(temphalo_upper, z[i])]
            set_SNR = max(SNR)
            #Output the massbin limits
            fofnp1 = get_col_halo_table(temphalo_lower, 'fof_np')
            fofnp2 = get_col_halo_table(temphalo_upper, 'fof_np')
            out = np.array([min(fofnp1), max(fofnp1), min(fofnp2), max(fofnp2)])
            outfile = '{0}mass_bins_{1}.txt'.format(direc, fns)
            writefile(outfile, out)
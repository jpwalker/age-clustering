'''
Created on Aug 22, 2013

@author: jpwalker
'''

from numpy import logical_and, array, where
from IO import readfile
from matplotlib.pyplot import figure, show
from matplotlib import rc, rcdefaults
from compute_nu import compute_nu
from os import environ
from compute_nu_eff import calc_seljak_warren_w_cut, calc_mo_white_nu, calc_seljak_warren,\
    calc_sheth_tormen_nu

if __name__ == '__main__':
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    snaps = (22, 27, 36, 40, 45, 51, 67)
    symbs = ('o', '^', 'v', 'D', 's', '*', 'p')
    snap_id = '-1'
    #Update the redshift as necessary
    z = (6.196857, 4.179475, 2.0700316, 1.5036374, 0.98870987, 0.5641763, 0.) 
    ##Create figure and axes to create both the regular plot and the sub-panel
    fig = figure()
    st_ax = fig.add_axes([0.1, 0.1, 0.85, 0.85])
    sp_ax = fig.add_axes([0.17, 0.45, 0.40, 0.45])
    #Cosmology for MS and MS2
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
    home = '{0}/'.format(environ['HOME'])
    (nu, b, _) = calc_seljak_warren_w_cut(1000, 0.75, cosmo)
    st_ax.plot(nu, b, 'r--')
    sp_ax.plot(nu, b, 'r--')
    (nu, b, _) = calc_seljak_warren(1000, cosmo)
    st_ax.plot(nu, b, 'k--')
    sp_ax.plot(nu, b, 'k--')
    (nu, b, _) = calc_mo_white_nu(1000, cosmo)
    st_ax.plot(nu, b, 'k-')
    sp_ax.plot(nu, b, 'k-')
    (nu, b, _) = calc_sheth_tormen_nu(1000, cosmo)
    st_ax.plot(nu, b, 'g-')
    sp_ax.plot(nu, b, 'g-')
    age_bins = 5
    mass_bins = 7
    ifile = 'properties.dat'
    agelabel = 'Sub-Max-Form. Age'
    for (i, s) in enumerate(snaps):
        snap_dir = 'snap{0}{1}'.format(s, snap_id)
        direc = '{0}Desktop/age-clustering-data/{1}/attempt1_sub_form_jp/'.format(home, snap_dir)
        data = readfile('{0}{1}'.format(direc, ifile), col = 28, delim = '    ', skip = 1)
        col_j = ['k', 'b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
        for age_i in range(0, age_bins + 1):
            bias = []
            mass = []
            for mass_i in range(1, mass_bins + 1):
                b_data = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
                idx1 = where(logical_and(b_data[0] >= 5, b_data[0] <= 15))[0]
                idx2 = where(logical_and(data[0] == mass_i, data[1] == age_i))[0]
                bias.append(sum(b_data[1][idx1]) / len(b_data[1][idx1]))
                mass.append(data[4][idx2][0])
            bias = array(bias)
            mass = array(mass)
            if symbs[i] == 'p' or symbs[i] == '*':
                symsize = 5.
            else:
                symsize = 4.
            st_ax.plot(compute_nu(mass * massconv / h, z[i], cosmo), bias, symbs[i], 
                       color = col_j[age_i], 
                       label = '{0}, Q: {1}, z:{2}'.format(agelabel, age_i, z[i]), 
                       ms = symsize)
            sp_ax.plot(compute_nu(mass * massconv / h, z[i], cosmo), bias, symbs[i], 
                       color = col_j[age_i], ms = symsize)
    sp_ax.set_xlim([0.3, 1.22])
    sp_ax.set_ylim([0.25, 1.75])
    st_ax.set_xlim([0.3, 3.1])
    st_ax.set_ylim([0.25, 8.5])
    rc('text', usetex = True)
    st_ax.set_xlabel('$\\nu$')
    st_ax.set_ylabel('$b$')
    #st_ax.legend()
    rcdefaults()
    show()
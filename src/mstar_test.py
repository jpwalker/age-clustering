'''
Created on Jan 10, 2014

@author: jpwalker
'''

import matplotlib.pyplot as plt
import numpy as np
import MillenniumII as m2
import os
import Correlation_Func as cf
import Standard_Plots as sp
    
if __name__ == '__main__':
    curr = '{0}/'.format(os.getcwd())
    filen = 'Mstar_cat_snap31-MS2.txt'
    xi_m_m_filen = 'xi_m_m_36.txt'
    h = 0.73
    mass_conv = 6.9E6 / h #Converts to Solar Masses 
    #Read in xi_m_m
    xi_m_m_corr = cf.read_corr_file(xi_m_m_filen)
    #Read in sample
    sample = m2.read_halo_table_ascii('{0}{1}'.format(curr, filen), '7,8,9,17')
    print 'Plotting position scatter plot of sample file: {0}'.format(filen)
    sp.plot_position_scatter(sample, 'x', 'y')
    plt.show()
    print np.median(np.array(m2.get_col_halo_table(sample, 'fof_np')) * mass_conv)
    sample_auto_corr = cf.calc_auto_corr(sample, MS2 = True)
    #sample_cross_corr = calc_cross_corr(sample)
    plt.loglog(sample_auto_corr['data'].r, sample_auto_corr['data'].cf, label = 'sample')
    plt.loglog(xi_m_m_corr['data'].r, xi_m_m_corr['data'].cf, label = '$\\xi_{mm}$')
    print sample_auto_corr['data'].cf
    print xi_m_m_corr['data'].cf
    plt.plot(sample_auto_corr['data'].r, np.sqrt(sample_auto_corr['data'].cf / xi_m_m_corr['data'].cf))
    plt.legend()
    plt.rc('text', usetex = True)
    plt.xlabel('r [Mpc / h]')
    plt.ylabel('$\\xi(r)$')
    plt.show()
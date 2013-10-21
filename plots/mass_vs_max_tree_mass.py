'''
Created on Oct 21, 2013

@author: jpwalker
'''

from MillenniumII import *
import IO
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    massconv = 6.885E6 / 0.73
    direc = '/Users/jpwalker/Desktop/age-clustering attempt 1/z0_attempt1_form_gao/'
    data = read_halo_table_ascii('{0}{1}'.format(direc, \
                                             'millenniumIIsnap67age_attempt1057fof_2.txt'), \
                             'x,x,x,x,x,x,x,7,8,9,x,x,x,17,x,21,22,23,24,x,x,x,x,x')
    maxtreemass = np.array(get_col_halo_table(data, 'max_tree_mass')) * massconv
    rootmass = np.array(get_col_halo_table(data, 'fof_np')) * massconv
    plt.loglog(rootmass, maxtreemass, '.')
    plt.loglog(plt.xlim(), plt.ylim(), '--')
    plt.xlabel('Root Mass [M_Sun]')
    plt.ylabel('Max Tree Mass [M_Sun]')
    plt.show()
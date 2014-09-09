'''
Created on Jan 24, 2014

@author: jpwalker
'''

import numpy as np
import MillenniumII as m2
import matplotlib.pyplot as plt

cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}

def check_for_pos_key(key):
    if not (key == 'x' or key == 'y' or key == 'z'):
        raise TypeError('Input key: {0} is not valid').format(key)
def check_for_mass_key(key):
    if not (key == 'fof_np' or key == 'sub_np'):
        raise TypeError('Imput key: {0} is not valid').format(key)

##function plots Millennium or MillenniumII structures 
def plot_position_scatter(MS_table, pos_key1 = 'x', pos_key2 = 'y'):
    check_for_pos_key(pos_key1)
    check_for_pos_key(pos_key2)
    pos1 = m2.get_col_halo_table(MS_table, pos_key1)
    pos2 = m2.get_col_halo_table(MS_table, pos_key2)
    plt.plot(pos1, pos2, '*', markersize = .96)
    plt.xlabel('{0} [Mpc / h]'.format(pos_key1))
    plt.ylabel('{0} [Mpc / h]'.format(pos_key2))
    
def plot_mass_histogram(MS_table, mass_key = 'fof_np', no_h = True, MS2 = False, bins = 50, color = 'k', label = ''):
    check_for_mass_key(mass_key)
    mass = np.array(m2.get_col_halo_table(MS_table, mass_key))
    if MS2 == False:
        mass_conv = 8.6E8
    else:
        mass_conv = 6.885E6
    if no_h:
        mass_conv /= cosmo['h']
    mass = np.log10(mass * mass_conv)
    hist_ret = plt.hist(mass, bins, color = color, label = label)
    return hist_ret
    
if __name__ == '__main__':
    a = m2.read_halo_table_ascii("/Volumes/DATA/Millennium Data/MillenniumII/snap6.txt", "0,1,2,3,4,5,6,7,8,9,x,x,x,x,x,15,16,17,x,x,20")
    plot_mass_histogram(a, mass_key = 'fof_np', no_h = True, MS2 = True, color = 'k', label = 'no_h')
    plot_mass_histogram(a, mass_key = 'fof_np', no_h = False, MS2 = True, color = 'r')
    plt.rc('text', usetex = True)
    plt.xlabel('Mass (M$_\\odot$)')
    plt.show()
'''
Created on Oct 21, 2013

@author: jpwalker
'''

from MillenniumII import *
import IO
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_max_mass_vs_mass(rootmass, maxtreemass, (idx1, idx2)):
    massconv = 6.885E6 / 0.73
    plt.loglog(rootmass[idx1] * massconv, maxtreemass[idx1] * massconv, '.k')
    plt.loglog(rootmass[idx2] * massconv, maxtreemass[idx2] * massconv, '.r')
    one_to_one()
    plt.xlabel('Root Mass [M_Sun]')
    plt.ylabel('Max Tree Mass [M_Sun]')
    plt.show()
    
def plot_age_us_vs_age_gao(form_jp, form_gao, (idx1, idx2)):
    plt.plot(form_jp[idx1], form_gao[idx1], '.k')
    plt.plot(form_jp[idx2], form_gao[idx2], '.r')      
    plt.xlabel('Form. Us (Gyrs)')
    plt.ylabel('Form. Gao (Gyrs)')
    plt.show()
    
def one_to_one():
    mi = min([min(plt.xlim()), max(plt.ylim())])
    ma = max([max(plt.xlim()), max(plt.ylim())])
    plt.loglog([mi, ma], [mi, ma], '--')
    
if __name__ == '__main__':
    homed = '{0}/'.format(os.environ['HOME'])
    cwd = '{0}/'.format(os.getcwd())
    direc = '{0}Desktop/age-clustering attempt 2/z0_attempt1_form_jp/'.format(homed)
    filename = 'millenniumIIsnap67age_attempt1057fof_2.txt'
    formt = '0,1,2,3,4,5,6,7,8,9,10,11,15,17,16,21,22,23,24,26,28,25,27,29'
    data = read_halo_table_ascii('{0}{1}'.format(direc, filename), formt)
    maxtreemass = np.array(get_col_halo_table(data, 'max_tree_mass'))
    rootmass = np.array(get_col_halo_table(data, 'fof_np'))
    form_gao = np.array(get_col_halo_table(data, 'form_gao'))
    form_jp = np.array(get_col_halo_table(data, 'form_jp'))
    idx1 = np.where((maxtreemass - rootmass) >= 2. * np.sqrt(maxtreemass)) 
    idx2 = np.where((maxtreemass - rootmass) < 2. * np.sqrt(maxtreemass))
    print '{0} halos with significant mass loss.'.format(len(idx1[0]))
    print '{0} halos without significant mass loss.'.format(len(idx2[0]))
    plot_max_mass_vs_mass(rootmass, maxtreemass, (idx1, idx2))
    plot_age_us_vs_age_gao(form_jp, form_gao, (idx1, idx2))
    write_halo_table_ascii('{0}{1}'.format(cwd, 'sig_massloss.txt'), \
                           select_halo_table(data, idx1[0]), formt)
    write_halo_table_ascii('{0}{1}'.format(cwd, 'no_sig_massloss.txt'), \
                           select_halo_table(data, idx2[0]), formt)
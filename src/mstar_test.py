'''
Created on Jan 10, 2014

@author: jpwalker
'''

from IO import readfile 
import matplotlib.pyplot as plt
import numpy as np
import MillenniumII as m2
from subprocess import check_output
import os
from collections import namedtuple
from matplotlib import rc

corr_func = namedtuple('corr_func', ['r', 'cf', 'err', 'RR'])

def create_corr_struct(r = [], cf = [], err = [], RR = [], num = 0):
    if len(r) == len(cf) and len(cf) == len(err) and len(err) == len(RR):
        cast(r, 'flt')
        cast(cf, 'flt')
        cast(RR, 'flt')
        cast(err, 'flt')
        cast(num, 'int')
        return {'num': 0, 'data': corr_func(r, cf, err, RR)}
    else:
        raise TypeError('Input array length mismatch')

def cast(d, t):
    ret = np.zeros(len(d))
    try:
        for (j, i) in enumerate(d):
            if t == 'int':
                ret[j] = int(i)
            if t == 'flt':
                ret[j] =  float(i)
    except ValueError:
        print('Unable to cast {0}'.format(i))
    return ret
        
def read_corr_file(filen):
    num = readfile(filen, 1, skip = 1, numlines = 1)
    data = readfile(filen, 4, ',', skip = 2)
    return create_corr_struct(data[0], data[1], np.zeros(len(data[0])), data[2], num)
    
def calc_auto_corr(mill_data, outfile = '', tempfile_addon = ''):
    curr = '{0}/'.format(os.getcwd())
    if outfile == '':
        outfile = '{0}outtemp'.format(curr)
        wr = False
    temp_file = '{0}temp{1}'.format(curr, tempfile_addon)
    m2.write_halo_table_ascii(temp_file, mill_data, '7,8,9')
    check_output(['2pt-autocorrelation-MS', temp_file, outfile])
    auto_corr = read_corr_file(outfile)
    os.remove(temp_file)
    if not wr:
        os.remove(outfile)
    return auto_corr

def check_for_pos_key(key):
    if not (key == 'x' or key == 'y' or key == 'z'):
        raise TypeError('Input key: {0} is not valid').format(key)

##function plots Millennium or MillenniumII structures 
def plot_position_scatter(MS_table, pos_key1 = 'x', pos_key2 = 'y'):
    check_for_pos_key(pos_key1)
    check_for_pos_key(pos_key2)
    pos1 = m2.get_col_halo_table(MS_table, pos_key1)
    pos2 = m2.get_col_halo_table(MS_table, pos_key2)
    plt.plot(pos1, pos2, '*', markersize = .96)
    plt.xlabel('{0} [Mpc / h]'.format(pos_key1))
    plt.ylabel('{0} [Mpc / h]'.format(pos_key2))
    plt.show()
    
if __name__ == '__main__':
    curr = '{0}/'.format(os.getcwd())
    filen = 'Mstar_cat2.txt'
    xi_m_m_filen = 'xi_m_m_boylan.txt'
    h = 0.73
    mass_conv = 8.6E8 / h #Converts to Solar Masses 
    #Read in xi_m_m
    xi_m_m_corr = read_corr_file(xi_m_m_filen)
    #Read in sample
    sample = m2.read_halo_table_ascii('{0}{1}'.format(curr, filen), '7,8,9,17')
    print 'Plotting position scatter plot of sample file: {0}'.format(filen)
    plot_position_scatter(sample, 'x', 'y')
    print np.median(np.array(m2.get_col_halo_table(sample, 'fof_np')) * mass_conv)
    sample_corr = calc_auto_corr(sample)
    plt.loglog(sample_corr['data'].r, sample_corr['data'].cf, label = 'sample')
    plt.loglog(xi_m_m_corr['data'].r, xi_m_m_corr['data'].cf, label = 'xi_m_m')
    plt.plot(sample_corr['data'].r, np.sqrt(sample_corr['data'].cf / xi_m_m_corr['data'].cf))
    plt.legend()
    #plt.rc('text', usetex = True)
    plt.xlabel('r [Mpc / h]')
    plt.ylabel('$\\xi(r)$')
    plt.show()
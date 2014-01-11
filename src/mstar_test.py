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
    data = readfile(filen, 3, ',', skip = 2)
    return create_corr_struct(data[0], data[1], np.zeros(len(data[0])), data[2], num)
    
def calc_auto_corr(mill_data, outfile, tempfile_addon = ''):
    curr = '{0}/'.format(os.getcwd())
    temp_file = '{0}temp{1}'.format(curr, tempfile_addon)
    m2.write_halo_table_ascii(temp_file, mill_data, '7,8,9')
    check_output(['2pt-autocorrelation', temp_file, outfile])
    auto_corr = read_corr_file(outfile)
    os.remove(temp_file)
    return auto_corr
    
if __name__ == '__main__':
    print os.environ['PATH']
    curr = '{0}/'.format(os.getcwd())
    filen = 'Mstar_cat.txt'
    auto_sample_filen = '{0}autosample'.format(curr)
    h = 0.73
    mass_conv = 8.6E8 / h #Converts to Solar Masses 
    sample = m2.read_halo_table_ascii('{0}{1}'.format(curr, filen), '7,8,9,17')
    print np.median(np.array(m2.get_col_halo_table(sample, 'fof_np')) * mass_conv)
    sample_corr = calc_auto_corr(sample, auto_sample_filen)
    plt.loglog(sample_corr['data'].r, sample_corr['data'].cf)
    plt.show()
    #Cleanup
    os.remove(auto_sample_filen)
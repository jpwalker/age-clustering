'''
Created on Jan 24, 2014

@author: jpwalker
'''

from IO import readfile
import numpy as np
from collections import namedtuple
from subprocess import check_output
import os
import MillenniumII as m2
import cosmolopy.perturbation as per
import matplotlib.pyplot as plt

corr_func = namedtuple('corr_func', ['r', 'cf', 'err', 'DD', 'RR'])
corr_f_fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20'

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

def create_corr_struct(r = [], cf = [], err = [], DD = [], RR = [], num = 0):
    if len(r) == len(cf) and len(cf) == len(err) and len(err) == len(RR) and \
    len(RR) == len(DD):
        cast(r, 'flt')
        cast(cf, 'flt')
        cast(RR, 'flt')
        cast(DD, 'flt')
        cast(err, 'flt')
        num = int(num)
        return {'num': 0, 'data': corr_func(r, cf, err, DD, RR)}
    else:
        raise TypeError('Input array length mismatch')

#Grow the 
def corr_grow(xi_m_m1, zin1, zout, cosmo, xi_m_m2 = None, zin2 = None, pt = False):
    growth_fac_1 = per.fgrowth(zin1, cosmo['omega_M_0'])
    growth_fac_out = per.fgrowth(zout, cosmo['omega_M_0'])
    xi_m_m1_new = create_corr_struct(xi_m_m1['data'].r, xi_m_m1['data'].cf / growth_fac_1**2. * growth_fac_out**2., \
                                         xi_m_m1['data'].err, xi_m_m1['data'].DD, xi_m_m1['data'].RR, xi_m_m1['num'])
    xi_m_m_out = xi_m_m1_new
    if xi_m_m2 != None and zin2 != None and (xi_m_m1['data'].r == xi_m_m2['data'].r).all():
        growth_fac_2 = per.fgrowth(zin2, cosmo['omega_M_0'])
        xi_m_m2_new = create_corr_struct(xi_m_m2['data'].r, xi_m_m2['data'].cf / growth_fac_2**2. * growth_fac_out**2., \
                                         xi_m_m2['data'].err, xi_m_m2['data'].DD, xi_m_m2['data'].RR, xi_m_m2['num'])
        cf_temp = []
        temp_len = len(xi_m_m1['data'].r)
        temp_zero = np.zeros(temp_len)
        for i in range(temp_len):
            temp_array = np.array([xi_m_m1_new['data'].cf[i], xi_m_m2_new['data'].cf[i]])
            (wavg, sum_wts) = np.average(temp_array, weights = np.abs([1 / (zin1 - zout), 1 / (zin2 - zout)]), returned = True)
            cf_temp.append(wavg)
        xi_m_m_out = create_corr_struct(xi_m_m1['data'].r, cf_temp, temp_zero, temp_zero, temp_zero, num = 0)
    if pt:
        plt.loglog(xi_m_m1['data'].r, xi_m_m1['data'].cf, label = 'xi1_old')
        plt.loglog(xi_m_m1_new['data'].r, xi_m_m1_new['data'].cf, label = 'xi1_new')
        if xi_m_m2 != None:
            plt.loglog(xi_m_m2['data'].r, xi_m_m2['data'].cf, label = 'xi2_old')
            plt.loglog(xi_m_m2_new['data'].r, xi_m_m2_new['data'].cf, label = 'xi2_new')
    return xi_m_m_out
    
##Standard format for read_corr_file is r, xi, DD, RR
def read_corr_file(filen):
    num = readfile(filen, 1, skip = 1, numlines = 1)
    data = readfile(filen, 4, ',', skip = 2)
    return create_corr_struct(data[0], data[1], np.zeros(len(data[0])), data[2], \
                              data[3], num[0])

##Standard format for write_corr_file is r, xi, DD, RR
def write_corr_file(filen, data):
    output = []
    delim = ','
    try:
        f = open(filen, 'w+')
        f.write('radii,CF(r),DD(r),RR(r)\n')
        f.write('{0}\n'.format(data['num']))
        for i in range(len(data['data'].r)):
            temp = [str(data['data'].r[i]), str(data['data'].cf[i]), \
                    str(data['data'].DD[i]), str(data['data'].RR[i])]
            output.append('{0}\n'.format(delim.join(temp)))
        print 'Writing to file...'
        f.writelines(output)
        print 'File Saved!!!'
        f.close()
    except IOError:
        print 'Error opening/writing to file'

#
def calc_auto_corr(mill_data, outfile = '', halo_file = '', MS2 = False):
    tw = True
    wr = True
    curr = '{0}/'.format(os.getcwd())
    if outfile == '':
        outfile = '{0}outtemp'.format(curr)
        wr = False
    if halo_file == '':
        halo_file = '{0}temp'.format(curr)
        tw = False
    m2.write_halo_table_ascii(halo_file, mill_data, fmt = corr_f_fmt)
    if MS2:
        check_output(['2pt-autocorrelation-MS2', halo_file, outfile])
    else:
        check_output(['2pt-autocorrelation-MS', halo_file, outfile])
    auto_corr = read_corr_file(outfile)
    if not tw:
        os.remove(halo_file)
    if not wr:
        os.remove(outfile)
    return auto_corr


#
def calc_cross_corr(mill_data1, mill_data2, outfile = '', halo_file1 = '', \
                    halo_file2 = '', MS2 = False):
    wr = True
    tw1 = True
    tw2 = True
    curr = '{0}/'.format(os.getcwd())
    if outfile == '':
        outfile = '{0}outtemp'.format(curr)
        wr = False
    if halo_file1 == '':
        halo_file1 = '{0}temp1'.format(curr)
        tw1 = False
    if halo_file2 == '':
        halo_file2 = '{0}temp2'.format(curr)
        tw2 = False
    m2.write_halo_table_ascii(halo_file1, mill_data1, corr_f_fmt)
    m2.write_halo_table_ascii(halo_file2, mill_data2, corr_f_fmt)
    if MS2:
        check_output(['2pt-crosscorrelation-MS2', halo_file1, halo_file2, outfile])
    else:
        check_output(['2pt-crosscorrelation-MS', halo_file1, halo_file2, outfile])
    cross_corr = read_corr_file(outfile)
    if not tw1:
        os.remove(halo_file1)
    if not tw2:
        os.remove(halo_file2)
    if not wr:
        os.remove(outfile)
    return cross_corr

if __name__ == '__main__':
    cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
    xi_m_m_67 = read_corr_file('xi_m_m_67.txt')
    xi_m_m_36 = read_corr_file('xi_m_m_36.txt')
    xi_m_m_22 = read_corr_file('xi_m_m_22.txt')
    new_xi_m_m = corr_grow(xi_m_m_22, 6.196857, 4.179475, cosmo, xi_m_m2 = xi_m_m_36, zin2 = 2.0700316, pt = True)
    plt.loglog(xi_m_m_36['data'].r, xi_m_m_36['data'].cf, label = '36')
    plt.loglog(new_xi_m_m['data'].r, new_xi_m_m['data'].cf, label = 'new_xi')
    plt.xlabel('r')
    plt.ylabel('xi')
    plt.legend()
    plt.show()
    write_corr_file('xi_m_m_27.txt', new_xi_m_m)
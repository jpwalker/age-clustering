#!/usr/bin/env python
# create_xi_m_m.py

'''
Created on Jan 27, 2014

@author: jpwalker
'''

import sys
import numpy as np
from IO import readfile
from IO import writefile
from scipy import interpolate as inter
import matplotlib.pyplot as plt
from Correlation_Func import create_corr_struct
from Correlation_Func import write_corr_file


def check_max_min_step(low, high, step):
    if (high - low) % step == 0:
        return True
    else:
        return False

##Program was created to interface Boylan-Kolchin's files with ours
##Basic input for this program are: 
##infile, outfile, minimum_rad, maximum_rad, step_rad, log_flag 
if __name__ == '__main__':
    ##Setup and Input Error check
    infile = None
    outfile = None
    low = None
    high = None
    step = None
    log_flag = False
    try:
        infile = str(sys.argv[1])
        outfile = str(sys.argv[2])
        low = float(sys.argv[3])
        high = float(sys.argv[4])
        step = float(sys.argv[5])
    except IndexError:
        raise IndexError('Check your requiered input parameters: Infile:  {0} Outfile: {1} minimum: '
        '{2} maximum: {3} step: {4}'.format(infile, outfile, low, high, step))
    except ValueError:
        print 'Check your minimum, maximum and step inputs: minimum: {0} maximum: {1} '
        'step: {2}'.format(sys.argv[3], sys.argv[4], sys.argv[5])
    try:
        if sys.argv[6] == 'False' or sys.argv[6] == 'false' or sys.argv[6] == '0':
            log_flag = False
        elif sys.argv[6] == 'True' or sys.argv[6] == 'true' or sys.argv[6] == '1':
            log_flag = True
        else:
            raise TypeError('Log-flag should be be some type of boolean value such as (true, false, 1, or 0).')
    except IndexError:
        print 'No Log-flag given assuming linear space.'
    if not check_max_min_step(low, high, step):
        raise RuntimeError('Given min, max, step don\'t make sense: minimum: {0} maximum: {1} '
        'step: {2}'.format(low, high, step))
    ##Setup and Input Error check complete
    #Create new radius values
    if not log_flag:
        r_new = np.linspace(low, high, (high - low) / step + 1.)
    else:
        r_new = np.logspace(low, high, (high - low) / step + 1.)
    zeros = np.zeros(len(r_new))
    #Read in old correlation file.
    ##THE FOLLOWING ONLY WORKS WITH BOYLAN-KOLCHIN'S CORREL FILES
    infile_data = readfile(infile, col = 4, delim = ' ', skip = 2)
    new_cf_func = inter.splrep(infile_data[0], infile_data[1])
    new_corr = create_corr_struct(r_new, inter.splev(r_new, new_cf_func), zeros, zeros, zeros, 0)
    plt.loglog(infile_data[0], infile_data[1])
    plt.loglog(new_corr['data'].r, new_corr['data'].cf, '*')
    plt.show()
    write_corr_file(outfile, new_corr)
    print 'File {0} saved.'.format(outfile)
'''
Created on Jul 17, 2013

@author: jpwalker
'''

from MillenniumII import *
import matplotlib.pyplot as plt
import numpy as np
import math as mth

def binning(data, data2, limits):
    avg = [[], []]
    med = [[], []]
    for (i, l) in enumerate(limits[0:len(limits) - 1]):
        u = limits[i + 1]
        (data_average, idx) = get_bin_mean(data, l, u)
        if idx != []:
            avg[0].append(data_average)
            med[0].append(np.median(data[idx]))
            avg[1].append(np.average(data2[idx]))
            med[1].append(np.median(data2[idx]))
    return (np.array(avg), np.array(med))
    

def get_bin_mean(data, b_start, b_end):
    idx = np.nonzero(np.logical_and(data >= b_start, data < b_end))[0]
    if idx != []:
        return (np.average(data[idx]), idx)
    else:
        return (None, idx)

if __name__ == '__main__':
    direc = '/home/jpwalker/Desktop/z0_attempt1/'
    infile = 'millenniumIIsnap67age_attempt1057fof.txt'
    age_key = 'merg'
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    #Read in all halos
    halos = read_halo_table_ascii('{0}{1}'.format(direc, infile), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23')
    fof_np = np.array(get_col_halo_table(halos, 'fof_np')) * massconv
    form = np.array(get_col_halo_table(halos, age_key))
    #plt.semilogx(fof_np, form, 'k.')
    lims = 10. ** np.linspace(9, 15, (15.25-9) / .25)
    (avg, med) = binning(fof_np, form, lims)
    plt.semilogx(avg[0], avg[1], '+b', subsx = [2, 3, 4, 5, 6, 7, 8, 9], label = 'Average')
    plt.semilogx(med[0], med[1], 'b', linestyle = 'dashed', label = 'Median')
    MS = 13.5795 - 10.3112 * np.arcsinh(0.0504329 * avg[0] ** 0.08445)
    plt.semilogx(avg[0], MS, 'r', label = 'MS Curve')
    plt.legend()
    plt.xlabel('M [M_sun / h]')
    plt.ylabel('Formation Age Lookback time [Gyr]')
    
    ##Create Second x axis
    xlims = plt.xlim()
    x2 = plt.twiny()
    x2.set_xscale('log')
    x2.set_xlim((xlims[0] / .73, xlims[1] / .73))
    x2.set_xlabel('M [M_sun]')
    
    ##Create second y axis
    ylims = plt.ylim()
    yt = plt.yticks()[0]
    y2 = plt.twinx()
    y2.set_ylim(ylims)
    y2.set_yticks(yt)
    yl = []
    for j in yt:
        if j < 13.5795:
            yl.append('{:5.2f}'.format(1.44224957031 / mth.sinh(0.0969815 * (13.5795 - j))**(2./3.)))
        else:
            yl.append('')
    y2.set_yticklabels(yl)
    y2.set_ylabel('z + 1')
    
    plt.show()
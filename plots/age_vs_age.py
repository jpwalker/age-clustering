'''
Created on Sep 17, 2013

@author: jpwalker
'''

#from Correlation_Func import read_corr_file, calc_bias_cross
from MillenniumII import *
import matplotlib.pyplot as plt
import numpy.random as rnd
import numpy as np
import os
import scipy.stats as sts

def find_centers(xedges):
    if len(xedges) >= 2:
        centers = []
        for (i, x1) in enumerate(xedges): 
            if i <= len(xedges) - 2: centers.append((xedges[i + 1] - x1) / 2. + x1)
        return centers
    else:
        raise ValueError('Number of edges has to be greater than 2')

def plot_percentiles(data, numbins, xlim, ylim, vert = True, color = 'k', linestyle = 'solid', linew = 2):
    perc = 1. / numbins
    p = []
    for i in range(1, numbins):
        p.append(sts.scoreatpercentile(data, i * perc * 100.))
        if vert:
            plt.vlines(p[-1], ylim[0], ylim[1], color, linestyle, linewidth = linew)
        else:
            plt.hlines(p[-1], xlim[0], xlim[1], color, linestyle, linewidth = linew)
    return p

if __name__ == '__main__':
    h = 0.73
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/snap{1}/'.format(home, '67-1')
    age_file = ('attempt1millenniumIIsnap67_500_sub.txt', \
                'attempt1millenniumIIsnap67_500_fof.txt')
    agekeys = ['form_jp', 'form_jp']
    lbls = ['Sub-Max_Tree-Form. Age', 'FOF-Max_tree-Form. Age']
    xi_m_m = '{0}{1}'.format(direc, 'xi_m_m_67.txt')
    num_xbins = 50 #Number of bins on x axis. This is used for contour plot.
    num_ybins = 50 #Number of bins on y axis. This is used for contour plot.
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,17,x,21,22,23,24,27,25,28,26,29'
    halos1 = read_halo_table_ascii('{0}{1}'.format(direc, age_file[0]), \
                                  fmt = fmt)
    halos2 = read_halo_table_ascii('{0}{1}'.format(direc, age_file[1]), \
                                  fmt = fmt)
    print 'File read...Ploting...'
    age1 = np.array(get_col_halo_table(halos1, agekeys[0]))
    age2 = np.array(get_col_halo_table(halos2, agekeys[1]))
    z = np.histogram2d(age1, age2, bins = [num_xbins, num_ybins])
    xcenters = find_centers(z[1])
    ycenters = find_centers(z[2])
    (y, x) = np.meshgrid(xcenters, ycenters)
    #idx = np.where(age1 > age2)
    plt.plot(age1, age2, '*', markersize = 0.9, color = 'k', alpha = 0.1)
#     rng = [min(np.reshape(np.log10(z[0]), num_xbins * num_ybins)), 
#            max(np.reshape(np.log10(z[0]), num_xbins * num_ybins))]
#     if rng[0] == float('-inf'):
#         rng[0] = 0.0001
#     lvls = np.linspace(0.35 * (rng[1] - rng[0]) + rng[0], rng[1], 15)
    plt.contour(x, y, np.log10(z[0]), colors = 'k', levels = [2,3,4,5,6])
    xl = plt.xlim()
    yl = plt.ylim()
    x_perc = plot_percentiles(age1, 5, xl, yl, color = 'r')
    y_perc = plot_percentiles(age2, 5, xl, yl, False, color = 'r')
    
    #Load xi_m_m
    xi_m_m_d = read_corr_file(xi_m_m)
    
    ##Select halos in each age bin
    idx = np.where(np.logical_and(age1 >= x_perc[-1], age2 < y_perc[0]))[0]
    if len(idx) != 0:
        sel_halos = select_halo_table(halos1, idx)
        bias = calc_bias_cross(sel_halos, halos1, xi_m_m_d, MS2 = True)
    plt.xlabel(lbls[0])
    plt.ylabel(lbls[1])
    plt.show()
    plt.plot(bias[0] / h, bias[1])
    plt.xlim([5, 15])
    plt.xlabel('r (Mpc)')
    plt.ylabel('b')
    plt.show()
    
    
'''
Created on Sep 17, 2013

@author: jpwalker
'''

from Correlation_Func import read_corr_file, calc_bias_cross, average_bias
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
            if i <= len(xedges) - 2: centers.append((xedges[i + 1] + x1) / 2.)
        return centers
    else:
        raise ValueError('Number of edges has to be greater than 2')

def plot_percentiles(data, numbins, xlim, ylim, vert = True, color = 'k', 
                     linestyle = 'solid', linew = 1):
    perc = 1. / numbins
    p = []
    for i in range(0, numbins + 1):
        p.append(sts.scoreatpercentile(data, i * perc * 100.))
        if (i != 0 and i != numbins): 
            if vert:
                plt.vlines(p[-1], ylim[0], ylim[1], color, linestyle, linewidth = linew)
            else:
                plt.hlines(p[-1], xlim[0], xlim[1], color, linestyle, linewidth = linew)
    return p

if __name__ == '__main__':
    h = 0.73
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/snap{1}/'.format(home, '67-1')
    age_file = ('attempt1millenniumIIsnap67_500_fof.txt', \
                'attempt1millenniumIIsnap67_500_fof.txt')
    agekeys = ['form_jp', 'form_gao']
    lbls = ['FOF-Form. Age-Max', 'FOF-Form. Age-Root']
    xi_m_m = '{0}{1}'.format(direc, 'xi_m_m_67.txt')
    xi_halos = '{0}{1}'.format(direc, 'attempt1_sub_form_jp/xi_attempt1millenniumII_sub.txt')
    num_xbins = 40 #Number of bins on x axis. This is used for contour plot.
    num_ybins = 40 #Number of bins on y axis. This is used for contour plot.
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,17,x,21,22,23,24,27,25,28,26,29'
    halos1 = read_halo_table_ascii('{0}{1}'.format(direc, age_file[0]), \
                                  fmt = fmt)
    halos2 = read_halo_table_ascii('{0}{1}'.format(direc, age_file[1]), \
                                  fmt = fmt)
    print 'File read...Ploting...'
    age1 = np.array(get_col_halo_table(halos1, agekeys[0]))
    age2 = np.array(get_col_halo_table(halos2, agekeys[1]))
    ## Statistics of the ages
    print('age1 == age2: {0}'.format(float(len(np.where(age1 == age2)[0])) / len(age1)))
    print('age1 < age2: {0}'.format(float(len(np.where(age1 < age2)[0])) / len(age1)))
    print('age1 > age2: {0}'.format(float(len(np.where(age1 > age2)[0])) / len(age1)))
    z = np.histogram2d(age2, age1, bins = [num_xbins, num_ybins])
    xl = (np.min(z[1]), np.max(z[1]))
    yl = (np.min(z[2]), np.max(z[2]))
    xcenters = find_centers(z[1])
    ycenters = find_centers(z[2])
    (x, y) = np.meshgrid(xcenters, ycenters)
    plt.contour(x, y, z[0], colors = 'k', 
                levels = [100, 500, 1000, 5000, 10000])
    #plt.plot(age1, age2, 'k+', alpha = .05)
    plt.xlim(xl[0], xl[1])
    plt.ylim(yl[0], yl[1])
    x_perc = plot_percentiles(age1, 5, xl, yl, color = 'r')
    y_perc = plot_percentiles(age2, 5, xl, yl, False, color = 'r')
    plt.xlabel(lbls[0])
    plt.ylabel(lbls[1])
    plt.imshow(z[0], origin = 'lower', extent = (xl[0], xl[1], yl[0], yl[1]), 
               cmap = 'Greys', vmin = 10000)
    plt.colorbar()
    
    #Load xi_m_m and xi_halos
    xi_m_m_d = read_corr_file(xi_m_m)
    xi_halos_d = read_corr_file(xi_halos)
    
#     bias_img = np.zeros((1000, 1000))
#     for i in range(5):
#         for j in range(5):       
#     ##Select halos in each age bin
#             test1 = np.logical_and(age1 >= x_perc[i], age1 < x_perc[i + 1])
#             test2 = np.logical_and(age2 >= y_perc[j], age2 < y_perc[j + 1])
#             idx = np.where(np.logical_and(test1, test2))[0]
#             if len(idx) != 0:
#                 sel_halos = select_halo_table(halos1, idx)
#             bias = calc_bias_cross(sel_halos, halos1, xi_m_m_d, 
#                                xi_auto_halos = xi_halos_d, MS2 = True)
#             avg_bias = average_bias(bias, 5, 15)
#             (left, right) = (float(x_perc[i] - xl[0]) / (xl[1] - xl[0]) * 999., 
#                              (x_perc[i + 1] - xl[0]) / (xl[1] - xl[0]) * 999.)
#             (down, up) = (float(y_perc[j] - yl[0]) / (yl[1] - yl[0]) * 999., 
#                           (y_perc[j + 1] - yl[0]) / (yl[1] - yl[0]) * 999.)
#             bias_img[down:up, left:right] = avg_bias
#             st = '{0} <= age1 < {1}; {2} <= age2 < {3}; bias: {4}'
#             print(st.format(x_perc[i], x_perc[i + 1], y_perc[j], y_perc[j + 1], 
#                        avg_bias))
#     plt.imshow(bias_img, origin = 'lower', extent = (xl[0], xl[1], yl[0], yl[1]), 
#                cmap = 'binary', alpha = 0.2)
    #plt.colorbar()
    plt.show()
#     plt.plot(bias[0] / h, bias[1])
#     plt.xlim([5, 15])
#     plt.xlabel('r (Mpc)')
#     plt.ylabel('b')
    
    
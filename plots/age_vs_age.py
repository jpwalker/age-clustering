'''
Created on Sep 17, 2013

@author: jpwalker
'''
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
    for i in range(1, numbins):
        if vert:
            plt.vlines(sts.scoreatpercentile(data, i * perc * 100.), ylim[0], ylim[1], color, linestyle, linewidth = linew)
        else:
            plt.hlines(sts.scoreatpercentile(data, i * perc * 100.), xlim[0], xlim[1], color, linestyle, linewidth = linew)

if __name__ == '__main__':
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/'.format(home)
    age_file = ('attempt1millenniumIIsnap67_1057_fof.txt', \
                'attempt1millenniumIIsnap67_1057_sub.txt')
    age_file = age_file[1]
    agekeys = ['assem_jp', 'assem_gao']
    lbls = ['Sub-Max_tree-Assem. Age', 'Sub-Root-Assem. Age']
    num_xbins = 30 #Number of bins on x axis. This is used for contour plot.
    num_ybins = 30 #Number of bins on y axis. This is used for contour plot.
    fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29'
    halos = read_halo_table_ascii('{0}{1}'.format(direc, age_file), \
                                  fmt = fmt)
    print 'File read...Ploting...'
    age1 = np.array(get_col_halo_table(halos, agekeys[0]))
    age2 = np.array(get_col_halo_table(halos, agekeys[1]))
    z = np.histogram2d(age1, age2, bins = [num_xbins, num_ybins])
    xcenters = find_centers(z[1])
    ycenters = find_centers(z[2])
    x = np.zeros_like(z[0])
    y = np.zeros_like(z[0])
    for (x_i, xc) in enumerate(xcenters):
        for (y_i, yc) in enumerate(ycenters):
            x[x_i][y_i] = xc
            y[x_i][y_i] = yc
    idx = np.where(age1 > age2)
    plt.plot(age1[idx], age2[idx], '*', markersize = 0.9, color = 'k')
    rng = [min(np.reshape(np.log10(z[0]), num_xbins * num_ybins)), 
           max(np.reshape(np.log10(z[0]), num_xbins * num_ybins))]
    if rng[0] == float('-inf'):
        rng[0] = 0.0001
    lvls = np.linspace(0.35 * (rng[1] - rng[0]) + rng[0], rng[1], 15)
    plt.contour(x, y, np.log10(z[0]), colors = 'k', levels = lvls)
    xl = plt.xlim()
    yl = plt.ylim()
    plot_percentiles(age1, 5, xl, yl, color = 'r')
    plot_percentiles(age2, 5, xl, yl, False, color = 'r')
    plt.xlabel(lbls[0])
    plt.ylabel(lbls[1])
    plt.show()
    
    
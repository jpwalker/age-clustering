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
    age_file = 'attempt1millenniumIIsnap67_1057_fof.txt'
    agekeys = ['assem_jp', 'assem_gao']
    lbls = ['FOF-Max_tree-Form. Age', 'FOF-Root-Form. Age']
    num_xbins = 30 #Number of bins on x axis. This is used for contour plot.
    num_ybins = 30 #Number of bins on y axis. This is used for contour plot.
    halos = read_halo_table_ascii('{0}{1}'.format(direc, age_file), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29')
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
    
    #Indexing for number statistics later
    idx = np.where(age1 > age2)
    idx1 = np.where(age1 == age2)
    idx2 = np.where(age1 < age2)
    
    ##Plotting 
    plt.figure(1)
    plt.subplot(2,2,4)
    #plt.plot(age1[idx], age2[idx], '.', color = 'k') #Plotting halos in the lower-right quadrant
    rng = [min(np.reshape(np.log10(z[0]), num_xbins * num_ybins)), max(np.reshape(np.log10(z[0]), num_xbins * num_ybins))]
    if rng[0] == float('-inf'):
        rng[0] = 0.0001
    lvls = np.linspace(0.35 * (rng[1] - rng[0]) + rng[0], rng[1], 15)
    plt.contour(x, y, np.log10(z[0]), colors = 'k', levels = lvls)
    #plot_percentiles(data, numbins, xlim, ylim, vert = True, color = 'k', linestyle = 'solid', linew = 2)
    #plot_percentiles(age1, 10, plt.xlim(), plt.ylim())
    #plot_percentiles(age2, 10, plt.xlim(), plt.ylim(), False)
    xl = plt.xlim()
    yl = plt.ylim()
    plot_percentiles(age1, 5, xl, yl, color = 'r')
    plot_percentiles(age2, 5, xl, yl, False, color = 'r')
    plt.xlabel(lbls[0])
    plt.ylabel(lbls[1])
    plt.subplot(2, 2, 2)
    plt.hist(age1, 50, histtype = 'stepfilled')
    plt.xlim(xl)
    plt.ylim(plt.ylim())
    plt.xlabel(lbls[0])
    plot_percentiles(age1, 5, plt.xlim(), plt.ylim(), color = 'r')
    plt.subplot(2, 2, 3)
    plt.hist(age2, 50, histtype = 'stepfilled', orientation = 'horizontal')
    plt.ylim(yl)
    plt.xlim(plt.xlim())
    plt.ylabel(lbls[1])
    plot_percentiles(age2, 5, plt.xlim(), plt.ylim(), False, color = 'r')
    firstquintus = sts.scoreatpercentile(age1, 20.)
    lastquintgao = sts.scoreatpercentile(age2, 80.)
    #print float(len(np.where(np.logical_and(age1 <= firstquintus, age2 >= lastquintgao))[0]))
    print '{0} number of halos with {1} > {2}.'.format(len(idx[0]), agekeys[0], agekeys[1])
    print '{0} number of halos with {1} < {2}.'.format(len(idx2[0]), agekeys[0], agekeys[1])
    print '{0} number of halos with {1} = {2}.'.format(len(idx1[0]), agekeys[0], agekeys[1])
    print '{0} number of halos.'.format(len(age1))
    plt.show()
    
    
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

if __name__ == '__main__':
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/age-clustering attempt 1/z0_attempt1_form_jp/'.format(home)
    age_file = 'millenniumIIsnap67age_attempt1057fof_2.txt'
    agekeys = ['form_jp', 'form_gao']
    lbls = ['Form. Age', 'Lit. Form. Age']
    num_xbins = 30 #Number of bins on x axis. This is used for contour plot.
    num_ybins = 30 #Number of bins on y axis. This is used for contour plot.
    halos = read_halo_table_ascii('{0}{1}'.format(direc, age_file), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,26,28,25,27,29')
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
    plt.plot(age1, age2, '.', color = 'k')
    rng = [min(np.reshape(np.log10(z[0]), num_xbins * num_ybins)), max(np.reshape(np.log10(z[0]), num_xbins * num_ybins))]
    if rng[0] == float('-inf'):
        rng[0] = 0.1
    lvls = np.linspace(0.35 * (rng[1] - rng[0]) + rng[0], rng[1], 15)
    #plt.contour(x, y, np.log10(z[0]), colors = 'r', levels = lvls)
    for i in range(1, 5):
        plt.vlines(sts.scoreatpercentile(age1, i * .2 * 100), 0, 14, 'r', linewidth = 2)
        plt.hlines(sts.scoreatpercentile(age2, i * .2 * 100), 0, 14, 'r', linewidth = 2)
    firstquintus = sts.scoreatpercentile(age1, 20.)
    lastquintgao = sts.scoreatpercentile(age2, 80.)
    print float(len(np.where(np.logical_and(age1 <= firstquintus, age2 > lastquintgao))[0]))
    plt.xlabel(lbls[0])
    plt.ylabel(lbls[1])
    plt.show()
    
    
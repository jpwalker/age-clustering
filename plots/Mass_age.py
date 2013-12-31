'''
Created on Jul 17, 2013

@author: jpwalker
'''

from MillenniumII import *
import matplotlib.pyplot as plt
import numpy as np
import math as mth
import os

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

def plot_age(form, fof_np, age_labels, symbls):
    lims = 10. ** np.linspace(9, 15, (15.25-9) / .25) #These are the limits for the mass bins
    for (i, form_i) in enumerate(form):
        (avg, med) = binning(fof_np[i], form_i, lims)
        plt.semilogx(avg[0], avg[1], marker = symbls[i], subsx = [2, 3, 4, 5, 6, 7, 8, 9], \
                     label = 'Average {0}'.format(age_labels[i]))
        plt.semilogx(med[0], med[1], linestyle = 'dashed', label = 'Median {0}'.format(age_labels[i]))
    #MS = 13.5795 - 10.3112 * np.arcsinh(0.0504329 * avg[0] ** 0.08445)
    #plt.semilogx(avg[0], MS, 'r', label = 'MS Curve')
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
    
def plot_redshift(redshifts, fof_np, age_labels, symbls):
    lims = 10. ** np.linspace(9, 15, (15.25-9) / .25)
    for (i, red_i) in enumerate(redshifts): 
        (avg, med) = binning(fof_np[i], red_i, lims)
        plt.semilogx(avg[0], avg[1], marker = symbls[i], subsx = [2, 3, 4, 5, 6, 7, 8, 9], \
                     label = 'Average {0}'.format(age_labels[i]))
    #plt.semilogx(med[0], med[1], 'b', linestyle = 'dashed', label = 'Median')
    MS = 2.89 * (avg[0] / 10. ** 10.) ** -0.0563
    plt.semilogx(avg[0], MS, 'r', label = 'MS Curve')
    plt.legend()
    plt.xlabel('M [M_sun / h]')
    plt.ylabel('z + 1')
    
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
        yl.append('{:5.2f}'.format(13.5795 - mth.asinh((j / 1.4424957031) ** (-3. / 2.)) / 0.0969815))
    y2.set_yticklabels(yl)
    y2.set_ylabel('Lookbacktime')
    plt.show()    

if __name__ == '__main__':
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/'.format(home)
    age_file = ('attempt1millenniumIIsnap67_1057_fof.txt', 'attempt1millenniumIIsnap67_1057_sub.txt')
    infile = age_file[1]
    age_key = ['assem_gao', 'assem_jp']
    age_labels = ['Sub-Root-Assem. Age', 'Sub-Max_tree-Assem. Age']
    symbls = ['s', '^']
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    #Read in all halos
    halos = read_halo_table_ascii('{0}{1}'.format(direc, infile), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29')
    form = []
    redshifts = []
    fof_np = []
    for i in age_key:
        tempmass = np.array(get_col_halo_table(halos, 'fof_np'))
        tempage = np.array(get_col_halo_table(halos, i))
        if i == 'merg':
            idx = np.where(tempage <= 13.5)
            tempmass = tempmass[idx]
            tempage = tempage[idx]
        fof_np.append(tempmass * massconv)
        form.append(tempage) 
        redshifts.append(1.44224957031 * np.sinh(0.0969815 * (13.5795 - form[-1])) ** (-2. / 3.))
    plot_age(form, fof_np, age_labels, symbls)
    plot_redshift(redshifts, fof_np, age_labels, symbls)
    
'''
Created on Jul 17, 2013

@author: jpwalker
'''

from MillenniumII import *
import matplotlib.pyplot as plt
from matplotlib import rc
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

def plot_age(p, form, fof_np, age_labels, symbls):
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
    
def plot_redshift(p, redshifts, fof_np, age_labels, symbls):
    lims = 10. ** np.linspace(9, 15, (15.25-9) / .25)
    for (i, red_i) in enumerate(redshifts): 
        (avg, med) = binning(fof_np[i], red_i, lims)
        p.semilogx(avg[0], avg[1], marker = symbls[i], subsx = [2, 3, 4, 5, 6, 7, 8, 9], \
                     label = 'Average {0}'.format(age_labels[i]))
    #plt.semilogx(med[0], med[1], 'b', linestyle = 'dashed', label = 'Median')
    MS = 2.89 * (avg[0] / 10. ** 10.) ** -0.0563
    p.semilogx(avg[0], MS, 'r', label = 'MS Curve')
    p.legend(fontsize = "small")
    #p.set_xlabel('M [M_sun]')
    #p.set_ylabel('z + 1')
    p.set_xlim(5e9, 1.1e15)
    p.set_ylim(1.4, 5.22)
    ##Create second y axis

def s_plot(p, fnames, age_keys, age_labels, symbols):
    for i in range(len(fnames)):
        #Read in all halos
        halos = read_halo_table_ascii('{0}{1}'.format(direc, fnames[i]), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29')
        form = []
        redshifts = []
        fof_np = []
        for j in age_keys:
            tempmass = np.array(get_col_halo_table(halos, 'fof_np'))
            tempage = np.array(get_col_halo_table(halos, j))
            if j == 'merg':
                idx = np.where(tempage <= 13.5)
                tempmass = tempmass[idx]
                tempage = tempage[idx]
            fof_np.append(tempmass * massconv / h) ## fof_np is in M_sun units
            form.append(tempage)
            redshifts.append(1.44224957031 * np.sinh(0.0969815 * (13.5795 - form[-1])) ** (-2. / 3.))
        #plot_age(p, form, fof_np, age_labels, symbls)
        plot_redshift(p, redshifts, fof_np, age_labels, symbols)
            
if __name__ == '__main__':
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/snap67/'.format(home)
    age_file = (('attempt1millenniumIIsnap67_1057_fof.txt', 
                 'attempt1millenniumIIsnap67_1057_sub.txt'), 
                ('attempt1millenniumIIsnap67_1057_fof.txt', 
                 'attempt1millenniumIIsnap67_1057_sub.txt'))
    age_key = ((('form_gao', 'form_jp'), ('form_gao', 'form_jp')), 
               (('assem_gao', 'assem_jp'), ('assem_gao', 'assem_jp')))
    age_labels = ((('FOF-Root-Form. Age', 'FOF-Max-Form. Age'), 
                   ('Sub-Root-Form. Age', 'Sub-Max-Form. Age')), 
                  (('FOF-Root-Assem. Age', 'FOF-Max-Assem. Age'), 
                   ('Sub-Root-Assem. Age', 'Sub-Max-Assem. Age')))
    symbls = ((('s', '^'), ('s', '^')), (('s', '^'), ('s', '^')))
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    rc('text', usetex = True)
    ## Create figures and subplots
    (fig, ax) = plt.subplots(2, 2, True, True)
    ## Axis Labels
    fig.text(0.47, 0.03, "M $(\\mathrm{M}_\\odot)$")
    fig.text(0.972,0.62, 'Lookback time (Gyr)', rotation = 'vertical')
    fig.text(0.034, 0.53, "$z+1$", rotation = 'vertical')
    for (i_idx, i) in enumerate(ax):
        for (j_idx, j) in enumerate(i):
            s_plot(j, (age_file[i_idx][j_idx],), age_key[i_idx][j_idx], age_labels[i_idx][j_idx], symbls[i_idx][j_idx])
            if ((i_idx, j_idx) == (0, 1)) or ((i_idx, j_idx) == (1,1)):
                ylims = j.get_ylim()
                yt = j.get_yticks()
                y2 = j.twinx()
                y2.set_ylim(ylims)
                y2.set_yticks(yt)
                yl = []
                for j in yt:
                    yl.append('{:5.2f}'.format(13.5795 - mth.asinh((j / 1.4424957031) ** (-3. / 2.)) / 0.0969815))
                y2.set_yticklabels(yl) 
    plt.show()
            
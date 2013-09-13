#! /usr/bin/env python
##Code plots the bias of halos select based on age selection alone

from MillenniumII import *
from scipy.stats import scoreatpercentile
from os import getcwd
import sys
from subprocess import check_output
from IO import *
import matplotlib.pyplot as plt

def age_sub_select(halos, agekey, leftage, rightage):
    halos2 = create_halo_table()
    for i in halos['data']:
        if i[keys[agekey]] >= leftage and i[keys[agekey]] < rightage:
            halo_table_append(halos2, i)
    return halos2

def calc_corr_funcs(cwd, age_i, selected_halos_filename, all_halos_filename, xi_auto_filename, xi_cross_filename):
    check_output(['2pt-autocorrelation', selected_halos_filename, xi_auto_filename])
    check_output(['2pt-crosscorrelation', selected_halos_filename, all_halos_filename, xi_cross_filename])
    
def preperations(cwd, xi_halos):
    #Read in correlation function for future use
    xi_auto_halos = readfile(xi_halos, col = 3, delim = ',', skip = 2)
    xi_m_m = readfile('{0}xi_m_m.txt'.format(cwd), col = 2, delim = ' ')
    return (xi_auto_halos, xi_m_m)
    
def calc_bias(cwd, xi_cross_filename, xi_m_m, xi_auto_halos, bias_filename):
    age_selected_halos_xi_cross = readfile(xi_cross_filename, col = 3, delim = ',', skip = 2)
    bias = np.array([age_selected_halos_xi_cross[0], age_selected_halos_xi_cross[1] / np.sqrt(xi_m_m[1] * \
                                                                                              xi_auto_halos[1])])
    writefile(bias_filename, bias, delim = ',',  note = 'radii, bias')

def calc_plot_values(cwd, selected_halos, bias_filename, ageky):
    selected_ages = np.array(get_col_halo_table(selected_halos, agekey))
    bias = readfile('{0}bias/bias_0_{1}'.format(cwd, age_i), col = 2, delim = ',', skip = 1)
    idx = np.where(np.logical_and(np.logical_and(bias[0] >= 5., bias[0] <= 25.), bias[1] == bias[1]))
    return (np.average(selected_ages), np.sum(bias[1][idx]) / len(bias[1][idx]))

if __name__ == '__main__':
    #Obtain the parameters from the shell
    agekey = sys.argv[1]
    ifile = sys.argv[2]
    fmtstr = sys.argv[3]
    all_halos_filename = 'halo_table_{0}'.format(ifile)
    #Obtain the cwd to save files
    cwd = '{0}/'.format(getcwd())
    (xi_auto_all_halos, xi_m_m)  = preperations(cwd, '{0}xi_{1}'.format(cwd, ifile))
    #Read in halo file 
    halos = read_halo_table_ascii('{0}{1}'.format(cwd, ifile), fmt = fmtstr)
    num_agebins = 5
    unsorted_ages = get_col_halo_table(halos, agekey)
    low_age = min(unsorted_ages)
    avg_age = []
    bias = []
    for age_i in range(num_agebins + 1):
        print 'Processing age bin: {0}'.format(age_i)
        if age_i < num_agebins:
            high_age = scoreatpercentile(unsorted_ages, (age_i + 1.) * (100.) / num_agebins)
        else:
            high_age = max(unsorted_ages)
        selected_halos = age_sub_select(halos, agekey, low_age, high_age)
        out_halo_name = '{0}halo_tables/halo_table_0_{1}.dat'.format(cwd, age_i)
        #Write selected halos to file
        write_halo_table_ascii(out_halo_name, selected_halos, \
                               fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
        #Calculate the auto, cross and bias for these halos and write out to file
        xi_auto_filename = '{0}auto_corr_func/xi_0_{1}.dat'.format(cwd, age_i)
        xi_cross_filename = '{0}cross_corr_func/xi_0_{1}.dat'.format(cwd, age_i)
        bias_filename = '{0}bias/bias_0_{1}'.format(cwd, age_i)
        calc_corr_funcs(cwd, age_i, out_halo_name, all_halos_filename, xi_auto_filename, xi_cross_filename)
        calc_bias(cwd, xi_cross_filename, xi_m_m, xi_auto_all_halos, bias_filename)
        (x,y) = calc_plot_values(cwd, selected_halos, bias_filename, agekey)
        avg_age.append(x)
        bias.append(y)
    plt.plot(avg_age, bias, '*', color = 'k')
    plt.show()
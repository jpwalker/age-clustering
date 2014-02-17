#!/usr/bin/env python
# ageclustering.py

"""This code reads in MillenniumII data bins it in mass and age and calculates
the bias of these sub-selected halos.
"""

from MillenniumII import *
from math import log10
import sys
from scipy.stats import scoreatpercentile
from os import mkdir, getcwd
from subprocess import check_output
from IO import *
from Correlation_Func import *

def mass_sub_select(halos, leftmass, rightmass):
    halos2 = create_halo_table()
    for i in halos['data']:
        if i.fof_np >= leftmass and i.fof_np < rightmass:
            halo_table_append(halos2, i)
    return halos2

def age_sub_select(halos, agekey, leftage, rightage):
    halos2 = create_halo_table()
    for i in halos['data']:
        if i[keys[agekey]] >= leftage and i[keys[agekey]] < rightage:
            halo_table_append(halos2, i)
    return halos2

def create_folders(direc):
    halo_table_outdirec = '{0}halo_tables/'.format(direc)
    xi_auto_outdirec = '{0}auto_corr_func/'.format(direc)
    xi_cross_outdirec = '{0}cross_corr_func/'.format(direc)
    bias = '{0}bias/'.format(direc)
    try:
        mkdir(halo_table_outdirec)
    except OSError:
        print 'Warning: Halo_tables directory already exists. Rewriting files...'
    try:
        mkdir(xi_auto_outdirec)
    except OSError:
        print 'Warning: Auto_Corr_func directory already exists. Rewriting files...'
    try:
        mkdir(xi_cross_outdirec)
    except OSError:
        print 'Warning: Cross_Corr_func directory already exists. Rewriting files...'
    try:
        mkdir(bias)
    except OSError:
        print 'Warning: Bias directory already exists. Rewriting files...'
    return (halo_table_outdirec, xi_auto_outdirec, xi_cross_outdirec, bias)

def preperations(halos_filename, xi_halos, halos):
    #Calculate the 2pt-auto func. for all halos just read in. This is xi_ML_ML
    print 'Calculating 2pt-autocorrelation function for all halos'
    #Read in correlation function for future use
    xi_auto_halos = calc_auto_corr(halos, xi_halos, halos_filename, MS2 = True)
    xi_m_m = read_corr_file('xi_m_m.txt')
    return (xi_auto_halos, xi_m_m)

def calc_bias(xi_cross, xi_m_m, xi_auto_halos, bias_filename):
    if xi_cross['data'].r == xi_m_m['data'].r and xi_m_m['data'].r == xi_auto_halos['data'].r:
        bias = np.array([xi_cross['data'].r, xi_cross['data'].cf / np.sqrt(xi_m_m['data'].cf * \
                                                                           xi_auto_halos['data'].cf)])
    else:
        raise TypeError('Radius component doesn\'t match between cross, full sample and xi_m_m.')
    writefile(bias_filename, bias, delim = ',',  note = 'radii, bias')
    return bias

def write_properties(filestr, halos, agekey, mass_i, age_i):
    filestr.write('{0}\n'.format('    '.join([str(mass_i), str(age_i), str(halos['length']), \
                                   str(min(get_col_halo_table(halos, 'fof_np'))), \
                                   str(np.median(get_col_halo_table(halos, 'fof_np'))), \
                                   str(np.average(get_col_halo_table(halos, 'fof_np'))), \
                                   str(max(get_col_halo_table(halos, 'fof_np'))), \
                                   str(min(get_col_halo_table(halos, 'max_tree_mass'))), \
                                   str(np.median(get_col_halo_table(halos, 'max_tree_mass'))), \
                                   str(np.average(get_col_halo_table(halos, 'max_tree_mass'))), \
                                   str(max(get_col_halo_table(halos, 'max_tree_mass'))), \
                                   str(min(get_col_halo_table(halos, 'max_tree_mass_snap'))), \
                                   str(np.median(get_col_halo_table(halos, 'max_tree_mass_snap'))), \
                                   str(np.average(get_col_halo_table(halos, 'max_tree_mass_snap'))), \
                                   str(max(get_col_halo_table(halos, 'max_tree_mass_snap'))), \
                                   str(min(get_col_halo_table(halos, 'min_mass_root_max'))), \
                                   str(np.median(get_col_halo_table(halos, 'min_mass_root_max'))), \
                                   str(np.average(get_col_halo_table(halos, 'min_mass_root_max'))), \
                                   str(max(get_col_halo_table(halos, 'min_mass_root_max'))), \
                                   str(min(get_col_halo_table(halos, 'min_mass_root_max_snap'))), \
                                   str(np.median(get_col_halo_table(halos, 'min_mass_root_max_snap'))), \
                                   str(np.average(get_col_halo_table(halos, 'min_mass_root_max_snap'))), \
                                   str(max(get_col_halo_table(halos, 'min_mass_root_max_snap'))), \
                                   agekey, str(min(get_col_halo_table(halos, agekey))), \
                                   str(np.median(get_col_halo_table(halos, agekey))), \
                                   str(np.average(get_col_halo_table(halos, agekey))), \
                                   str(max(get_col_halo_table(halos, agekey)))])))

if __name__ == "__main__":
    if len(sys.argv) == 5:
        h = 0.73
        massconv = 6.885e6 / h
        num_mass_bins = 7
        num_age_bins = 5
        agekey = sys.argv[1]
        #agekey = 'form_jp'
        #Read in data from age files
        indirec = '{0}/'.format(getcwd())
        #indirec = '/Users/jpwalker/Desktop/z0_attempt1_form_jp/'
        infile = sys.argv[2]
        #infile = 'millenniumIIsnap67age_attempt1057fof_2.txt'
        fmt = sys.argv[3]
        #fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,17,x,21,22,23,24,27,25,28,26,29'
        halos = read_halo_table_ascii(indirec + infile, fmt = fmt)
        halos_filename = '{0}halo_table_{1}'.format(indirec, infile)
        xi_halos = '{0}xi_{1}'.format(indirec, infile)
        print 'Halos read into memory...'
        (xi_auto_halos, xi_m_m) = preperations(halos_filename, xi_halos, halos)
        #Create directories for output
        (halo_table_outdirec, xi_auto_outdirec, xi_cross_outdirec, bias_direc) = create_folders(indirec)
        #Mass Selection masses in number of particles
        massbins = [1056, 1885, 1886, 3352, 3353, 5962, 5963, 10602, 10603, 33528, 33529, 106027, 106028, 80000000000]
        massbin = [1, 0]
        #Prepare lists to store results0
        mass_selected_halos = [] #Stores halo tables for mass selected sets
        mass_selected_halos_xi_auto = []
        mass_selected_halos_xi_cross = []
        age_selected_halos = [] #Stores halo tables for mass-age selected sets
        age_selected_halos_xi_auto = [] #Stores the 2pt-autocorr for the age_selected_halos tables
        age_selected_halos_xi_cross = [] #Stores the 2pt-crosscorr for the age_selected halos and all halos table
        testnum = 0
        out = open('{0}properties.dat'.format(indirec), 'w')
        out.write('mass_i    age_i    num    min_mass    median_mass    average_mass    max_mass    min_max_tree_mass    \
        median_max_tree_mass    average_max_tree_mass    max_max_tree_mass    min_max_tree_mass_snap    median_max_tree_mass_snap    \
        average_max_tree_mass_snap    max_max_tree_mass_snap    min_min_mass_root_max    median_min_mass_root_max    \
        average_min_mass_root_max    max_min_mass_root_max    min_min_mass_root_max_snap    median_min_mass_root_max_snap    \
        average_min_mass_root_max_snap    max_min_mass_root_max_snap    age_key    min_age    median_age    average_age    max_age\n')
        for mass_i in range(1, num_mass_bins + 1):
            massbin = [massbins[(mass_i - 1) * 2], massbins[(mass_i - 1) * 2 + 1]]
            if mass_i == num_mass_bins:
                massbin[1] += 1
            currmass_select_halo = mass_sub_select(halos, massbin[0], massbin[1])
            mass_selected_halos.append(currmass_select_halo)
            halo_table_filename = '{0}halo_table_{1}_0.dat'.format(halo_table_outdirec, mass_i)
            print 'Calculating autocorrelation function for mass selected sample.'
            xi_auto_filename = '{0}xi_{1}_0.dat'.format(xi_auto_outdirec, mass_i)
            xi_cross_filename = '{0}xi_{1}_0.dat'.format(xi_cross_outdirec, mass_i)
            write_properties(out, currmass_select_halo, agekey, mass_i, 0)
            calc_auto_corr(currmass_select_halo, xi_auto_filename, halo_table_filename, True)
            xi_cross = calc_cross_corr(currmass_select_halo, halos, xi_cross_filename, '', '', True)
            b = calc_bias(xi_cross, xi_m_m, xi_auto_halos, '{0}bias_{1}_0'.format(bias_direc, mass_i))
            print '{0} halos with {1} <= M < {2} M_Sun'.format(currmass_select_halo['length'], \
                                                           log10(massbin[0] * massconv), \
                                                           log10(massbin[1] * massconv))
            print 'Age statistics of mass bin: min {0} max {1} Gyrs'.format(min(get_col_halo_table(currmass_select_halo, \
                                                                                               agekey)), \
                                                                        max(get_col_halo_table(currmass_select_halo, \
                                                                                               agekey)))
            agebin = [0, 0]
            #Age selection
            for age_i in range(1, num_age_bins + 1): 
                agebin[1] = scoreatpercentile(get_col_halo_table(currmass_select_halo, agekey), \
                                          age_i * 100. / num_age_bins)
                if age_i == num_age_bins:
                    agebin[1] += 0.001
                print 'Age bin {0}: {1} <= Age < {2}'.format(age_i, agebin[0], agebin[1])
                currage_select_halo = age_sub_select(currmass_select_halo, agekey, agebin[0], agebin[1])
                age_selected_halos.append(currage_select_halo)
                print '{0} halos in age bin.'.format(currage_select_halo['length'])
                halo_table_filename = '{0}halo_table_{1}_{2}.dat'.format(halo_table_outdirec, mass_i, age_i)
                xi_auto_filename = '{0}xi_{1}_{2}.dat'.format(xi_auto_outdirec, mass_i, age_i)
                xi_cross_filename = '{0}xi_{1}_{2}.dat'.format(xi_cross_outdirec, mass_i, age_i)
                
                calc_auto_corr(currage_select_halo, xi_auto_filename, halo_table_filename, True)
                xi_cross = calc_cross_corr(currage_select_halo, halos, xi_cross_filename, '', '', True)
                b = calc_bias(xi_cross, xi_m_m, xi_auto_halos, '{0}bias_{1}_{2}'.format(bias_direc, mass_i, age_i))
                write_properties(out, currage_select_halo, agekey, mass_i, age_i)
                testnum += currage_select_halo['length']
                agebin[0] = agebin[1]
            massbin[0] = massbin[1]
        print 'Finished processing {0} halos!'.format(testnum)
        
        #Calculate the clustering based on age dependence only.
        unsorted_ages = get_col_halo_table(halos, agekey)
        low_age = min(unsorted_ages)
        testnum = 0
        for age_i in range(1, num_age_bins + 1):
            print 'Processing age bin: {0}'.format(age_i)
            if age_i < num_age_bins:
                high_age = scoreatpercentile(unsorted_ages, age_i * (100.) / num_age_bins)
            else:
                high_age = max(unsorted_ages) + 1.
            selected_halos = age_sub_select(halos, agekey, low_age, high_age)
            write_properties(out, selected_halos, agekey, 0, age_i)
            print '{0} halos in age bin.'.format(selected_halos['length'])
            out_halo_name = '{0}halo_table_0_{1}.dat'.format(halo_table_outdirec, age_i)
            #Calculate the auto, cross and bias for these halos and write out to file
            xi_auto_filename = '{0}xi_0_{1}.dat'.format(xi_auto_outdirec, age_i)
            xi_cross_filename = '{0}xi_0_{1}.dat'.format(xi_cross_outdirec, age_i)
            bias_filename = '{0}bias_0_{1}'.format(bias_direc, age_i)
            
            calc_auto_corr(selected_halos, xi_auto_filename, out_halo_name, True)
            xi_cross = calc_cross_corr(selected_halos, halos, xi_cross_filename, '', '', True)
            calc_bias(xi_cross, xi_m_m, xi_auto_halos, bias_filename)
            testnum += selected_halos['length']
            #Redefine the low_age for next pass
            low_age = high_age
            #End of the clustering of age selected only subset
        print testnum, halos['length']
        out.close()
    else:
        print 'Error: Check number of arguments'
        raise TypeError
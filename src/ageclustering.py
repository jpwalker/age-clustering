#! /usr/bin/env python
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
import matplotlib.pyplot as plt

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
    write_halo_table_ascii(halos_filename, halos, \
                           fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
    check_output(['2pt-autocorrelation', halos_filename, xi_halos])
    #Read in correlation function for future use
    xi_auto_halos = readfile(xi_halos, col = 3, delim = ',', skip = 2)
    xi_m_m = readfile('{0}xi_m_m.txt'.format(indirec), col = 2, delim = ' ')
    return (xi_auto_halos, xi_m_m)

def calc_bias(xi_cross_filename, xi_m_m, xi_auto_halos, bias_filename):
    age_selected_halos_xi_cross = readfile(xi_cross_filename, col = 3, delim = ',', skip = 2)
    bias = np.array([age_selected_halos_xi_cross[0], age_selected_halos_xi_cross[1] / np.sqrt(xi_m_m[1] * \
                                                                                              xi_auto_halos[1])])
    writefile(bias_filename, bias, delim = ',',  note = 'radii, bias')

if __name__ == "__main__":
    if len(sys.argv) == 4:
        h = 0.73
        massconv = 6.885e6 / h
        num_mass_bins = 7
        num_age_bins = 5
        agekey = sys.argv[1]
        #Read in data from age files
        indirec = '{0}/'.format(getcwd())
        infile = sys.argv[2]
        halos = read_halo_table_ascii(indirec + infile, fmt = sys.argv[3])
        halos_filename = '{0}halo_table_{1}'.format(indirec, infile)
        xi_halos = '{0}xi_{1}'.format(indirec, infile)
        print 'Halos read into memory...'
        (xi_auto_halos, xi_m_m) = preperations(halos_filename, xi_halos, halos)
        #Create directories for output
        (halo_table_outdirec, xi_auto_outdirec, xi_cross_outdirec, bias_direc) = create_folders(indirec)
        #Mass Selection masses in number of particles
        massbins = [1056, 1885, 1886, 3352, 3353, 5962, 5963, 10602, 10603, 33528, 33529, 106027, 106028, 80000000000]
        massbin = [1, 0]
        #Prepare lists to store results
        mass_selected_halos = [] #Stores halo tables for mass selected sets
        mass_selected_halos_xi_auto = []
        mass_selected_halos_xi_cross = []
        age_selected_halos = [] #Stores halo tables for mass-age selected sets
        age_selected_halos_xi_auto = [] #Stores the 2pt-autocorr for the age_selected_halos tables
        age_selected_halos_xi_cross = [] #Stores the 2pt-crosscorr for the age_selected halos and all halos table
        testnum = 0
        out = open('{0}properties.dat'.format(indirec), 'w')
        out.write('mass_i    age_i    num    min_mass    median_mass    average_mass    max_mass    age_key    \
        min_age    median_age    average_age    max_age\n')
        for mass_i in range(1, num_mass_bins + 1):
            massbin = [massbins[(mass_i - 1) * 2], massbins[(mass_i - 1) * 2 + 1]]
            #massbin[1] = scoreatpercentile(get_col_halo_table(halos, 'fof_np'), mass_i * 100. / num_mass_bins)
            if mass_i == num_mass_bins:
                massbin[1] += 1
            currmass_select_halo = mass_sub_select(halos, massbin[0], massbin[1])
            mass_selected_halos.append(currmass_select_halo)
            halo_table_filename = '{0}halo_table_{1}_0.dat'.format(halo_table_outdirec, mass_i)
            write_halo_table_ascii(halo_table_filename, currmass_select_halo, \
                                   fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
            print 'Calculating autocorrelation function for mass selected sample.'
            xi_auto_filename = '{0}xi_{1}_0.dat'.format(xi_auto_outdirec, mass_i)
            xi_cross_filename = '{0}xi_{1}_0.dat'.format(xi_cross_outdirec, mass_i)
            check_output(['2pt-autocorrelation', halo_table_filename, xi_auto_filename])
            check_output(['2pt-crosscorrelation', halo_table_filename, halos_filename, xi_cross_filename])
            calc_bias(xi_cross_filename, xi_m_m, xi_auto_halos, '{0}bias_{1}_0'.format(bias_direc, mass_i))    
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
                out.write('{0}\n'.format('    '.join([str(mass_i), str(age_i), str(currage_select_halo['length']), \
                                   str(min(get_col_halo_table(currage_select_halo, 'fof_np'))), \
                                   str(np.median(get_col_halo_table(currage_select_halo, 'fof_np'))), \
                                   str(np.average(get_col_halo_table(currage_select_halo, 'fof_np'))), \
                                   str(max(get_col_halo_table(currage_select_halo, 'fof_np'))), \
                                   agekey, str(min(get_col_halo_table(currage_select_halo, agekey))), \
                                   str(np.median(get_col_halo_table(currage_select_halo, agekey))), \
                                   str(np.average(get_col_halo_table(currage_select_halo, agekey))), \
                                   str(max(get_col_halo_table(currage_select_halo, agekey)))])))
                print '{0} halos in age bin.'.format(currage_select_halo['length'])
                #Saving halo table to file
                halo_table_filename = '{0}halo_table_{1}_{2}.dat'.format(halo_table_outdirec, mass_i, age_i)
                write_halo_table_ascii(halo_table_filename, currage_select_halo, \
                                   fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
                xi_auto_filename = '{0}xi_{1}_{2}.dat'.format(xi_auto_outdirec, mass_i, age_i)
                xi_cross_filename = '{0}xi_{1}_{2}.dat'.format(xi_cross_outdirec, mass_i, age_i)
                check_output(['2pt-autocorrelation', halo_table_filename, xi_auto_filename])
                check_output(['2pt-crosscorrelation', halo_table_filename, halos_filename, xi_cross_filename])
                calc_bias(xi_cross_filename, xi_m_m, xi_auto_halos, '{0}bias_{1}_{2}'.format(bias_direc, mass_i, age_i))
                testnum += currage_select_halo['length']
                agebin[0] = agebin[1]
            massbin[0] = massbin[1]
        print 'Finished processing {0} halos!'.format(testnum)
        out.close()
    else:
        print 'Error: Check number of arguments'
        raise TypeError
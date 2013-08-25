'''
Created on Aug 22, 2013

@author: jpwalker
'''

from IO import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    direc = '/home/jpwalker/Desktop/z0_attempt1_form/'
    files = ['properties.dat', 'bias_properties.dat']
    out = 'prop_table_attempt1_form.tex'
    data1 = readfile('{0}{1}'.format(direc, files[0]), col = 12, delim = '    ', skip = 1)
    data2 = readfile('{0}{1}'.format(direc, files[1]), col = 3, delim=' ', skip = 1)
    age_bins = 5
    mass_bins = 12
    col_j = ['b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
    for age_i in range(age_bins):
        bias = []
        mass = []
        idx_age = np.where(data1[1] == age_i + 1)
        for j in idx_age[0]:
            idx = np.where(np.logical_and(data2[0] == data1[0][j], data2[1] == age_i + 1))
            if len(data2[0][idx]) == 1:
                bias.append(data2[2][idx][0])
                mass.append(data1[4][j])
            else:
                print "Error in the code!!!!"
        bias = np.array(bias)
        mass = np.array(mass)
        plt.semilogx(mass * massconv, bias, color = col_j[age_i], label = age_i)
    plt.xlabel('Mass [M_sun / h]')
    plt.ylabel('bias')
    plt.show()
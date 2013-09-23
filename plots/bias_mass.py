'''
Created on Aug 22, 2013

@author: jpwalker
'''

from IO import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    h = 0.73
    massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
    direc = '/Users/jpwalker/Desktop/z0_attempt1_form_jp/'
    ifile = 'properties.dat'
    data = readfile('{0}{1}'.format(direc, ifile), col = 12, delim = '    ', skip = 1)
    age_bins = 5
    mass_bins = 7
    col_j = ['b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
    for age_i in range(1, age_bins + 1):
        bias = []
        mass = []
        for mass_i in range(1, mass_bins + 1):
            b_data = readfile('{0}bias/bias_{1}_{2}', col = 2, delim = ',', skip = 1)
            bias.append(data[2][idx][0])
            mass.append(data[4][j])
        bias = np.array(bias)
        mass = np.array(mass)
        plt.semilogx(mass * massconv, bias, color = col_j[age_i], label = age_i)
    plt.xlabel('Mass [M_sun / h]')
    plt.ylabel('bias')
    plt.show()
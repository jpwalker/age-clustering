'''
Created on Sep 17, 2013

@author: jpwalker
'''
from MillenniumII import *
import matplotlib.pyplot as plt
import numpy.random as rnd
import numpy as np

if __name__ == '__main__':
    direc = '/Users/jpwalker/Desktop/z0_attempt1_form_jp/'
    age_file = 'millenniumIIsnap67age_attempt1057fof_2.txt'
    agekey = 'assem'
    halos = read_halo_table_ascii('{0}{1}'.format(direc, age_file), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,25,27,26,28,29')
    print 'File read...Ploting...'
    age1 = np.array(get_col_halo_table(halos, '{0}_jp'.format(agekey)))
    age2 = np.array(get_col_halo_table(halos, '{0}_gao'.format(agekey)))
    idx = rnd.random_integers(0, len(age1), 40000)
    plt.plot(age1[idx], age2[idx], '.', color = 'k')
    plt.xlabel('{0}_jp Age (Gyrs)'.format(agekey))
    plt.ylabel('{0}_gao Age (Gyrs)'.format(agekey))
    plt.show()
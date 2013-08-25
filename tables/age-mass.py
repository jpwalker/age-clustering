'''
Created on Aug 22, 2013
Creates a table for latex where the properties of the age-mass selected samples are listed.
@author: jpwalker
'''

from IO import *
import numpy as np

def write_tex(fn, bn, d1, d2):
    f = open(fn, 'w')
    f.write("""\\begin{deluxetable}{lcccccccc}\n""")
    f.write("""    \\tablehead{\colhead{Name} & \colhead{Bias} & \colhead{Number} & \colhead{Min. Mass} & \colhead{Median Mass} & \colhead{Max. Mass} & \colhead{Min. Age} & \colhead{Median Age} & \colhead{Max. Age}}\n""")
    f.write("""    \\tabletypesize{\\tiny}\n""")
    f.write("""    \\tablewidth{0pt}\n""")
    f.write("""    \\startdata\n""")
    for i in range(len(d1[0])):
        idx = np.where(np.logical_and(d2[0] == d1[0][i], d2[1] == d1[1][i]))
        if len(d2[0][idx]) == 1:
            if i != len(d1[0]) - 1:
                cap = '\\\\'
            else:
                cap = ''
            f.write('\t{0}{1}-{2} & {3:4.3} & {4} & {5} & {6} & {7} & {8:4.3} & {9:4.3} & {10:4.3} {11}\n'\
                    .format(bn, int(d1[0][i]), int(d1[1][i]), d2[2][idx][0], int(d1[2][i]), \
                            int(d1[3][i]), int(d1[4][i]), int(d1[6][i]), d1[8][i], d1[9][i], d1[10][i], cap))
        else:
            print 'Error: Check code!!!!'
    f.write("""    \\enddata\n""")
    f.write("""\\end{deluxetable}""")
    f.close()
    
    
    
if __name__ == "__main__":
    direc = '/home/jpwalker/Desktop/z0_attempt1_form/'
    files = ['properties.dat', 'bias_properties.dat']
    out = 'prop_table_attempt1_form.tex'
    data1 = readfile('{0}{1}'.format(direc, files[0]), col = 12, delim = '    ', skip = 1)
    data2 = readfile('{0}{1}'.format(direc, files[1]), col = 3, delim=' ', skip = 1)
    write_tex('{0}{1}'.format(direc, out), 'HMFA1-', data1, data2)
    
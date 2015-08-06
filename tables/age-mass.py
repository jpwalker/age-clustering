'''
Created on Aug 22, 2013
Creates a table for latex where the properties of the age-mass selected samples are listed.
@author: jpwalker
'''

from os.path import join
from os import environ
from IO import readfile
import numpy as np

def write_tex(fn, bn, d1, d2):
    f = open(fn, 'w')
    
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
    
def setup_file(fn):
    f = open(fn, 'w')
    f.write("""\\begin{deluxetable}{lcccccccc}\n""")
    f.write("""    \\tablehead{\colhead{Name} & \colhead{Bias} & \colhead{Number} & \colhead{Min. Mass} & \colhead{Median Mass} & \colhead{Max. Mass} & \colhead{Min. Age} & \colhead{Median Age} & \colhead{Max. Age}}\n""")
    f.write("""    \\tabletypesize{\\tiny}\n""")
    f.write("""    \\tablewidth{0pt}\n""")
    f.write("""    \\startdata\n""")

if __name__ == "__main__":
    home = environ['HOME']
    b_t_direc = join(home, 'Desktop/age-clustering-data')
    b_o_direc = join(home, 'Google\\ Drive/Age-Clustering\\ Paper')
    tables = ('attempt1_fof_form_jp', 'attempt1_fof_form_gao', 
              'attempt1_fof_assem_jp', 'attempt1_fof_assem_gao', 
              'attempt1_sub_form_jp', 'attempt1_sub_form_gao', 
              'attempt1_sub_assem_jp', 'attempt1_sub_assem_gao')
    table_labels = ('M-Form-FOF', 'R-Form-FOF', 'M-Assem-FOF', 'R-Assem-FOF',
                    'M-Form-sub', 'R-Form-sub', 'M-Assem-sub', 'R-Assem-sub')
    outs = ('prop_table_fof_form_jp.tex', 'prop_table_fof_form_gao.tex', 
            'prop_table_fof_assem_jp.tex', 'prop_table_fof_assem_gao.tex', 
            'prop_table_sub_form_jp.tex', 'prop_table_sub_form_gao.tex', 
            'prop_table_sub_assem_jp.tex', 'prop_table_sub_assem_gao.tex')
    snaps = (22,27,31,36,40,45,51,67)
    zs = (6.196857, 4.179475,3.060424,2.0700316,1.5036374, 0.5641763, 0.)
    snap_postfix = '-1'
    files = ('properties.dat',)
    for (t, l, o) in zip(tables, table_labels, outs):
        o_direc = join(b_o_direc, o)
        setup_file(o_direc)
        for sn in snaps:
            t_direc = join(b_t_direc, 'snap{0}{1}'.format(sn, snap_postfix), t)
            for f in files:
                fn = join(t_direc, f)
                try:
                    data = readfile(fn, col = 28, delim = '    ', skip = 1)
                except IOError:
                    print('Unable to open: {0}'.format(fn))
                write_tex(odirec, 'HMFA1-', data1, data2)
    
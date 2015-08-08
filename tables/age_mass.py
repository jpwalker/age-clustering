'''
Created on Aug 22, 2013
Creates a table for latex where the properties of the age-mass selected samples are listed.
@author: jpwalker
'''

from __future__ import print_function
from os.path import join
from os import environ
from IO import readfile
from sys import stderr
from math import log10
from compute_nu import compute_nu
from compute_nu_eff import calc_bias
from numpy import logical_and

prefix = """\\begin{deluxetable}{lccccccccc}
    \\tablecaption{}
    \\tablehead{\colhead{Name} & \\colhead{Number} & 
    \\colhead{Mass Range} & \\colhead{Median Mass} & \\colhead{Age Range} & 
    \\colhead{Median Age} & \\colhead{$z$} & \\colhead{$\\alpha$} &  
    \\colhead{$\\nu$} & \\colhead{$b$} \\\\ & & 
    \\colhead{$\\log_{10}\\mathrm{M}/\\mathrm{M}_\\odot$} & 
    \\colhead{$\\log_{10}\\mathrm{M}/\\mathrm{M}_\\odot$} & 
    \\colhead{Gyr} & \\colhead{Gyr} & & & &}
    \\tabletypesize{\\tiny}
    \\tablewidth{0pt}
    \\startdata
"""

suffix = """\t\\enddata
\\end{deluxetable}"""

cosmo = {'omega_M_0': 0.25, 'omega_lambda_0': 0.75, 'omega_b_0': 0.045, \
             'h': 0.73, 'sigma_8': 0.9, 'n': 1.0, 'omega_n_0': 0., 'N_nu': 0}
h = cosmo['h']
mass_conv = 6.9E6 / h

def write_tex(f, label, data, end=False):
    b_tex_line = '\t\t{0}{1}'.format(label, '-{0:}-{1:} & {2:,} & \
[{3:4.3},{4:4.3}] & {5:4.3} & [{6:4.3},{7:4.3}] & {8:4.3} & {9:4.3} & {10:4.3} & \
{11:4.3} & {12:4.3}{13}')
    cap = '\\\\\n'
    for i in range(len(data[0])):
        if data[0][i] != 0:
            mass_i = int(data[0][i])
            age_i = int(data[1][i])
            masses = (log10(data[3][i] * mass_conv), 
                      log10(data[6][i] * mass_conv), 
                      log10(data[4][i] * mass_conv))
            ages = (data[24][i], data[27][i], data[25][i])
            #index of average age without age and only mass selection
            idx = logical_and(data[0] == mass_i, data[1] == 0)
            alpha = ages[2] / data[25][idx][0] - 1.
            nu = compute_nu(10. ** masses[2], data[28], cosmo)
            bias = calc_bias(data[29], mass_i, age_i)
            tex_line = b_tex_line.format(mass_i, age_i, int(data[2][i]), 
                                         masses[0], masses[1], masses[2], 
                                         ages[0], ages[1], ages[2], data[28], 
                                         alpha, nu, bias, cap)
            f.write(tex_line)
    
def setup_file(fn):
    f = open(fn, 'w')
    f.write(prefix)
    return f

def close_file(f):
    f.write(suffix)
    f.close()

if __name__ == "__main__":
    home = environ['HOME']
    b_t_direc = join(home, 'Desktop/age-clustering-data')
    b_o_direc = join(home, 'Google Drive/Age-Clustering Paper')
    tables = ('attempt1_fof_form_jp', 'attempt1_fof_form_gao', 
              'attempt1_fof_assem_jp', 'attempt1_fof_assem_gao', 
              'attempt1_sub_form_jp', 'attempt1_sub_form_gao', 
              'attempt1_sub_assem_jp', 'attempt1_sub_assem_gao')
    table_labels = ('M-Form-FOF', 'R-Form-FOF', 'M-Assem-FOF', 'R-Assem-FOF',
                    'M-Form-sub', 'R-Form-sub', 'M-Assem-sub', 'R-Assem-sub')
    titles = ('Max-Formation-FOF Age', 'Root-Formation-FOF Age', 
              'Max-Assembly-FOF Age', 'Root-Assembly-FOF Age', 
              'Max-Formation-subhalo Age', 'Root-Formation-subhalo Age', 
              'Max-Assembly-subhalo Age', 'Root-Assembly-subhalo Age')
    outs = ('prop_table_fof_form_jp.tex', 'prop_table_fof_form_gao.tex', 
            'prop_table_fof_assem_jp.tex', 'prop_table_fof_assem_gao.tex', 
            'prop_table_sub_form_jp.tex', 'prop_table_sub_form_gao.tex', 
            'prop_table_sub_assem_jp.tex', 'prop_table_sub_assem_gao.tex')
    snaps = (22, 27, 31, 36, 40, 45, 51, 67)
    zs = (6.196857, 4.179475, 3.060424, 2.0700316, 1.5036374, 0.98870987, 
          0.5641763, 0.)
    snap_postfix = '-1'
    files = 'properties.dat'
    for (t, l, o, tt) in zip(tables, table_labels, outs, titles):
        o_direc = join(b_o_direc, o)
        of = setup_file(o_direc)
        for (sn, z) in zip(snaps, zs):
            t_direc = join(b_t_direc, 'snap{0}{1}'.format(sn, snap_postfix), t)
            #data = []
            #for f in files:
            fn = join(t_direc, files)
            try:
                #data.append(readfile(fn, col = 28, delim = '    ', skip = 1))
                data = readfile(fn, col = 28, delim = '    ', skip = 1)
                data.extend((z, t_direc))
            except IOError:
                print('Unable to open: ', fn, file=stderr)
                data = None
            if data != None:
                write_tex(of, l, data, sn == snaps[-1])
        close_file(of)
'''
Created on Nov 12, 2015

@author: jpwalker
'''

from MillenniumII import read_halo_table_ascii
from os import environ
from os.path import join

def init_direc():
    hm = environ['HOME']
    snap = 67
    i = 0
    j = 1
    snap_suffix = '-1'
    d_snap = join('snap{0}{1}'.format(snap, snap_suffix))
    d_prefix = 'attempt1'
    halo_type = 'sub'
    age_def = 'form_jp'
    d_age = join('{0}_{1}_{2}'.format(d_prefix, halo_type, age_def))
    d_halo = join('halo_tables', 'halo_table_{0}_{1}.dat'.format(i, j))
    fn = join(hm, 'Desktop', 'age-clustering-data', d_snap, d_age, d_halo)

if __name__ == '__main__':
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,17,x,x,x'
    fn = init_direc()
    main_sample = read_halo_table_ascii(fn, fmt, skip = 1)
    
    
'''
Created on Nov 12, 2015

@author: jpwalker
'''

from MillenniumII import read_halo_table_ascii
from os import environ, times, getpid
from os.path import join
from random import choice, randint, seed
from itertools import ifilter
from threading import RLock, Thread

def params(num_halos):
    # Determine number of halos in each subsample used in future bootstrap 
    # samples.
    if num_halos >= 800:
        ns = num_halos // 100
    else:
        ns = 8
    # Number of bootstrap samples created.
    n_resmp = 100
    # Determine the seed for the RNG.
    t = times()
    sd = hash(hash(t[0]) + hash(t[4]) + hash(getpid()))
    seed(sd)
    return {'ns':ns, 'seed':seed, 'nr':n_resmp, 'nh':num_halos}

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
    return join(hm, 'Desktop', 'age-clustering-data', d_snap, d_age, d_halo)
    

def set_idx1(params):
    idx = []
    temp = [randint(1, params['ns']) for _ in range(params['nh'])]
    for i in range(params['ns']):
        idx.append(range(params['nh'])[temp == i])
    return tuple(idx)

def set_idx2 (params):
    smp = 1
    idx = []
    while smp <= params['ns']:
        lmb = lambda x: x % params['ns'] + 1 == smp
        idx.append([i for i in ifilter(lmb, range(params['nh']))])
        smp += 1
    return tuple(idx)

    
if __name__ == '__main__':
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,17,x,x,x'
    fn = init_direc()
    main_sample = read_halo_table_ascii(fn, fmt, skip = 1)
    params = params(main_sample['length'])
    idx = set_idx2(params)
    from matplotlib.pyplot import hist, show
    hist(idx, bins = params['ns'])
    show()
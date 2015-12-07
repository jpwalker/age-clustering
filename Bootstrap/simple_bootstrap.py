'''
Created on Nov 12, 2015

@author: jpwalker
'''

from MillenniumII import read_halo_table_ascii, select_halo_table,\
    create_halo_table, halo_table_extend
from os import environ, times, getpid
from os.path import join
from random import randint, seed, sample, choice
from threading import Thread, RLock

def create_params(num_halos):
    # Determine number of halos in each subsample used in future bootstrap 
    # samples.
    if num_halos >= 800:
        if num_halos % 100 != 0:
            ns = (num_halos // 100) + 1 # Number of samples
        else:
            ns = num_halos // 100 # Number of samples
        nhs = 100 # Number of halos in samples
    else:
        ns = 8 # Number of samples
        nhs = num_halos // 8 # Number of halos in samples
    n_resmp = 100 # Number of bootstrap resamples created.
    # Determine the seed for the RNG.
    t = times()
    sd = hash(hash(t[0]) + hash(t[4]) + hash(getpid()))
    seed(sd)
    return {'ns':ns, 'seed':seed, 'nr':n_resmp, 'nh':num_halos, 'nhs':nhs}

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

def set_idx2(params):
    nh = params['nh']
    av_idx = range(nh)
    idx = []
    nhs = params['nhs']
    for _ in range(params['ns']):
        if nh >= nhs:
            temp = sample(av_idx, nhs)
            for i in temp:
                temp_idx = av_idx.index(i)
                _ = av_idx.pop(temp_idx)
            idx.append(temp)
        else:
            idx.append(av_idx)
        nh = len(av_idx)
    return tuple(idx)

    
def create_samples(halos, idxs):
    samples = []
    for idx in idxs:
        samples.append(select_halo_table(halos, idx))
    return samples

def create_bootstraps(params, samples):
    nbs = params['ns'] * 3 # Number of samples contained in each bootstrap
                            # resample is 3 times the original sample.
    BS_samples = []
    for _ in xrange(params['nr']):
        BS_samples.append(create_halo_table())
        for _ in xrange(nbs):
            halo_table_extend(BS_samples[-1], choice(samples))
    return BS_samples

def thread_func(samples):
    for smp in samples:
        calc_bias_cross(halo_table1, halo_table2, xi_m_m, halo_file1 = '', \
                    halo_file2 = '', cross_filename = '', auto_filename = '', 
                    bias_filename = '', xi_auto_halos = None, MS2 = False)

def setup_threads(params, samples, num=8):
    ns = params['ns']
    thrds = []
    sample_start = 0
    sample_end = ns // num + 1
    for i in range(num):
        arg = (samples[sample_start:sample_end])
        thrds.append(Thread(target=thread_func, args=arg))
        sample_start = sample_end + 1
        sample_end += ns // num + 1
        if sample_end > ns - 1:
            sample_end = ns - 1
        
if __name__ == '__main__':
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,17,x,x,x'
    fn = init_direc()
    main_sample = read_halo_table_ascii(fn, fmt, skip = 1)
    params = create_params(main_sample['length'])
    idxs = set_idx2(params)
    draw_samples = create_samples(main_sample, idxs)
    BS_samples = create_bootstraps(params, draw_samples)
    setup_threads()
    for i in BS_samples:
#     from matplotlib.pyplot import hist, show
#     hist(idx, bins = params['ns'])
#     show()
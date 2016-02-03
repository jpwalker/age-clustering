#!/usr/bin/env python
'''
Created on Nov 12, 2015

@author: jpwalker
'''

from MillenniumII import read_halo_table_ascii, select_halo_table,\
    create_halo_table, halo_table_extend
from os import environ, times, getpid, makedirs
from os.path import join, exists
from random import randint, seed, sample, choice
from Correlation_Func import calc_bias_cross, read_corr_file
from threading import Thread
from cProfile import run

def create_params(nh):
    # Determine number of halos in each subsample used in future bootstrap 
    # samples.
#     if num_halos >= 1000:
#         nhs = 100 # Number of halos in samples
#         if num_halos % nhs != 0:
#             ns = (num_halos // nhs) + 1 # Number of samples
#         else:
#             ns = num_halos // nhs # Number of samples
#     else:
    ns = 10 # Number of samples
    nhs = nh // ns # Number of halos in each sample on average
    n_resmp = 100 # Number of bootstrap samples created.
    # Determine the seed for the RNG.
    t = times()
    sd = hash(hash(t[0]) + hash(t[4]) + hash(getpid()))
    seed(sd)
    return {'ns':ns, 'seed':seed, 'nr':n_resmp, 'nh':nh, 'nhs':nhs}

def init_direc():
    hm = environ['HOME']
    snap = 67
    i = 0
    j = 1
    snap_suffix = '-1'
    xi_m_m_fn = 'xi_m_m.txt'
    xi_all_fn = 'xi_attempt1millenniumII_sub.txt'
    d_ahalo = 'halo_table_attempt1millenniumII_sub.txt'
    d_snap = join('snap{0}{1}'.format(snap, snap_suffix))
    d_prefix = 'attempt1'
    halo_type = 'sub'
    age_def = 'form_jp'
    d_age = join('{0}_{1}_{2}'.format(d_prefix, halo_type, age_def))
    d_halo = join('halo_tables', 'halo_table_{0}_{1}.dat'.format(i, j))
    # Input Files
    temp = join(hm, 'Desktop', 'age-clustering-data', d_snap, d_age,)
    d_halo_fl = join(temp, d_halo)
    d_ahalo_fl = join(temp, d_ahalo)
    xi_m_m_fl = join(temp, xi_m_m_fn)
    xi_all_halo_fl = join(temp, xi_all_fn)
    # Output Files
    d_BS = join(temp, 'BS_{0}_{1}'.format(i, j))
    # These are meant to be assigned a BS idx
    temp = join(d_BS,'halo_tables')
    if not exists(temp):
        makedirs(temp)
    BS_ht_fl = join(temp, 'BS_{0}')
    temp = join(d_BS, 'cross')
    if not exists(temp):
        makedirs(temp)
    BS_xi_fl = join(temp,'xi_{0}')
    temp = join(d_BS, 'bias')
    if not exists(temp):
        makedirs(temp)
    BS_b_fl = join(temp, 'bias_{0}')
    inp = {'ht':d_halo_fl,'a_ht':d_ahalo_fl,'xm':xi_m_m_fl,'xa':xi_all_halo_fl}
    out = {'ht':BS_ht_fl,'xi':BS_xi_fl,'b':BS_b_fl}
    return (inp, out)
    
def set_idx1(params):
    idx = []
    temp = [randint(1, params['ns']) for _ in range(params['nh'])]
    for i in range(params['ns']):
        idx.append(range(params['nh'])[temp == i])
    return tuple(idx)

def set_idx2(params):
    nh = params['nh']
    av_idx = range(nh) # list of available halo indecies
    idx = []
    nhs = params['nhs']
    for _ in range(params['ns']):
        if nh >= nhs:
            temp = sample(av_idx, nhs)
            _ = [av_idx.pop(av_idx.index(i)) for i in temp]
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
    nbs = params['ns'] * 3 # Number of halos contained in each bootstrap
                            # resample is 3 times the original sample.
    BS_samples = []
    for _ in xrange(params['nr']):
        BS_samples.append(create_halo_table())
        for _ in xrange(nbs):
            halo_table_extend(BS_samples[-1], choice(samples))
        print(BS_samples[-1]['length'])
    return BS_samples

def thread_func(samples, smp_idx_start, a_halos, xi_m_m, xi_all, of):
    #smp_idx_start is the starting indesx number used to uniquely save data.
    #a_halos is a halo table with all halos used in the cross-correlation.
    #xi_all, xi_m_m holds the autocorrelation function of all halos and matter.
    #of is the output file.
    for (t_idx, smp) in enumerate(samples):
        idx = t_idx + smp_idx_start
        print(idx)
        hf = of['ht'].format(idx)
        crsf = of['xi'].format(idx)
        bf = of['b'].format(idx)
        run("_ = calc_bias_cross(smp, a_halos, xi_m_m, halo_file1 = hf, \
                            cross_filename = crsf, bias_filename = bf, \
                            xi_auto_halos = xi_all, MS2 = True)")

def setup_threads(params, fn_i, fn_o, samples, num=1):
    nr = params['nr']
    thrds = []
    sample_start = 0
    delta = nr // num + 1
    sample_end = delta
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,17,x,x,x'
    all_ht = read_halo_table_ascii(fn_i['a_ht'], fmt, skip = 1)
    xi_m_m = read_corr_file(fn_i['xm'])
    xi_all = read_corr_file(fn_i['xa'])
    for _ in xrange(num):
        arg = (samples[sample_start:sample_end], sample_start, all_ht, 
               xi_m_m, xi_all, fn_o)
        thrds.append(Thread(target=thread_func, args=arg))
        sample_start = sample_end + 1
        sample_end += delta
        if sample_end > nr - 1:
            sample_end = nr - 1
    return thrds
        
if __name__ == '__main__':
    fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,17,x,x,x'
    (fn_i, fn_o) = init_direc()
    main_sample = read_halo_table_ascii(fn_i['ht'], fmt, skip = 1)
    params = create_params(main_sample['length'])
    idxs = set_idx2(params)
    draw_samples = create_samples(main_sample, idxs)
    main_sample = []
    BS_samples = create_bootstraps(params, draw_samples)
    draw_samples = []
    print(len(BS_samples))
    thrds = setup_threads(params, fn_i, fn_o, BS_samples, num=1)
    for thrd in thrds:
        thrd.start()
    for thrd in thrds:
        thrd.join()
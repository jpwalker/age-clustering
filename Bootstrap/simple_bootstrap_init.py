#!/usr/bin/env python
'''
simple_bootstrap_init -- Init. for bias_bootstrap.py

simple_bootstrap_init is an initialization code for simple_bootstrap.py that 
sets up the argument parser and data to process for bias_bootstrap.py.

@author:     jpwalker
@contact:    jpwalker@physics.rutgers.edu
@deffield    updated: 2-5-16
'''

from argparse import ArgumentParser, FileType

rf = FileType('r') #Read in file type
hlp = ('Path to file for halo_tbl_1. Bootstraps will be created from \
halo_tbl_1.', 
'Path to file for halo_tbl_2. The created bootstraps from halo_tbl_1 will be \
cross-correlated with halo_tbl_2.', 
'Path to file containing the 2pt-autocorrelation function for matter in the \
universe.', 
'The 2pt- autocorrelation function for halo_tbl_2. If not given it has to be \
calculated.')
std_args = (('halo_tbl_1',{'action':'store', 'nargs':1, 'type':rf,
                           'help':hlp[0]}),
            ('halo_tbl_2', {'action':'store', 'nargs':1, 'type':rf,
                            'help':hlp[1]}),
            ('xi_m_m', {'action':'store', 'nargs':1, 'type':rf, 
                        'help':hlp[2]}),
            ('--xi_ht2', {'action':'store', 'nargs':1, 'type':rf,
                          'help':hlp[3], 'metavar':'xi_halo_tbl_2'}))

def arg_parser():
    arg_kwds = {'description':'Creates bootstrap samples of halo_tbl_1 and \
    cross-correlates it with halo_tbl_2 to find halo bias for each bootstrap \
    sample with the given xi_m_m.', 'epilog':'Version 1.0 : 2-5-16'}
    return ArgumentParser(**arg_kwds)

def arguments(prs, args=std_args):
    '''Setup arguments for parsing for the parser in prs.'''
    for arg in args:
        prs.add_argument(arg[0], **arg[1])
    return prs

if __name__ == "__main__":
    parser = arguments(arg_parser())
    parser.parse_args(['-h'])
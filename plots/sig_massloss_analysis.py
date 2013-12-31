'''
Created on Dec 10, 2013

@author: jpwalker
'''

#Todo List
#1. Make figure for methodology section where I show 



import MillenniumII as ml
import os
from subprocess import check_output
from IO import readfile
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}/Projects/age-clustering/plots/'.format(home)
    ifilearr = ['sig_massloss.txt', 'no_sig_massloss.txt']
    for ifile in ifilearr: 
        data = ml.read_halo_table_ascii('{0}{1}'.format(direc, ifile), 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,x,x,x,x,x,x,x')
        x = np.array(ml.get_col_halo_table(data,'x'))
        y = np.array(ml.get_col_halo_table(data, 'y'))
        z = np.array(ml.get_col_halo_table(data, 'z'))
        out_halo_name = '{0}halo_{1}'.format(direc, ifile)
        ml.write_halo_table_ascii(out_halo_name, data, fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
        xiauto_file = '{0}xi_{1}'.format(direc, ifile)
        #check_output(['2pt-autocorrelation', out_halo_name, xiauto_file])
        #xi_auto = readfile(xiauto_file, 3, ',', 2)
        plt.plot(x, y, '+', markersize = 0.9, label = ifile)
        plt.show()
        #plt.loglog(xi_auto[0],xi_auto[1], label = ifile)
    #plt.legend()
    #plt.show()
    #haloid, subhaloid, treeid, descendantid, lastprogenitorid, snapnum, sub_np, x, y, z, firsthaloinfofgroupid, radii, fofid, fof_np, firstsubhaloid, max_tree_mass, max_tree_mass_snap, min_mass_root_max, min_mass_root_max_snap, assem_gao, assem_jp, form_gao, form_jp, merg
    #check_output(['2pt-crosscorrelation', out_halo_name, halos_filename, xi_cross_filename])
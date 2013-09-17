#Code recreates figure2 in Gao et al. 2005 using data from the Millennium-II simulation 
import matplotlib.pyplot as plt
from MillenniumII import *
from IO import *

direc = '/home/jpwalker/Desktop/z0_attempt6/'
infile = 'millenniumIIsnap67age_attempt1057fof_mod.txt'
h = 0.73
massconv = 6.885e6 #Mass conversion reports mass in M_sun/h
#Read in the 2pt-autocorrelation function for all halos
pos_all = read_halo_table_ascii('{0}halo_table_{1}'.format(direc, infile), \
                            fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,x,x,x,x', skip = 1)
smpl = sample_table(pos_all, 25000)
#Read in the properties file were mass and age properties are stored.
prop = readfile('{0}properties.dat'.format(direc), col = 8, delim = '    ', skip = 1)
xrng = (40, 60)
yrng = (40, 60)
plt.figure(1)
temp = 220
j = [1, 5]
col_j = ['b', 'r']
lbl_coords = [[0.25, 0.65, 0.25], [0.85, 0.85, 0.4]]
for mass_i in range(1,4):
    plt.subplot(temp + mass_i)
    plt.xlim(xrng)
    plt.ylim(yrng)
    plt.scatter(get_col_halo_table(smpl, 'x'), get_col_halo_table(smpl, 'y'), marker = '.', color = 'k')    
    mass = []
    for (i, age_i) in enumerate(j):
        idx = np.where(np.logical_and(prop[0] == mass_i, prop[1] == age_i))[0][0]
        mass.extend([prop[3][idx], prop[4][idx]])
        h_t = read_halo_table_ascii('{0}halo_tables/halo_table_{1}_{2}.dat'.format(direc, mass_i, age_i), \
                              fmt = 'x,x,x,x,x,x,x,7,8,9,x,x,x,x,x,x,x,x,x,x,x', skip = 1)
        plt.scatter(get_col_halo_table(h_t, 'x'), get_col_halo_table(h_t, 'y'), s = 40,  marker = 'x', \
                    linewidth = 3.5, color = col_j[i])
        plt.xlabel('x [Mpc / h]')
        plt.ylabel('y [Mpc / h]')
    mass = np.array(mass) * massconv
    #n = int(np.log10(max(mass)))
    #plt.figtext(lbl_coords[0][mass_i - 1], lbl_coords[1][mass_i - 1], \
                #'[{0:1.1f}, {1:1.1f}] x 10^{2} M_sun/h'.format(min(mass) / 10.** n, max(mass) / 10. ** n, n))    
plt.show()
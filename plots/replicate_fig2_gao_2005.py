#Code recreates figure2 in Gao et al. 2005 using data from the Millennium-II simulation 
import matplotlib.pyplot as plt
from IO import *

direc = '/home/jpwalker/Desktop/z0_attempt6/'
infile = 'millenniumIIsnap67age_attempt1057fof_mod.txt'
h = 0.73
massconv = 6.885e6 / h #Mass conversion reports mass in M_sun/h Add /h for M_sun
#Read in the 2pt-autocorrelation function for all halos
xi_all = readfile('{0}xi_{1}'.format(direc, infile), col = 3 , delim = ',', skip = 2)
#Read in the properties file were mass and age properties are stored.
prop = readfile('{0}properties.dat'.format(direc), col = 8, delim = '    ', skip = 1)
xrng = (1,45)
plt.figure(1)
temp = 220
j = [1, 5]
col_j = ['b', 'r']
lbl_coords = [[0.25, 0.65, 0.25, 0.65], [0.85, 0.85, 0.4, 0.4]]
for mass_i in range(1,5):
    plt.subplot(temp + mass_i)
    plt.xlim(xrng)
    mass = []
    for (i, age_i) in enumerate(j):
        idx = np.where(np.logical_and(prop[0] == mass_i, prop[1] == age_i))[0][0]
        mass.extend([prop[3][idx], prop[4][idx]])
        xi_hml = readfile('{0}cross_corr_func/xi_{1}_{2}.dat'.format(direc, mass_i, age_i), col = 3, delim = ',', skip = 2)
        xi_m_m = readfile('{0}xi_m_m.txt'.format(direc), col = 2, delim = ' ')
        plt.loglog(xi_m_m[0], xi_m_m[1], color = 'g', label = 'xi_m_m')
        plt.loglog(xi_hml[0], xi_hml[1] ** 2. / xi_all[1], color = col_j[i])
        plt.loglog(xi_all[0], xi_all[1], color = 'k')
        plt.xlabel('r [Mpc / h]')
        plt.ylabel('xi(r)')
    mass = np.array(mass) * massconv
    n = int(np.log10(max(mass)))
    plt.figtext(lbl_coords[0][mass_i - 1], lbl_coords[1][mass_i - 1], \
                '[{0:1.2f}, {1:1.2f}] x 10^{2} M_sun'.format(min(mass) / 10.** n, max(mass) / 10. ** n, n))    
plt.show()
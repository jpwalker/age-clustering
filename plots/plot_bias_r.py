#Code recreates figure2 in Gao et al. 2005 using data from the Millennium-II simulation 
#Except we are plotting bias(r)
import matplotlib.pyplot as plt
from MillenniumII import *
from IO import *
import Correlation_Func as corr
import os

snap = 67
snap_post = '-1'
home = '{0}/'.format(os.environ['HOME'])
agedirec = 'attempt1_sub_form_jp'
direc = '{0}Desktop/age-clustering-data/snap{1}{2}/{3}/'.format(home, snap, snap_post, agedirec)
infile = 'attempt1millenniumII_sub.txt'
outfile = 'bias_properties.dat'
xscale = (5, 25)
yscale = (0.5, 2.7)
h = 0.73
massconv = 6.885e6 #Mass conversion reports mass in M_sun
#Read in the matter matter 2pt-autocorrelation function
xi_m_m = corr.read_corr_file('{0}xi_m_m.txt'.format(direc))
#Read in the properties file were mass and age properties are stored.
prop = readfile('{0}properties.dat'.format(direc), col = 28, delim = '    ', skip = 1)
plt.figure(1)
temp1 = 3
temp2 = 3
j = [1, 2, 3, 4, 5] #Age bins which will be plotted
col_j = ['b', 'c', 'g', 'm', 'r'] #Colors of Age bins that are plotted
#lbl_coords = [[0.25, 0.65, 0.25, 0.65], [0.85, 0.85, 0.4, 0.4]] #Coords of labels on plot
stored_bias = [[], [], []]
for mass_i in [0]:#range(1, 9):
    plt.subplot(temp1, temp2, mass_i)
    plt.axhline(1., linestyle = 'k-', linewidth = 2)
    for (i, age_i) in enumerate(j):
        idx = np.where(np.logical_and(prop[0] == mass_i, prop[1] == age_i))[0][0]
        mass = np.array([prop[3][idx], prop[6][idx]]) * massconv
        bias = readfile('{0}bias/bias_{1}_{2}'.format(direc, mass_i, age_i), col = 2, delim = ',', skip = 1)
        idx = np.where(np.logical_and(np.logical_and(bias[0] >= 5., bias[0] <= 25.), bias[1] == bias[1]))
        stored_bias[2].append(np.sum(bias[1][idx]) / len(bias[1][idx]))
        stored_bias[0].append(mass_i)
        stored_bias[1].append(age_i)
        plt.title('{0:.2E} <= M < {1:.2E} [M_Sun / h]'.format(mass[0], mass[1]), fontsize = 'medium')
#         plt.figtext(lbl_coords[0][mass_i - 1], lbl_coords[1][mass_i - 1] - .03 * (i + 1), \
#                '[bias_{0}_{1}: {2}]'.format(mass_i, age_i, stored_bias[2][-1]), color = col_j[i])
        plt.plot(bias[0], bias[1], linewidth = 3.5, color = col_j[i])
        plt.xlim(xscale)
        plt.ylim(yscale)
        plt.xlabel('r [Mpc / h]')
        plt.ylabel('b(r)')
#         mass = np.array(mass) * massconv
#         n = int(np.log10(max(mass)))
#         plt.figtext(lbl_coords[0][mass_i - 1], lbl_coords[1][mass_i - 1], \
#                '[{0:1.1f}, {1:1.1f}] x 10^{2} M_sun/h'.format(min(mass) / 10.** n, max(mass) / 10. ** n, n))
plt.show()
stored_bias = np.array(stored_bias)
writefile('{0}{1}'.format(direc, outfile), stored_bias, delim = ' ', note = 'mass_i    age_i    bias')

import matplotlib.pyplot as plt
from IO import *

if __name__ == '__main__':
    direc = '/home/jpwalker/Desktop/z0_attempt4/'
    mass_bins = 5
    age_bins = 1
    
    #Read in autocorr for full sample
    full = readfile('{0}xi_millenniumIIsnap67age_attempt1057fof.txt'.format(direc), 3, ',', 2)   
    
    #Setup colors for plotting
    clr = []
    for i in np.arange(0., 256., 255. / (age_bins - 1)): clr.append([i,0,0])
    clr = np.array(clr) / 255.
    
    #Set integers for plotting
    c = 0
    d = 0
    for i in range(1, mass_bins + 1):
        for j in range(1, age_bins + 1):
            f = '{0}cross_corr_func/xi_{1}_{2}.dat'.format(direc, i, j)
            data = readfile(f, 3, ',', 2)
            lbl = f.split('{0}cross_corr_func/'.format(direc))[1].split('.dat')[0]
            plt.loglog(data[0], data[1] ** 2. / full[1], label = lbl, color = tuple(clr[c]), linewidth = (d + 1.) / 2. + 1. / 2.)
            c += 1
            if c == age_bins:
                c = 0
                d += 1
    plt.xlabel('r [Mpc / h]')
    plt.ylabel('xi(r)')
    plt.legend()
    plt.show()
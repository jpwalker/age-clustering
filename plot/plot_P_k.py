'''
Created on Jun 11, 2013

@author: jpwalker
'''
import IO as p
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    files = ['wavenumber_pknowiggle_z=0.txt', 'wavenumber_pknowiggle_z=30.txt', \
             'wmap5baosn_max_likelihood_matterpower_at_z=30.dat', \
             'wmap5baosn_max_likelihood_matterpower.dat', 'MSII-Pk.dat']
    c = ['b', 'g', 'r', 'c', 'm']
    for (i, f) in enumerate(files):
        data = p.readfile('/home/jpwalker/Downloads/eisensteinhu/{0}'.format(f))
        if i == 4:
            q2 = 1
            q1 = 2 * np.pi ** 2. / (data[0] / q2) ** 3.
        else:
            q1 = 1.
            q2 = 1.
        plt.loglog(data[0] / q2, data[1] * q1, color = c[i], label = f)
    plt.legend(loc = 3)
    plt.xlabel('k (h / Mpc)')
    plt.ylabel('P(k) (Mpc / h)^3')
    plt.show()
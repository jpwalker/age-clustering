'''
Created on Mar 4, 2015

@author: jpwalker
'''

import numpy as np
import matplotlib.pyplot as plt
from math import exp

if __name__ == '__main__':
    trans = 1000.
    best_fit = (7.09088257E1, 3.21411038E-2, -7.03202061E1)
    alpha = (-0.5, 0.5)
    color = ('blue', 'red')
    nu0 = (best_fit[0] * exp(best_fit[1] * a) + best_fit[2] for a in alpha)
    nu = np.linspace(0., 3.5, 1000)
    nu_eff = ((nu - n0) / (1. + np.exp(-trans * (nu - n0))) + n0 for n0 in nu0)
    for (i, y) in enumerate(nu_eff):
        plt.plot(nu,y, color[i])
    plt.show()    
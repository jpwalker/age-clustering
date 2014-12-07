#Age Histogram
from MillenniumII import *
import matplotlib.pyplot as plt
import os
import numpy as np

if __name__ == "__main__":
    home = '{0}/'.format(os.environ['HOME'])
    direc = '{0}Desktop/age-clustering-data/snap67-1/'.format(home)
    age_file = ('attempt1millenniumIIsnap67_500_fof.txt', 'attempt1millenniumIIsnap67_500_sub.txt')
    agekeys = [['form_gao', 'form_jp', 'assem_gao', 'assem_jp'], ['form_gao', 'form_jp', 'assem_gao', 'assem_jp']]
    labls = [['FOF-Form. Age-Root', 'FOF-Form. Age-Max', 'FOF-Assem. Age-Root', 'FOF-Assem. Age-Max'], \
             ['Sub-Form. Age-Root', 'Sub-Form. Age-Max', 'Sub-Assem. Age-Root', 'Sub-Assem. Age-Max']]
    lines = [['solid', 'dashed', 'solid', 'dashed'], ['solid', 'dashed', 'solid', 'dashed']]
    colrs = [['k', 'k', 'r', 'r'], ['k', 'k', 'r', 'r']]
    halos = (read_halo_table_ascii('{0}{1}'.format(direc, age_file[0]), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29'), \
             read_halo_table_ascii('{0}{1}'.format(direc, age_file[1]), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,27,25,28,26,29'))
    print 'File read...Ploting...'
    xlimits = [0, 14]
    ylimits = [0, 30000]
    plt.figure(1)
    for j in range(2):
        ##Plotting individual panels
        plt.subplot(120 + j + 1)
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        for (i, a) in enumerate(agekeys[j]):
            ages = np.array(get_col_halo_table(halos[j], a))
            if a == 'merg':
                plt.hist(ages[np.where(ages <= 13.5)], bins = 1000, color = colrs[j][i], label = labls[j][i], histtype = 'step', \
                         linewidth = 2, linestyle = lines[j][i])
            else:
                plt.hist(ages, bins = 80, color = colrs[j][i], label = labls[j][i], histtype = 'step', linewidth = 2, linestyle = lines[j][i])
        plt.legend(loc = 2)
        plt.xlabel('Age (Gyrs)')
        plt.ylabel('Number of halos')
    plt.show()
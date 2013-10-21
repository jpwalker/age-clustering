#Age Histogram
from MillenniumII import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    direc = '/Users/jpwalker/Desktop/age-clustering-data/z0_attempt1_form_jp/'
    age_file = 'millenniumIIsnap67age_attempt1057fof_2.txt'
    agekeys = ['form_gao', 'form_jp', 'assem_gao', 'assem_jp', 'merg']
    lines = ['solid', 'dashed', 'solid', 'dashed', 'solid']
    colrs = ['k', 'k', 'r', 'r', 'b']
    halos = read_halo_table_ascii('{0}{1}'.format(direc, age_file), \
                                  fmt = 'x,x,x,x,x,x,x,x,x,x,x,x,x,17,x,21,22,23,24,26,28,25,27,29')
    print 'File read...Ploting...'
    for (i, a) in enumerate(agekeys):
        ages = get_col_halo_table(halos, a)
        plt.hist(ages, bins = 80, color = colrs[i], label = a, histtype = 'step', linewidth = 2, linestyle = lines[i])
    plt.legend(loc = 2)
    plt.xlabel('Age (Gyrs)')
    plt.ylabel('Number of halos')
    plt.vlines(13.55848, 0, 100000, 'b', linewidth = 3)
    plt.show()
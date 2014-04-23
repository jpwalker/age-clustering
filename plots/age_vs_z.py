'''
Created on Apr 22, 2014

@author: jpwalker
'''

from os import environ

if __name__ == '__main__':
    home = '{0}/'.format(environ['HOME'])
    dir = 'Desktop/age-clustering-data/'
    redshifts = ((22, 27, 36, 45, 67), (6.196857, 4.179475, 2.0700316, 0.98870987, 0))
    for i in range(len(redshifts[0])):
        final_dir()
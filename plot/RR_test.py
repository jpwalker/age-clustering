import numpy as np
import math as mth
import matplotlib.pyplot as plt
import random as rnd
from IO import *
from MillenniumII import *
from subprocess import check_output

def radii2(x, y, z, side):
	rad = []
	for i in range(len(x) - 1):
		for j in range(i + 1, len(x)):
			dx = min([(x[i] - x[j])**2., (x[i] - x[j] - side)**2., (x[i] - x[j] + side)**2.])
			dy = min([(y[i] - y[j])**2., (y[i] - y[j] - side)**2., (y[i] - y[j] + side)**2.])
			dz = min([(z[i] - z[j])**2., (z[i] - z[j] - side)**2., (z[i] - z[j] + side)**2.])
			rad.append(mth.sqrt(dx + dy + dz))
	return rad

def radii(x, y, z):
	rad = []
	for i in range(len(x) - 1):
		for j in range(i + 1, len(x)):
			rad.append(mth.sqrt((x[i] - x[j])**2. + (y[i] - y[j])**2. + (z[i] - z[j])**2.))
	return rad

if __name__ == "__main__":
	side = 100.
	rmin = 0
	rmax = 174
	rstep = 0.5
	nbins = (rmax - rmin) / rstep
	rnd.seed()
	x = []
	y = []
	z = []
	N = 5000
	norm = (float(N) * (float(N) - 1.)) / 2.
	tbl = create_halo_table()
	for i in range(N):
		x.append(rnd.uniform(side,0))
		y.append(rnd.uniform(side,0))
		z.append(rnd.uniform(side,0))
		halo_table_append(tbl, create_halo(0, 0, 0, 0, 0, 0, 0, x[-1], y[-1], z[-1], 0, 0, 0, 0, 0, \
										0, 0, 0, 0, 0, 0, 0, 0, 0))
	write_halo_table_ascii('halo_test.txt', tbl, \
                                   fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
	check_output(['2pt-autocorrelation', 'halo_test.txt', 'xi_halo_test.txt'])
	##Non Periodic Boundaries
# 	rad = np.array(radii(x, y, z))
# 	rad = rad[np.where(rad < rmax)]
# 	bins = np.linspace(rmin, rmax, nbins + 1)
# 	bin_centers = np.linspace(rmin + rstep / 2., rmax - rstep / 2., nbins)
# 	counts = np.zeros(nbins)
# 	temp = np.digitize(rad, bins)
# 	for i in temp:
# 		counts[i - 1] += 1
# 	plt.plot(bin_centers, counts / norm, label = 'None-periodic BC')
# 	
# 	##Periodic Boundary Conditions
#   	rad = np.array(radii2(x, y, z, side))
#   	rad = rad[np.where(rad < rmax)]
#   	bins = np.linspace(rmin, rmax, nbins + 1)
#   	bin_centers = np.linspace(rmin + rstep / 2., rmax - rstep / 2., nbins)
#   	counts = np.zeros(nbins)
#   	temp = np.digitize(rad, bins)
#   	for i in temp:
#   		counts[i - 1] += 1
#   	plt.plot(bin_centers, counts / norm, label = 'Periodic BC')
	
	direc = ''
	infile = 'halo_test.txt'
	f = '{0}xi_{1}'.format(direc, infile)
	file_data = readfile(f, 3, ',', 2)
	plt.plot(file_data[0], file_data[2], '+', label = 'RR')
	plt.plot(file_data[0], (file_data[1] + 1.) * file_data[2], label = 'DD')
	plt.plot(file_data[0], 4 * np.pi * file_data[0] ** 2. * 0.5 / side ** 3., label = '4pir^2dr/box^3')
	plt.legend()
	plt.show()

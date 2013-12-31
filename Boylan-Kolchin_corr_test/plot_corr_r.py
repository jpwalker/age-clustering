##Plot the 2-pt autocorrelation function from Boylan-Kolchin
import os
import IO
import matplotlib.pyplot as plt

if __name__ == '__main__':
	cwd = '{0}/'.format(os.getcwd())
	correlation_location = 'correlations/'
	files = ['xi_m_m.txt', 'correl_067_millen.txt', 'correl_067_mini.txt', 'correl_067.txt']
	for i in files:
		if i != 'xi_m_m.txt':
		#0 element has r (Mpc/h); 1 element is xi This is only true for Boylan-Kolchin files
			data_i = IO.readfile('{0}{1}{2}'.format(cwd, correlation_location, i), 4, ' ', 2)
			symbol = ''
		else:
			data_i = IO.readfile('{0}{1}{2}'.format(cwd, correlation_location, i), 2, ' ')
			symbol = '*'
		plt.plot(data_i[0], data_i[1], symbol, label = i)
	plt.xlabel('r (Mpc / h)')
	plt.ylabel('xi(r)')
	plt.xlim([0., 25.])
	plt.ylim([0., 10.])
	plt.legend()
	plt.show()
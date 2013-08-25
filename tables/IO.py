'''
Created on Jun 17, 2013

@author: jpwalker
'''
import numpy as np

def readfile(filename, col = 2, delim = ' ', skip = -1):
    #Read in P(k)
    f = open(filename, 'r')
    data = f.read()
    data = data.splitlines()
    #Setup P
    P = []
    for i in range(col): 
        P.append([])
    line_count = 0
    for i in data:
        if line_count >= skip:
            q = 0
            for j in i.split(delim):
                if j != '':
                    try:
                        P[q].append(float(j))
                    except:
                        P[q].append(j)
                    q += 1
        line_count += 1
    for (i, j) in enumerate(P):
        P[i] = np.array(j)
    return P

def writefile(filename, np_array, delim = ' ', note = ''):
    shp = np_array.shape
    f = open(filename, 'w')
    f.write('{0}\n'.format(note))
    if len(shp) == 2:
        for i in range(shp[1]):
            temp = []
            for j in range(shp[0]):
                temp.append(str(np_array[j][i]))
            f.write('{0}\n'.format(delim.join(temp)))            
    f.close()
    
if __name__ == '__main__':
    x = [0,5]
    y = [0, 25]
    a = np.array([x,y])
    writefile('test', a)
    b = readfile('test', col = 2, delim = ' ')
    print a 
    print b[0], b[1]
    
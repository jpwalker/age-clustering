'''
Created on Jan 26, 2016

@author: jpwalker
'''

from cProfile import run

# Tests to see if extend is faster than append
if __name__ == '__main__':
    x = []
    data = range(10000000)
    print(run("a = x.extend(data)"))
    a = []
    print(run("for i in data: a.append(i)"))
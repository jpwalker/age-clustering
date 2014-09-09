#! /usr/bin/env python
'''
Created on Jul 16, 2014

@author: jpwalker
Code will connect to a local MySQL server and retrieve queries submitted to it.
'''

import mysql.connector as con
import MillenniumII as ms

def output_halotable(results):
    output_table = ms.create_halo_table()
    for i in results:
        halo = ms.create_halo(i[0], i[1], i[2], i[3], i[4], i[5], i[6], \
                              i[7], i[8], i[9], i[10], i[11], i[12], i[13], \
                              i[14], i[15], i[16], i[17], i[18], i[19])
        ms.halo_table_append(output_table, halo)
    return output_table

def submit_query(query, db = 'millenniumii', user = 'jpwalker'):
    c = con.connect(unix_socket = '/tmp/mysql.sock', user = user, database = db)
    cu = c.cursor()
    cu.execute(query)
    res = cu.fetchall()
    return res

def get_merger_tree(halo, last = None, snaps = None):
    selects = 'haloid, subhaloid, treeid, descendantid, lastprogenitorid, \
    snapnum, sub_np, x, y, z, halfmassradius, vdisp, \
    vmax, vmaxrad, fofid, firstsubhaloid, fof_np, m200, r200, nsubs'
    if last == None:
        query = 'select lastprogenitorid from master where haloid = {0};'
        query.format(halo)
        res = submit_query(query)
        if len(res) != 0:
            last = res[0][0]
        else:
            raise('Haloid not found!')
    if snaps != None:
        res = []
        for i in snaps:
            query = 'select {0} from snap{1} where haloid between {2} and {3};'
            query.format(selects ,i, halo, last)
            res.extend(submit_query(query))
    else:
        query = 'select {0} from master where haloid between {1} and {2}'
        query.format(selects, halo, last)
        res = submit_query(query)
    res = output_halotable(res)
    return res

if __name__ == '__main__':
    get_merger_tree(16)
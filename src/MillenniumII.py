'''
Created on Mar 24, 2013

@author: jpwalker
'''

import collections
halo = collections.namedtuple('halo', ['haloid', 'subhaloid', 'treeid', 'descendantid', 'lastprogenitorid', \
                                       'snapnum', 'sub_np', 'x', 'y', 'z', 'firsthaloinfofgroupid', 'radii', \
                                       'vdisp', 'vmax', 'vmaxrad', 'fofid', 'firstsubhaloid', 'fof_np', 'm200', \
                                       'r200', 'nsubs', 'max_tree_mass', 'max_tree_mass_snap', 'min_mass_root_max', \
                                       'min_mass_root_max_snap', 'form_gao', 'assem_gao', 'form_jp', 'assem_jp', 'merg'])
keys = {'haloid': 0, 'subhaloid': 1, 'treeid': 2, 'descendantid': 3, 'lastprogenitorid': 4, 'snapnum': 5, \
        'sub_np': 6, 'x': 7, 'y': 8, 'z': 9, 'firsthaloinfofgroupid': 10, 'radii': 11, 'vdisp': 12, \
        'vmax': 13, 'vmaxrad': 14, 'fofid': 15, 'firstsubhaloid': 16, 'fof_np': 17, 'm200': 18, \
        'r200': 19, 'nsubs': 20, 'max_tree_mass': 21, 'max_tree_mass_snap': 22, 'min_mass_root_max': 23, \
        'min_mass_root_max_snap': 24, 'form_gao': 25, 'assem_gao': 26, 'form_jp': 27, 'assem_jp': 28, 'merg': 29}
keys_rev = {0: 'haloid', 1: 'subhaloid', 2: 'treeid', 3: 'descendantid', 4: 'lastprogenitorid', 5: 'snapnum', \
        6: 'sub_np', 7: 'x', 8: 'y', 9: 'z', 10: 'firsthaloinfofgroupid', 11: 'radii', 12: 'vdisp', \
        13: 'vmax', 14: 'vmaxrad', 15: 'fofid', 16: 'firstsubhaloid', 17: 'fof_np', 18: 'm200', \
        19: 'r200', 20: 'nsubs', 21: 'max_tree_mass', 22: 'max_tree_mass_snap', 23: 'min_mass_root_max', \
        24: 'min_mass_root_max_snap', 25: 'form_gao', 26: 'assem_gao', 27: 'form_jp', 28: 'assem_jp', 29: 'merg'}

def create_halo(haloid, sub, tree, desc, last, snap, s_np, x, y, z, firsthalo, radii, vdisp, \
                vmax, vmaxrad, fof, firstsub, f_np, m200, r200, nsubs, max_tree_mass, max_tree_mass_snap, \
                min_mass_root_max, min_mass_root_max_snap, form_gao, assem_gao, form_jp, assem_jp, merg):
    haloid = int(haloid)
    sub = int(sub)
    tree = int(tree)
    desc = int(desc)
    last = int(last)
    snap = int(snap)
    s_np = int(s_np)
    x = float(x)
    y = float(y)
    z = float(z)
    firsthalo = int(firsthalo)
    radii = float(radii)
    vdisp = float(vdisp)
    vmax = float(vmax)
    vmaxrad = float(vmaxrad)
    fof = int(fof)
    firstsub = int(firstsub)
    f_np = int(f_np)
    m200 = float(m200)
    r200 = float(r200)
    nsubs = int(nsubs)
    max_tree_mass = int(max_tree_mass)
    max_tree_mass_snap = int(max_tree_mass_snap)
    min_mass_root_max = int(min_mass_root_max)
    min_mass_root_max_snap = int(min_mass_root_max_snap)
    form_gao = float(form_gao)
    assem_gao = float(assem_gao)
    form_jp = float(form_jp)
    assem_jp = float(assem_jp)
    merg = float(merg)
    a = halo(haloid, sub, tree, desc, last, snap, s_np, x, y, z, firsthalo, radii, vdisp, vmax, \
             vmaxrad, fof, firstsub, f_np, m200, r200, nsubs, max_tree_mass, max_tree_mass_snap, \
                min_mass_root_max, min_mass_root_max_snap, form_gao, assem_gao, form_jp, assem_jp, merg)
    return a
    
def create_halo_table():
    return dict(data = [], length = 0)

def halo_table_append(table, h):
    try:
        if isinstance(h, halo):
            table['data'].append(h)
            table['length'] += 1
        else:
            print('Argument given not of type halo.')
    except KeyError:
        print('Error key not found')

def halo_table_insert(table, h, pos):
    try:
        if table.length - 1 >= pos:
            if isinstance(halo,halo):
                table.data[pos] = halo
            else:
                print('Argument given not of type halo.')
        else:
            print('Error position index not found.')
    except KeyError:
        print('Error key not found.')
    
def get_col_halo_table(table, key):
    """
    Returns a list containing the values from halo_table with keyword key.
    """
    
    try:
        idx = keys[key]
    except KeyError:
        print('Error key not found')
    col = []
    for i in table['data']: col.append(i[idx])
    return col

def select_halo_table(table, select_key):
    new_halo_table = create_halo_table()
    for i in select_key:
        halo_table_append(new_halo_table, table['data'][i])
    return new_halo_table

def sort_halo_table(table, sortkey):
    """
    Returns a list containing the values in halo_table sorted by sortkey.
    """
    col = get_col_halo_table(table, sortkey)
    sortorder = [i for i in sorted(range(len(col)), key = lambda x:col[x])]
    new_halo_table = create_halo_table()
    for i in sortorder:
        try:
            halo_table_append(new_halo_table, table['data'][i])
        except KeyError:
            print('Error key not found.')
    return new_halo_table

def parse_fmt(fmt):
    #Processing fmt string
    fmt = fmt.split(',')
    #Test to see of all numbers were in string
    num_total_col = len(fmt)
    empty_col_num = fmt.count('x')
    test = [0] * 24
    for i in range(24): test[i] = fmt.count(str(i))
    if num_total_col != empty_col_num + sum(test):
        raise ValueError('Error check fmt string.')
    return fmt

def cast(d, type):
    try:
        if type == 0 or type == 1 or type == 2 or type == 3 or type == 4 or type == 5  or type == 6 or \
        type == 10 or type == 15 or type == 16 or type == 17 or type == 20:
            return int(d)
        else:
            return float(d)
    except ValueError:
        print('Unable to cast {0}'.format(d))

def read_halo_table_ascii(filename, fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29'):
    h_tab = create_halo_table()
    counter = 0
    line = 0
    #Process fmt format string
    fmt = parse_fmt(fmt)
    lfmt = len(fmt)
    rfmt = range(lfmt)
    #Open File
    f = open(filename, 'r')
    test = True
    #Create new parameters variable for use later
    parameters = list(0 for i in range(30))
    while test:
        data = f.readline()
        if data != '':
            counter += 1
            line += 1
            #Split data by comma delimited columns
            data = data.split(',')
            data[-1] = (data[-1])[:-1] #Remove return character at end of string
            if len(data) != len(fmt):
                print('Line {0} doesn\'t match format string.'.format(line))
                counter -= 1
            else:
                try:
                    for i in rfmt:
                        if fmt[i] != 'x':
                            t_fmt = int(fmt[i])
                            parameters[t_fmt] = cast(data[i],t_fmt)
                except:
                    print('Unable to convert Line {0}, property {1}.'.format(line, keys_rev[t_fmt]))
                    counter -= 1
                halo_table_append(h_tab, create_halo(parameters[0], parameters[1], parameters[2], parameters[3], \
                                                     parameters[4], parameters[5], parameters[6], parameters[7], \
                                                     parameters[8], parameters[9], parameters[10], parameters[11], \
                                                     parameters[12], parameters[13], parameters[14], parameters[15], \
                                                     parameters[16], parameters[17], parameters[18], parameters[19], \
                                                     parameters[20], parameters[21], parameters[22], parameters[23], \
                                                     parameters[24], parameters[25], parameters[26], parameters[27], \
                                                     parameters[28], parameters[29]))
        else: test = not test
    f.close()
    print('{0} valid lines read out of {1} lines.'.format(counter, line))
    #for i in data: print(i)
    return h_tab

def header(f, fmt):
    out = []
    for i in fmt:
        out.append(keys_rev[int(i)])
    out = '{0}\n'.format(', '.join(out))
    f.writelines(out)

def write_halo_table_ascii(filename, table, fmt = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29'):
    fmt = parse_fmt(fmt)
    output = []
    delim = ', '
    try:
        f = open(filename, 'w+')
        header(f, fmt)
        for i in table['data']:
            temp = []
            for j in fmt:
                if j != 'x':
                    temp.append(str(i[int(j)]))
            output.append('{0}\n'.format(delim.join(temp)))
        print 'Writing to file...'
        f.writelines(output)
        print 'File Saved!!!'
        f.close()    
    except IOError:
        print 'Error opening/writing to file'

if __name__ == '__main__':
    import cProfile
    #cProfile.run('a = read_halo_table_ascii("/Volumes/DATA/Millennium Data/MillenniumII/snap15.txt", "0,1,2,3,4,5,6,7,8,9,x,x,x,x,x,15,16,17,x,x,20")')
    a = read_halo_table_ascii("/Volumes/DATA/Millennium Data/MillenniumII/snap5.txt", "0,1,2,3,4,5,6,7,8,9,x,x,x,x,x,15,16,17,x,x,20")
    write_halo_table_ascii("/Users/jpwalker/Desktop/positions.txt", a, "7,8,9")
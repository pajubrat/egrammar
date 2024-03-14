def print_lst(lst):
    str = ''
    for i, ps in enumerate(lst):
        if ps.terminal():
            str += f'{ps}°'
        else:
            str += f'{ps}'
        if i < len(lst) - 1:
            str += ', '
    return str

def print_constituent_lst(sWM):
    aWM = [x for x in sWM if not x.mother()]
    iWM = [x for x in sWM if x.mother()]
    str = f'{print_lst(aWM)}'
    if iWM:
        str += f' + {{ {print_lst(iWM)} }}'
    return str

def print_dictionary(sem):
    str = ''
    for key in sem.keys():
        if sem[key]:
            str += key + ': '
            for value in sem[key]:
                if value:
                    str += f'{value}, '
    return str[:-2]

def get_root(sWM):
    for X in sWM:
        if X.isRoot():
            return X

def tcopy(SO):
    return tuple(x.copy() for x in SO)

def tset(X):
    if isinstance(X, set):
        return X
    else:
        return {X}

def comment(line):
    return line.startswith('#')

def well_formed_lexical_entry(line):
    return '::' in line

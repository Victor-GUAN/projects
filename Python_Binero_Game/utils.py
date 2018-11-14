#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a package of utils to manipulate DIMACS file and Binero file, 
such as:
    - represent them with pure python and z3.
    - write clauses to the file in format DIMACS.
    - etc.

Creating time :    13/5/2018
Author        :    Jue WANG, Minghui GUAN
'''

from z3 import *

def parseDIMACS(filename):
    '''
    Parse DIMACS file
    temporarily only support cnf description

    Args:
        filename : the path of file in format DIMACS.

    Returns:
        form : the type of clauses
        num_vars : the number of variables
        num_clauses : the number of clauses
        clauses : the clauses in 2d array
    '''

    form = None
    num_vars, num_clauses = 0, 0
    clauses = []

    for line in open(filename, 'r'):
        tokens = line.strip().split()

        # Distinguish the instruction
        if len(tokens) == 0:
            continue
        elif tokens[0] == 'c':
            continue
        elif tokens[0] == 'p':
            form = tokens[1]
            num_vars, num_clauses = int(tokens[2]), int(tokens[3])
            continue

        if form == 'cnf' and len(clauses) < num_clauses:
            clauses.append([])
            for tk in tokens:
                c = int(tk)
                if c == 0:
                    break
                assert(abs(c) <= num_vars)
                clauses[-1].append(c)

    return form, num_vars, num_clauses, clauses


def writeCnf(num_vars, clauses, filepath='clauses.txt', description=None):
    '''
    write cnf constraints to a file in DIMACS format.

    Args:
        num_vars : (int) the number of variables
        clauses : (list) a list of clauses.
        filepath : (str) the path of file to write to.
        description : (str) the comments int the output file

    Returns:
        None
    '''
    output = open(filepath, 'w')

    output.write('c\n')
    output.write('c {}\n'.format(filepath))
    if description is not None:
        output.write('c {}\n'.format(description))
    output.write('c\n')

    output.write('p cnf {} {}\n'.format(num_vars, len(clauses)))
    for c in clauses:
        output.write(' '.join([str(i) for i in c]) + ' 0\n')

    output.close()


def cnf2z3(X, clauses):
    '''
    Convert cnf clauses to z3 supported ones.

    Args:
        X : two possibilities :
            1. (int) the number of vars, the program will automatically create the vars
            2. (list[z3vars]) a list of z3 vars, which are vars in clauses.
        clauses : a 2d list of clauses in cnf format.

    Returns:
        a z3 clause
    '''
    if isinstance(X, int):
        X = [Bool('x{}'.format(i)) for i in range(1, X+1)]
    elif isinstance(X, list):
        pass
    else:
        raise Exception('X abnormal type.')

    z3clauses = []
    for clause in clauses:
        z3clauses.append(Or([X[abs(i)-1] == (i > 0) for i in clause]))

    return z3clauses


def readGrid(filename):
    '''
    Parse Grid file

    Args:
        filename : the path of file in format Binero.

    Returns:
        grid : a 2d list containing a grid of binero, the elements are strings 
                where '1' stands for 1,
                      '0' stands for 0,
                      '.' will be determined whether 0 or 1.
    '''
    grid = []
    sizeI, sizeJ = 0, 0

    for line in open(filename, 'r'):
        tokens = line.strip().split()

        # Distinguish the instruction
        if len(tokens) == 0:
            continue
        elif tokens[0] == 'c':
            continue
        elif tokens[0] == 'binero' or tokens[0] == 'grid':
            sizeI, sizeJ = int(tokens[1]), int(tokens[2])
            continue

        # Read data.
        if len(grid) < sizeI:
            assert(len(tokens) == sizeJ)
            grid.append(tokens)
        else:
            break

    return grid

def writeSolution(grid, filepath='example_binero_answer.txt', description=None):
    '''
    write a solution to a file in its format (for example Binero format).
    Args:
        grid : (Grid) a grid object
        filepath : (str) the path of file to write to.
        description : (str) the comments int the output file

    Returns:
        None
    '''
    with open(filepath, 'w') as f:
        f.write('c\n')
        f.write('c {}\n'.format(filepath))
        if description is not None:
            f.write('c {}\n'.format(description))
        f.write('c\n')
        f.write('{} {} {}\n'.format(grid.type, grid.size, grid.size))
        f.write(grid.getSolution())
        
def writeGrid(grid, filepath='example_new_binero.txt', description=None):
    '''
    write the grid to a file in its format (for example Binero format).
    Args:
        grid : (Grid) a grid object
        filepath : (str) the path of file to write to.
        description : (str) the comments int the output file

    Returns:
        None
    '''
    with open(filepath, 'w') as f:
        f.write('c\n')
        f.write('c {}\n'.format(filepath))
        if description is not None:
            f.write('c {}\n'.format(description))
        f.write('c\n')
        f.write('{} {} {}\n'.format(grid.type, grid.size, grid.size))
        f.write(grid.getGrid())


def solverCnf(filename, X=None):
    '''
    This is a small example to solve a problem defined in format DIMACS.
    '''
    form, size_var, _, clauses = parseDIMACS(filename)
    if X is None:
        X = [Bool('x{}'.format(i)) for i in range(1, size_var+1)]

    assert(form == 'cnf')

    s = Solver()
    s.add(cnf2z3(X, clauses))

    return s, X

if __name__ == '__main__' :
    print('--test1--')

    for l in readGrid('example_binero.txt'):
        print(' '.join(l))

    print('--test2--')

    s, X = solverCnf('example_dimacs.txt')
    if s.check() == sat:
        print('s SATISFIABLE')

        m = s.model()
        print(m)
        print('v ', end='')
        for i in range(len(X)):
            if m[X[i]] is not None and is_false(m[X[i]]):
                print(-i-1, end=' ')
            else:
                print(i+1, end=' ')
        print('0')
        
    else:
        print('s UNSATISFIABLE')

    print('--test3--')

    _, num_vars, _, clauses = parseDIMACS('example_dimacs.txt')
    writeCnf(num_vars, clauses, 'clauses.txt')

    for l in open('clauses.txt', 'r'):
        print(l, end='')

    

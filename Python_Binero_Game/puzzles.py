#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file contains several classes to describe puzzles 
such as Binero puzzle.

Creating time :    13/5/2018
Author        :    Jue WANG, Minghui GUAN
'''

from time import time
from numpy.random import randint
from z3 import *
from utils import parseDIMACS, cnf2z3, readGrid, writeGrid
from rules import ClauseMaker, generateFirstConstraint, generateSecondConstraint, generateThirdConstraint 

class Grid:
    '''
    Grid class represent a n*n grid where each node is a bool variable.
    Its rules should be defined in DIMACS format and manually read them.
    '''
    def __init__(self):
        self.type = 'grid'
        self.solver = Solver()
        self.X = []
        self.T = []

    def readGrid(self, filename):
        self.grid = readGrid(filename)
        self.size = len(self.grid)
        self.X = []

        clauses_of_grid = []
        for i in range(self.size):
            for j in range(self.size):
                x = Bool('x{}_{}'.format(i+1,j+1))
                self.X.append(x)
                if self.grid[i][j] != '.':
                    clauses_of_grid.append(x == (self.grid[i][j]=='1'))

        self.solver.add(clauses_of_grid)

    def readDIMACS(self, dimacs_files):
        '''
        dimacs_files : a list of paths of the files which describe the rules of the grid
        '''
        for df in dimacs_files:

            form, num_vars, num_clauses, clauses = parseDIMACS(df)
            assert form == 'cnf'
    
            if num_vars > len(self.X) + len(self.T):
                self.T += [Bool('t{}'.format(i)) for i in range(len(self.T)+1, len(self.T)+1+num_vars-len(self.X))]
    
            self.solver.add(cnf2z3(self.X + self.T, clauses))

    def check(self, print_result=True):
        '''
        print('s UNSATISFIABLE')
        si la formule est insatisfiable, et de la forme suivante
        s SATISFIABLE
        print('v 1 2 -3 4 5 0')
        si la formule est satisfiable.
        '''
        if self.solver.check() == sat:
            if print_result:
                tmp = ['v']
                m = self.solver.model()
    
                for i in range(len(self.X)):
                    if m[self.X[i]]:
                        tmp.append(str(i+1))
                    else:
                        tmp.append(str(-i-1))
    
                for i in range(len(self.T)):
                    if m[self.T[i]]:
                        tmp.append(str(len(self.X)+i+1))
                    else:
                        tmp.append(str(-len(self.X)-i-1))
    
                tmp.append('0')
                print(' '.join(tmp))
            return True
        else:
            print('s UNSATISFIABLE')
            return False
            

    def getx(self, i, j):
        '''
        get z3 variable at i-th row and j-th column.
        '''
        return self.X[i*self.size+j]
    
    def getGrid(self):
        grid = ''
        for l in self.grid:
            grid += ' '.join(l) + '\n'
        return grid

    def printGrid(self):
        '''
        print the original grid.
        '''
        for l in self.grid:
            print(' '.join(l))

    def getSolution(self):
        '''
        get the solution in str.
        Returns:
            solution : (str) such as:
                0 0 1 1 0 0 1 1
                0 1 0 1 0 1 0 1
                1 1 0 0 1 0 1 0
                1 0 1 1 0 1 0 0
                0 1 0 0 1 0 1 1
                1 0 0 1 1 0 0 1
                0 1 1 0 0 1 1 0
                1 0 1 0 1 1 0 0
        '''

        m = self.solver.model()

        solution = []
        buf = []

        for x in self.X:
            if m[x] is None:
                buf.append('1')
            else:
                buf.append(str(is_true(m[x])+0))

            if len(buf) == self.size:
                solution.append(' '.join(buf))
                buf = []

        return '\n'.join(solution)

    def printSolution(self):
        print(self.getSolution())


class Binero(Grid):
    '''
    Bienro class extends Grid.
    After read the grid, it will automatically generate the constraints 
    of binero in DIMACS and read them.
    '''
    def __init__(self):
        super(Binero, self).__init__()
        self.type = 'binero'

    def readGrid(self, filename):
        super().readGrid(filename)

        size = self.size
        dimacs_files=['binero_first_constraint.txt',
                      'binero_second_constraint.txt',
                      'binero_third_constraint.txt',]

        cm = ClauseMaker(size*size)
        generateFirstConstraint(size, filepath=dimacs_files[0], cm=cm)
        generateSecondConstraint(size, filepath=dimacs_files[1], cm=cm)
        generateThirdConstraint(size, filepath=dimacs_files[2], cm=cm)

        self.readDIMACS(dimacs_files)
        

def generateBineroGrid(size, minRatio=40, filepath='example_new_binero.txt', description='un petit exemple'):
    '''
    this function generate a binero grid according to the size.
    As check() in z3 is much quicker than loading constraints, 
    we can check the correction and each try. 
    Thus, the algorithm principally runs as:
    
    load constraints.
    while not stop_condition:
        randomly fill a position with 0 or 1
        if sat:
            continue
        else:
            roll back

    Args:
        size : (int) the size of generated grid
        minRatio : (int) the expected minimum percentage of grid being blank
        filepath : (str) the path of the generated grid in Binero format
        description : (str) the description of the grid

    Returns:
        grid : (2d list) a 2d list representing the generated grid
    '''

    n = size*size
    b = Grid()
    b.type = 'binero'
    b.size = size
    b.X = [Bool('x{}_{}'.format(i+1,j+1)) for i in range(size) for j in range(size)]
    
    # manually generate constraints
    dimacs_files=['binero_first_constraint.txt',
                  'binero_second_constraint.txt',
                  'binero_third_constraint.txt',]
    cm = ClauseMaker(b.size*b.size)
    generateFirstConstraint(b.size, filepath=dimacs_files[0], cm=cm)
    generateSecondConstraint(b.size, filepath=dimacs_files[1], cm=cm)
    generateThirdConstraint(b.size, filepath=dimacs_files[2], cm=cm)
    
    # manually read the DIMACS files
    b.readDIMACS(dimacs_files)
    
    s = b.solver
    s.push()
    X = b.X.copy()
    
    n = size*size
    max_steps = n*2
    b.grid = [['.' for j in range(size)] for i in range(size)]
    
    while n > size*size*minRatio/100 and max_steps > 0:
        max_steps -= 1
        i = randint(n)
        randi = randint(2)
        s.push()
        s.add(X[i] == bool(randi))
        if s.check() == sat:
            xi, xj = str(X[i])[1:].split('_')
            b.grid[int(xi)-1][int(xj)-1] = str(randi)
            n -= 1
            X.pop(i)
        else:
            s.pop()
    
    with open(filepath, 'w') as f:
        f.write('c\n')
        f.write('c {}\n'.format(description))
        f.write('c\n')
        f.write('binero {} {}\n'.format(size, size))
        for l in b.grid:
            f.write(' '.join([str(i) for i in l]) + '\n')

    return b.grid


if __name__ == '__main__':
    print('---test1---')
    g = Grid()
    g.readGrid('example_binero.txt')
    print(g.solver.check())
    g.printSolution()

    print('---test2---')
    b = Binero()
    b.readGrid('example_binero.txt')
    if b.check(False):
        b.printSolution()
    writeGrid(b)

    # print('---test3---')
    # sg = Grid()
    # sg.readGrid(filename='example_binero.txt')
    # sg.readDIMACS(dimacs_files=['binero_first_constraint.txt',
    #                             'binero_second_constraint.txt',
    #                             'binero_third_constraint.txt'])
    # print(sg.solver.check())
    # sg.printSolution()


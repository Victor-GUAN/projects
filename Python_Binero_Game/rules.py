#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
This file is used to create a binero model with its constraints:
    - The no three consecutive constraint;
    - The balancedness constraint;
    - The no repeated vector constraint.

Creating time :    14/5/2018
Author        :    Jue WANG, Minghui GUAN
'''

from math import log
from z3 import *
from utils import writeCnf

class ClauseMaker:
    def __init__(self, num_x):
        self.C = num_x

    def _treat(self, A, clauses):
        '''
        this is tricky, the purpose is to make nesting methods possible.
        since the returns of each expression are not only the index of 
        the extra variable, but also the inherited clauses. Thus,
        we need to recognize them and extend the clauses and only 
        return the index.
        '''
        if isinstance(A, tuple):
            clauses.extend(A[1])
            return A[0]
        else:
            return A

    def _pretreat(self, A, B):
        clauses = []
        A = self._treat(A, clauses)
        B = self._treat(B, clauses)
        self.C += 1
        return A, B, clauses

    def And(self, A, B):
        A, B, clauses = self._pretreat(A, B)
        clauses.append([-A, -B, self.C])
        clauses.append([A, -self.C])
        clauses.append([B, -self.C])
        return self.C, clauses

    def Nand(self, A, B):
        A, B, clauses = self._pretreat(A, B)
        clauses.append([-A, -B, -self.C])
        clauses.append([A, self.C])
        clauses.append([B, self.C])
        return self.C, clauses

    def Or(self, A, B):
        A, B, clauses = self._pretreat(A, B)
        clauses.append([A, B, -self.C])
        clauses.append([-A, self.C])
        clauses.append([-B, self.C])
        return self.C, clauses

    def Nor(self, A, B):
        A, B, clauses = self._pretreat(A, B)
        clauses.append([A, B, self.C])
        clauses.append([-A, -self.C])
        clauses.append([-B, -self.C])
        return self.C, clauses

    def Not(self, A):
        A, _, clauses = self._pretreat(A, 0)
        clauses.append([-A, -self.C])
        clauses.append([A, self.C])
        return self.C, clauses

    def Xor(self, A, B):
        A, B, clauses = self._pretreat(A, B)
        clauses.append([-A, -B, -self.C])
        clauses.append([A, B, -self.C])
        clauses.append([A, -B, self.C])
        clauses.append([-A, B, self.C])
        return self.C, clauses

    def New(self):
        self.C += 1
        return self.C


def pos2idx(i, j, size, begin_with=1):
    '''
    This convert a position to the index of it
    the index begin with 1 by default.
    '''
    return i*size + j + begin_with


def generateFirstConstraint(size, filepath='binero_first_constraint.txt', cm=None):
    clauses = []
    for i in range(size):
        for j in range(size):
            if i != 0 and i != size-1:
                clauses.append([pos2idx(i-1,j,size),pos2idx(i,j,size),pos2idx(i+1,j,size)])
                clauses.append([-pos2idx(i-1,j,size),-pos2idx(i,j,size),-pos2idx(i+1,j,size)])
            if j != 0 and j != size-1:
                clauses.append([pos2idx(i,j-1,size),pos2idx(i,j,size),pos2idx(i,j+1,size)])
                clauses.append([-pos2idx(i,j-1,size),-pos2idx(i,j,size),-pos2idx(i,j+1,size)])

    writeCnf(size*size, clauses, filepath)

    return clauses


def generateSecondConstraint(size, filepath='binero_second_constraint.txt', cm=None):
    clauses = []
    if cm is None:
        cm = ClauseMaker(size*size)

    # target is a 2-ary representation of size/2
    num_d = int(log(size,2)) + 1
    target = [0 for i in range(num_d)]
    int_target = size//2
    for i in range(num_d):
        target[i] = int_target%2
        int_target //= 2

    # row
    for i in range(size):
        # init a and t
        a = [cm.New() for ii in range(num_d)]
        t = [cm.New() for ii in range(num_d+1)]
        clauses.extend([[-ai] for ai in a])
        clauses.extend([[-ti] for ti in t])

        for j in range(size):
            x = pos2idx(i, j, size)

            a0 = a[0]
            a[0], _clauses = cm.Xor(a0, x)
            clauses.extend(_clauses)

            t[1], _clauses = cm.And(a0, x)
            clauses.extend(_clauses)

            for k in range(1, num_d):
                t[k+1], _clauses = cm.And(a[k], t[k])
                clauses.extend(_clauses)
                a[k], _clauses = cm.Xor(a[k], t[k])
                clauses.extend(_clauses)

        for k in range(num_d):
            if target[k] == 1:
                clauses.append([a[k]])
            else:
                clauses.append([-a[k]])

    for j in range(size):
        # init a and t
        a = [cm.New() for ii in range(num_d)]
        t = [cm.New() for ii in range(num_d+1)]
        clauses.extend([[-ai] for ai in a])
        clauses.extend([[-ti] for ti in t])

        for i in range(size):
            x = pos2idx(i, j, size)

            a0 = a[0]
            a[0], _clauses = cm.Xor(a0, x)
            clauses.extend(_clauses)

            t[1], _clauses = cm.And(a0, x)
            clauses.extend(_clauses)

            for k in range(1, num_d):
                t[k+1], _clauses = cm.And(a[k], t[k])
                clauses.extend(_clauses)
                a[k], _clauses = cm.Xor(a[k], t[k])
                clauses.extend(_clauses)

        for k in range(num_d):
            if target[k] == 1:
                clauses.append([a[k]])
            else:
                clauses.append([-a[k]])

    writeCnf(cm.C, clauses, filepath)

    return clauses


def generateThirdConstraint(size, filepath='binero_third_constraint.txt', cm=None):
    clauses = []
    if cm is None:
        cm = ClauseMaker(size*size)

    # row
    for xi in range(size):
        for yi in range(size):
            if xi == yi:
                continue

            for k in range(size):
                xik, yik = pos2idx(xi,k,size), pos2idx(yi,k,size)
                if k == 0:
                    Dk, _clauses = cm.Or(cm.And(xik, yik), cm.And(-xik, -yik))
                else:
                    Dk, _clauses = cm.And(cm.Or(cm.And(xik, yik), cm.And(-xik, -yik)), Dk)
                clauses.extend(_clauses)

            clauses.append([-Dk])



    # col
    for xj in range(size):
        for yj in range(size):
            if xj == yj:
                continue

            for k in range(size):
                xkj, ykj = pos2idx(k,xj,size), pos2idx(k,yj,size)
                if k == 0:
                    Dk, _clauses = cm.Or(cm.And(xkj, ykj), cm.And(-xkj, -ykj))
                else:
                    Dk, _clauses = cm.And(cm.Or(cm.And(xkj, ykj), cm.And(-xkj, -ykj)), Dk)
                clauses.extend(_clauses)

            clauses.append([-Dk])

    writeCnf(cm.C, clauses, filepath)

    return clauses


if __name__ == '__main__':
    size = 8
    cm = ClauseMaker(size*size)
    generateFirstConstraint(size, cm=cm)
    generateSecondConstraint(size, cm=cm)
    generateThirdConstraint(size, cm=cm)
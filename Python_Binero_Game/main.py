
# coding: utf-8

# In[1]:


# get_ipython().run_line_magic('load_ext', 'autoreload')
# get_ipython().run_line_magic('autoreload', '2')


# In[2]:


from z3 import *
from puzzles import Grid, Binero, generateBineroGrid
from utils import writeGrid
from rules import ClauseMaker, generateFirstConstraint
from rules import generateSecondConstraint, generateThirdConstraint


# In[3]:


# test 1 : use Binero class
print('test 1 : use Binero class')

b = Binero()
'''
After reading the grid, it will automatically generate three 
DIMACS files containing the constraints of binero and read 
them into its z3 solver.
'''
b.readGrid('example_binero.txt')
b.check(print_result=False)
print('------Grid------')
b.printGrid()
print('----Solution----')
b.printSolution()
writeGrid(b, filepath='example_binero_answer.txt', description=None)


# In[4]:


# test 2 : use self-defined Grid class
print('test 2 : use self-defined Grid class')

b = Grid()
b.readGrid('example_binero2.txt')

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

b.check(print_result=False)
print('------Grid------')
b.printGrid()
print('----Solution----')
b.printSolution()
writeGrid(b, filepath='example_binero2_answer.txt', description=None)


# In[5]:


# test 3 : generate a binero grid and solve it
print('test 3 : generate a binero grid and solve it')

generateBineroGrid(6, filepath='example_new_binero.txt')

b = Binero()
b.readGrid('example_new_binero.txt')
b.check(print_result=False)
print('------Grid------')
b.printGrid()
print('----Solution----')
b.printSolution()
writeGrid(b, filepath='example_new_binero_answer.txt', description=None)


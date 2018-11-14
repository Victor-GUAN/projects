# Binero

this project depends on Z3 solver.

## Quick start

one command demo in command line:

```Shell
$ python3 main.py
```

Or try it in python:

```python
from puzzles import Binero
from utils import writeGrid

b = Binero()
b.readGrid('example_binero.txt')
b.check(print_result=False)
print('------Grid------')
b.printGrid()
print('----Solution----')
b.printSolution()
writeGrid(b, filepath='example_binero_answer.txt', description=None)
```

## File structure

Source codes:

- main.ipynb : it's a demo runing with jupyter notebook.

  main.py : do the same thing as main.ipynb

- puzzle.py : define puzzle class such as Binero.

- rules.py : it is used to generate the constraints of binero in DIMACS.

- utils.py : the utils used for manipulating data such as reading and writing DIMACS.

Data files:

- example_binero.txt : an example of binero puzzle.
- example_binero2.txt : another example of binero puzzle.
- example_dimacs.txt : it's a example of dimacs to test the functionality of utils.py

Report:

- Rapport.pdf : the report for the project.
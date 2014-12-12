
# need a way to auto-close tkinter dialogs

import subprocess

PYPY='d:/program/pypy/pypy.exe'
PYTHON2='c:/Python27/python.exe'
PYTHON3='c:/Python33/python.exe'

# run with PyPy
subprocess.call( [PYPY, 'winpdb.py'] )

# run with Python 3
subprocess.call( [PYTHON3, 'winpdb.py'] )

# run with Python 2
# subprocess.call( [PYTHON2, 'winpdb.py'] )


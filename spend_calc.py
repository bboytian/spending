#!/usr/bin/python3
'''
python3 /path/to/spend_calc.py filename
'''

# imports
from collections import defaultdict
import os.path as osp
import sys


# reading file
filepath = osp.join(
    osp.dirname(osp.abspath(__file__)),
    sys.argv[1]
)
print(f'reading file from: {filepath}')
with open(filepath, 'r') as textfile:
    contents = textfile.readlines()

cat_d = defaultdict(lambda: 0)

cat = ''
for line in contents:

    if line in ['', ' ', '\n']:
        continue

    else:

        try:
            val = float(line.split(' ')[0])
            cat_d[cat] += val
        except ValueError:
            cat = line.replace('\n', '')

for key, val in cat_d.items():
    print(f'{key}: {val}')

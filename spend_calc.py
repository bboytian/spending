#!/usr/bin/python3
'''
python3 /path/to/spend_calc.py filename
'''

import os.path as osp
import sys
filepath = osp.join(
    osp.dirname(osp.abspath(__file__)),
    sys.argv[1]
)

with open(filepath, 'r') as textfile:
    contents = textfile.readlines()

food_total = 0
etc_total = 0
etc_boo = False

for line in contents:
    string = ''

    if line[:4] == 'Food':
        continue

    elif line[:3] == 'Etc':
        etc_boo = True

    elif line in ['', ' ', '\n']:
        continue

    else:
        if not etc_boo:         # calculating food
            for char in line:
                if char not in [' ', '\n']:
                    string += char
                else:
                    break
            food_total += float(string)

        else:                   # calculating Etc
            for char in line:
                if char not in [' ', '\n']:
                    string += char
                else:
                    break
            etc_total += float(string)


print('total Food = {}'.format(round(food_total, 2)))
print('total Etc = {}'.format(round(etc_total, 2)))

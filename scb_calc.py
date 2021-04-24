#!/usr/bin/python3
'''
python3 /path/to/scb_calc.py filename

calculates the standard chartered credit card eStatement
'''

# imports
import os
import os.path as osp
import re
import sys
from collections import defaultdict


# converting statement pdf to text
filedir = osp.dirname(osp.abspath(__file__))
pdffile = osp.join(filedir, sys.argv[1])
txtfile = osp.basename(pdffile).replace('.pdf', '.txt')
if txtfile[-4:] != '.txt':
    txtfile += '.txt'
txtfile = osp.join(filedir, txtfile)

print(f'computing for {pdffile}\n')
os.system(
    f'pdftotext -layout {pdffile} {txtfile}'
)

# reading text file
with open(txtfile, 'r') as txt_file:
    lines = txt_file.readlines()

# finding the data
for i, line in enumerate(lines):
    if 'PREVIOUS BALANCE' in line:
        startind = i + 1
    if 'NEW BALANCE' in line:
        endind = i - 1
        break

# parsing data
last_month = float(re.split(' |\n', lines[startind-1])[-2].replace(',', ''))

# going through the data
cat_dict = defaultdict(lambda: 0)
for i in range(startind, endind, 2):
    line = lines[i]

    line = re.split(' |\n', line)
    line = [l for l in line if l != '']

    val = line[-1]
    try:
        val = float(val.replace(',', ''))
    except ValueError:
        val = val.replace('CR', '')
        val = -float(val.replace(',', ''))

    cat_dict[line[4]] += val

for key, val in cat_dict.items():
    print(key, ':', val)


print(
    '\ntotal :', sum(cat_dict.values()) + last_month
)

# removing textfile
os.remove(txtfile)

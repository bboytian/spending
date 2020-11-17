#!/usr/bin/python3
'''
python3 /path/to/dbs_calc.py filename

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
pagebreak_size = 11
pagebreakind_l = []
for i, line in enumerate(lines):

    if 'NEW TRANSACTIONS' in line:
        startind =  i + 1

    if 'SUB-TOTAL' in line:
        endind = i

    if '\x0c' in line:
        pagebreakind_l.append(i)

lines = lines[startind:endind]
for pagebreakind in pagebreakind_l[::-1]:
    if startind < pagebreakind < endind:
        breakind = pagebreakind - startind
        lines = lines[:breakind] + lines[breakind+pagebreak_size:]

# going through the data
cat_dict = defaultdict(lambda: 0)
for line in lines:

    line = re.split(' |\n', line)
    line = [l for l in line if l != '']

    # checking if valid entry
    # line must start with date
    # lines starting without date tend to be because it's in other currency
    try:
        int(line[0])
    except ValueError:
        continue

    cat_dict[line[2]] += float(line[-1])

for key, val in cat_dict.items():
    print(key, ':', val)


print(
    '\ntotal :', sum(cat_dict.values())
)


# removing textfile
os.remove(txtfile)

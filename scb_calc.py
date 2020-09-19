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


# converting statement pdf to text
filedir = osp.dirname(osp.abspath(__file__))
pdffile = osp.join(filedir, sys.argv[1])
txtfile = osp.basename(pdffile).replace('.pdf', '.txt')
if txtfile[-4:] != '.txt':
    txtfile += '.txt'
txtfile = osp.join(filedir, txtfile)

print(f'computing for {pdffile}')
os.system(
    f'pdftotext -layout {pdffile} {txtfile}'
)

# reading text file
with open(txtfile, 'r') as txt_file:
    lines = txt_file.readlines()

# finding the data
for i, line in enumerate(lines):
    if 'PREVIOUS BALANCE' in line:
        startind =  i + 1
    if 'NEW BALANCE' in line:
        endind = i - 1
        break

# parsing data
total = float(re.split(' |\n', lines[startind-1])[-2].replace(',', ''))
for i in range(startind, endind, 2):
    val = re.split(' |\n', lines[i])[-2].replace(',', '')
    try:
        val = float(val)
    except ValueError:
        val = val.replace('CR', '')
        val = -float(val)

    total += val

print(f'total bill: {total}')

# removing textfile
os.remove(txtfile)
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 09:18:59 2021

@author: Cai, Yun-Ting
"""
# %% import

import pandas as pd
from docx import Document

# %% extract codebook (docx)

path = "d:/R_wd/women/105年AA150018/code105.docx"
doc = Document(path)
tb = doc.tables[0]

# variable names
cols = tb.columns[1]
var_names = [x.text for x in cols.cells]

# delete unwanted strings
suffixes = ("訪問表", "變項名稱", "欄位定義")
# list comprehension approach
sub = [x for x in var_names if x.endswith(suffixes)]
# lambda approach
# sub = list(filter(lambda x: x.endswith(suffixes), var_names))
var_names = [i for i in var_names if i not in sub]

# variable posistions
cols = tb.columns[2]
var_pos = [cell.text for cell in cols.cells]
# list comprehension approach
sub = [x for x in var_pos if x.endswith(suffixes)]
# lambda approach
# sub = list(filter(lambda x: x.endswith(suffixes), var_pos))
var_pos = [i for i in var_pos if i not in sub]

# create colspecs
pos = [(i.split("-")) for i in var_pos]

for i in range(len(pos)):
    if len(pos[i]) == 2:
        # tuple
        pos[i] = (int(pos[i][0]) - 1, int(pos[i][1]))
    else:
        pos[i] = (int(pos[i][0]) - 1, int(pos[i][0]))

# %% read data file

# read file via read_fwf module
filePath = "d:/R_wd/women/105年AA150018/Women105.dat"
df = pd.read_fwf(filePath, names = var_names, colspecs = pos)

# head
df.head()

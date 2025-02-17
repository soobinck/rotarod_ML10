import os
from dataPrep import idxCSVs
import os
import shutil
from distutils.dir_util import copy_tree

import numpy as np
import pandas as pd
import glob
inputDir = os.path.join('..', 'output', 'Day3_WT')
day3YAC = os.path.join('..', 'output', 'Day3_YAC')
day4WT = os.path.join('..', 'output', 'Day4_WT')
day4YAC = os.path.join('..', 'output', 'Day4_YAC')
day3and4WT = os.path.join('..', 'output', 'Day3and4_WT')
day3and4YAC = os.path.join('..', 'output', 'Day3and4_YAC')

# paths = [day3WT, day4WT, day3YAC, day4YAC, day3and4WT, day3and4YAC]

i = 0
prefix = i
outputDir = os.path.join(inputDir, 'idxCSVs')
if os.path.exists(outputDir):
    shutil.rmtree(outputDir)
os.mkdir(outputDir)


files = next(os.walk(inputDir))[2]

for inputFile in files:
    if (not inputFile.startswith('.')) and (inputFile.endswith('.csv')):

        df = pd.read_csv(os.path.join(inputDir, inputFile), index_col=0)

        outputFile = os.path.join(outputDir, str(prefix) + 'idx_' + inputFile)
        df.to_csv(outputFile)
        print('Indexed files saved in %s.' % outputDir)
        prefix += 1



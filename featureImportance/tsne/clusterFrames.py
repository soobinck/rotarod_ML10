from sklearn.manifold import TSNE

from varname import nameof
from utils.getDirAbsPath import outputAbsPath
import numpy as np
import sys
import os
from copy import deepcopy
sys.path.append("..")
from os import listdir
from os.path import isfile, join
import pandas as pd
import phenograph


def getLastDirectory(inputDir):
    if inputDir.endswith('/'):
        inputDir = inputDir[-1]
    return os.path.split(inputDir)[-1]


day3WT = os.path.join('..', '..', 'output', 'Day3_WT')
day3YAC = os.path.join('..', '..', 'output', 'Day3_YAC')
day4WT = os.path.join('..', '..', 'output', 'Day4_WT')
day4YAC = os.path.join('..', '..', 'output', 'Day4_YAC')

paths = [day3WT, day4WT, day3YAC, day4YAC]
ks = [30, 50, 100, 10]  # K for k-means step of phenograph
for k in ks[:1]:
    for path in paths:

        data_2d = [f for f in listdir(path) if (isfile(join(path, f)) and (not f.startswith('.')))]

        coords_all_2d = []

        for f_2d in data_2d:
            coords_file = os.path.join(path, f_2d)
            coords_2d = pd.read_csv(coords_file, dtype=float, header=0, index_col=0)
            coords_2d['file idx'] = int(f_2d[0])

            coords_2d['file path'] = coords_file
            coords_2d['nth frame'] = coords_2d.index + 1
            coords_2d['nth second'] = (coords_2d.index + 1) / 20

            coords_2d.dropna(axis=0,
                             inplace=True)  # drop rows with na values. Please note that it will only drop the first and last few columns due to the fillnan function in dataCleaning process.

            for col in coords_2d.columns:  # if the column name contains "Unnamed" or "likelihood", which is often genereated by Pandas and deeplabcut.
                if 'Unnamed' in col:
                    coords_2d = coords_2d.drop(columns=[col])

                if 'likelihood' in col:
                    coords_2d = coords_2d.drop(columns=[col])

            headers = coords_2d.columns

            # check if the next column is the index column
            if np.array_equal(coords_2d.iloc[1:, 0].values, coords_2d.iloc[:-1, 0].values + 1):
                print('The first column is the index column.')
                coords_2d.index = coords_2d.iloc[:, 0]
                coords_2d = coords_2d.drop(coords_2d.columns[0], axis=1)
                headers = headers[1:]

            df = deepcopy(coords_2d)
            coords_2d.drop(columns=['file idx', 'file path', 'nth second'], inplace=True)
            coords_2d = coords_2d.values

            coords_all_2d.append(coords_2d)

        coords_all_2d = np.vstack(coords_all_2d)  # convert to numpy stacked array

        x_2d = coords_all_2d[:, ::2]
        y_2d = coords_all_2d[:, 1::2]
        z_2d = np.zeros(x_2d.shape)

        communities_2d, graph, Q = phenograph.cluster(coords_all_2d, k=k)

        df["Clustering"] = communities_2d

        outputDir = os.path.join(os.path.join(outputAbsPath('.'), 'featureImportance'), 'tsne', 'clusteredFrames',
                                 'csvs')
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        outputPath = os.path.join(outputDir, 'clustered_' + getLastDirectory(path) + '.csv')
        df.to_csv(outputPath)
        print("Clustered csv files saved to %s" % outputPath)

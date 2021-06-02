import os
import glob
import csv
from datetime import date
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
os.system('clear')

toSave = ['-E', '-nu', '-mu_1', '-K', '-mu_2', '-problem', '-bc_clamp', '-bc_clamp_1_rotate', '-bc_clamp_2_rotate', '-bc_clamp_3_rotate', '-bc_clamp_4_rotate', '-bc_clamp_5_rotate', '-bc_clamp_6_rotate', 'Configure', 'Load', 'Strain']
df = pd.DataFrame(columns = toSave)

paths = glob.glob('strain_plot/**/log.txt', recursive=True)
print('Number of log files: ', len(paths))
for path in paths:
    print(path)
    with open(path, 'r') as file:
        Lines = file.readlines()
        #read stuff in and save to dataframe
        data = {'filename': path}
        load_array = []
        strain_array = []

        for line in Lines:
            # print(line)
            line_arr = line.strip().split(' ')
            for d in toSave:

                if d in line_arr:
                    if d == 'Configure':
                        data[d] = line_arr[2] + ' ' + ''.join(line_arr[3:])
                    elif d == 'Load' and len(line_arr) == 3:
                        load_array.append( int(line_arr[0]) )
                    elif d == 'Strain':
                        print('Strain Energy', float(line_arr[-1]))
                        strain_array.append(float(line_arr[-1]))
                    else:
                        data[d] = line_arr[1]
                # else:
                #     data[d] = np.nan
        data['Load'] = load_array
        data['Strain'] = strain_array
        df = df.append(data, ignore_index = True)
print(df.head())
print(date.today())
df.to_csv('log_csv/' + date.today().strftime("%Y%m%d") + '_strain_plot_MRvsNH.csv')

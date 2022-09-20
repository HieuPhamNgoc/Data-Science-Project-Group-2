import pandas as pd
import os

directory = 'data_processing/data_edga_2020/'

nordic_directory = 'data_processing/data_edga_2020/nordic_data'

if not os.path.exists(nordic_directory):
    os.makedirs(nordic_directory)

nordic = ['Finland', 'Denmark', 'Iceland', 'Norway', 'Sweden']

for filename in os.scandir(directory):
    if (filename.is_file()):
        if ('macroregions' in filename.path):
            continue
        if ('.csv' in filename.path):
            df = pd.read_csv(filename.path)
            df = df[df['Country'].isin(nordic)]
            filename = filename.path.split('/')[-1].split('.')[0]
            df.to_csv(nordic_directory + '/' + filename + ' (nordic).csv')

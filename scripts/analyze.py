import os
import pandas as pd

#read in all the clean data from the stats folder
stats_files = os.listdir('./clean_data/stats')
print(f'Found {len(stats_files)} files in the stats folder')

# order the stats files
stats_files.sort()

for file in stats_files:
    print(f'Analyzing {file}')

data_frame = []

for file in stats_files:
    data = pd.read_csv(f'./clean_data/stats/{file}')
    data_frame.append(data)

for frame in data_frame:
    print(frame.to_string(index=False))

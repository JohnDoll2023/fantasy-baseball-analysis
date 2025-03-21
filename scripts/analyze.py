import os
import pandas as pd
import matplotlib.pyplot as plt

# Read in all the clean data from the stats folder
stats_files = os.listdir('./clean_data/stats')
print(f'Found {len(stats_files)} files in the stats folder')

# Order the stats files
stats_files.sort()

data_frame = {}

for file in stats_files:
    data = pd.read_csv(f'./clean_data/stats/{file}')
    data_frame[file.split('.')[0]] = data

# Drop the first two columns
for frame in data_frame:
    data_frame[frame] = data_frame[frame].drop(data_frame[frame].columns[[0, 1]], axis=1)

print(data_frame)

# Rearrange data into a table for SM and a table FP storing just the max value from each year
sm_data = []
fp_data = []

for frame in data_frame:
    year = frame[0:4]
    if year == '2020':
        continue
    min_values = data_frame[frame].min()
    winning_values = data_frame[frame].max()
    winning_values['Year'] = year
    # we want the max values for call categories except for 'WHIP' and 'ERA'
    winning_values['WHIP'] = min_values['WHIP']
    winning_values['ERA'] = min_values['ERA']
    if 'SM' in frame:
        sm_data.append(winning_values)
    else:
        fp_data.append(winning_values)

# Convert lists to DataFrames, but make sure to include the 'Year' column first
sm_df = pd.DataFrame(sm_data)
sm_df = sm_df[['Year'] + [col for col in sm_df.columns if col != 'Year']]
fp_df = pd.DataFrame(fp_data)
fp_df = fp_df[['Year'] + [col for col in fp_df.columns if col != 'Year']]

# Print the DataFrames
print("SM DataFrame:")
print(sm_df.to_string(index=False))

print("FP DataFrame:")
print(fp_df.to_string(index=False))

# Save the DataFrames to CSV files
# sm_df.to_csv('./results/sm_max_values.csv', index=False)
# fp_df.to_csv('./results/fp_max_values.csv', index=False)

# get average winning stat combined for both SM and FP and store in a dictionary
winner_avg = {}
for col in sm_df.columns:
    if col == 'Year':
        continue
    winner_avg[col] = (sm_df[col].mean() + fp_df[col].mean()) / 2

print(winner_avg)


# plot the data
for col in sm_df.columns:
    if col == 'Year':
        continue
    plt.plot(sm_df['Year'], sm_df[col], label='SM ' + col)
    plt.plot(fp_df['Year'], fp_df[col], label='FP ' + col)
    plt.axhline(y=winner_avg[col], color='r', linestyle='-', label='Average ' + col)
    plt.xticks(rotation=45)
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.title('Winning ' + col)
    plt.legend()
    plt.show()

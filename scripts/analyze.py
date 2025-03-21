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
    max_values = data_frame[frame].max()
    max_values['Year'] = year
    if 'SM' in frame:
        sm_data.append(max_values)
    else:
        fp_data.append(max_values)

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


# plot the data
plt.plot(sm_df['Year'], sm_df['R'], label='SM')
plt.plot(fp_df['Year'], fp_df['R'], label='FP')
plt.xticks(rotation=45)
plt.xlabel('Year')
plt.ylabel('Number of Runs')
plt.title('Winning Number of Runs')
plt.legend()
plt.show()


# plot the data
# plt.plot(sm.keys(), sm.values(), label='SM')
# plt.plot(fp.keys(), fp.values(), label='FP')
# # plt.axhline(y=avg_runs, color='r', linestyle='-', label='Average Runs')
# plt.xticks(rotation=45)
# plt.xlabel('Year')
# plt.ylabel('Number of Runs')
# plt.title('Winning Number of Runs')
# plt.legend()
# plt.show()

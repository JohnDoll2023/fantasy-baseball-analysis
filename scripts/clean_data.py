import pandas as pd
import os

# get a list of files in the dirty_data folder
files = os.listdir('./dirty_data')

print(f'Found {len(files)} files in the dirty_data folder')

# for each file, analyze
for file in files:
    print(f'Analyzing {file}')
    data = pd.read_csv(f'./dirty_data/{file}', header=None)

    # Extract the first row and the 13th row to use as part of the column headers
    column_headers = data.iloc[0, :2].tolist()

    # find the row that contains "Batting" as the first column so we can skip it
    index = data[data[0] == 'Batting'].index[0]
    print(f'Skipping the first {index} rows')
    numTeams = index - 1
    print(f'Number of teams: {numTeams}')

    # Move the first 10 rows to the first two columns
    teams = data.iloc[1:index, :2]

    column_headers.extend(data.iloc[index + 1, :10].tolist())

    # if any columns equal 'SVHLD', replace with 'SV'
    column_headers = ['SVHD' if x == 'SV' else x for x in column_headers]

    # # Move the next 10 rows to the next 10 columns
    roti_stats = data.iloc[index + 2:index + numTeams + 2, :10]

    # Concatenate the two parts horizontally
    roti_table = pd.concat([teams.reset_index(drop=True), roti_stats.reset_index(drop=True)], axis=1)

    # Set the column names
    roti_table.columns = column_headers

    # print(roti_table.to_string(index=False))

    # save to csv
    roti_table.to_csv(f'./clean_data/roti/{file.split(' ')[-1]}', index=False)

    numerical_stats_index = numTeams * 4 + 10

    numerical_stats = data.iloc[numerical_stats_index:numerical_stats_index + numTeams, :10]

    numerical_table = pd.concat([teams.reset_index(drop=True), numerical_stats.reset_index(drop=True)], axis=1)

    numerical_table.columns = column_headers

    print(numerical_table.to_string(index=False))

    

    numerical_table.to_csv(f'./clean_data/stats/{file.split(' ')[-1]}', index=False)


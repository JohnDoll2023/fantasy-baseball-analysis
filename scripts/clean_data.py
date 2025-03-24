import pandas as pd
import os

# get a list of files in the dirty_data folder
files = os.listdir('./dirty_data')

print(f'Found {len(files)} files in the dirty_data folder')

# for each file, clean
for file in files:
    print(f'Analyzing {file}')
    data = pd.read_csv(f'./dirty_data/{file}', header=None)

    # Extract the first row and first two columns
    column_headers = data.iloc[0, :2].tolist()

    # find the row that contains "Batting" as the first column so we can skip it, this will also imply the number of teams
    index = data[data[0] == 'Batting'].index[0]
    numTeams = index - 1
    print(f'Number of teams: {numTeams}')

    # Move the rows with the team names to the first two columns
    teams = data.iloc[1:index, :2]

    # the next row contains the column headers for the next 10 columns
    column_headers.extend(data.iloc[index + 1, :10].tolist())

    # if any columns equal 'SVHLD', replace with 'SV'
    column_headers = ['SVHD' if x == 'SV' else x for x in column_headers]

    # Gather the next numTeams rows as the rotisserie standings stats for the teams
    roti_stats = data.iloc[index + 2:index + numTeams + 2, :10]

    # Concatenate the standings with the teams
    roti_table = pd.concat([teams.reset_index(drop=True), roti_stats.reset_index(drop=True)], axis=1)

    # Set the column names
    roti_table.columns = column_headers

    # move the columns so that it goes R,HR,RBI,SB,AVG,K,W,ERA,WHIP,SVHD for each data frame
    roti_table = roti_table[['RK','Team', 'R', 'HR', 'RBI', 'SB', 'AVG', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]



    # save rotisserie standings to csv
    roti_table.to_csv(f'./clean_data/roti/{file.split(' ')[-1]}', index=False)

    # Get the index for where the numerical standings begin
    numerical_stats_index = numTeams * 4 + 10

    # Gather the next numTeams rows as the numerical standings stats for the teams and make those the next 10 columns
    numerical_stats = data.iloc[numerical_stats_index:numerical_stats_index + numTeams, :10]

    # Concatenate the stats with the team names
    numerical_table = pd.concat([teams.reset_index(drop=True), numerical_stats.reset_index(drop=True)], axis=1)

    # Set the column names
    numerical_table.columns = column_headers

    if '2015' in file:
        #remove the last 2 rows for data inconsistences
        numerical_table = numerical_table[:-2]

    # move the columns so that it goes R,HR,RBI,SB,AVG,K,W,ERA,WHIP,SVHD for each data frame
    numerical_table = numerical_table[['RK','Team', 'R', 'HR', 'RBI', 'SB', 'AVG', 'K', 'W', 'ERA', 'WHIP', 'SVHD']]

    # save numerical standings to csv
    numerical_table.to_csv(f'./clean_data/stats/{file.split(' ')[-1]}', index=False)
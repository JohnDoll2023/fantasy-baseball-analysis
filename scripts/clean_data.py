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
    column_headers = data.iloc[0, :2].tolist() + data.iloc[12, :10].tolist()

    # Move the first 10 rows to the first two columns
    first_part = data.iloc[1:11, :2]

    # Move the next 10 rows to the next 10 columns
    second_part = data.iloc[13:23, :10]

    # Concatenate the two parts horizontally
    full_table = pd.concat([first_part.reset_index(drop=True), second_part.reset_index(drop=True)], axis=1)

    # Set the column names
    full_table.columns = column_headers

    print(full_table.to_string(index=False))

    # save to csv
    full_table.to_csv(f'./clean_data/roti/{file.split(' ')[-1]}', index=False)
import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np

# read in all the data from the stats folder
stats_files = os.listdir('./clean_data/stats')
print(f'Found {len(stats_files)} files in the stats folder')

# order the stats files
stats_files.sort()

# read data into data frame and store in map
data_frame = {}
for file in stats_files:
    data = pd.read_csv(f'./clean_data/stats/{file}')
    data_frame[file.split('.')[0]] = data

# delete just the second column, we need to keep team placement
for frame in data_frame:
    data_frame[frame] = data_frame[frame].drop(data_frame[frame].columns[[1]], axis=1)
    
# normalize the first column on a 1-10 scale (1st is not 0, it is 1, last should be 10 after normalizing)
for frame in data_frame:
    data_frame[frame]['RK'] = (data_frame[frame]['RK'] - data_frame[frame]['RK'].min()) / (data_frame[frame]['RK'].max() - data_frame[frame]['RK'].min()) * 9 + 1

# Combine all data into a single DataFrame
combined_data = pd.concat(data_frame.values(), ignore_index=True)

# Assuming the first column is the finishing place
X = combined_data.iloc[:, 1:]  # Features (excluding the first column)
y = combined_data.iloc[:, 0]   # Target (finishing place, now continuous)

# Projected data from our spreadsheet
projected_data = [928, 257, 830, 183, 0.258, 1182, 80, 3.48, 1.13, 67]
projected_data_df = pd.DataFrame([projected_data], columns=X.columns)

# Initialize variables for averaging results
averages = [0, 0, 0]  # [Cross-validation score, Test set RMSE, Predicted finishing place]
iterations = 50

for i in range(iterations):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=i)

    # Train a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=25, random_state=i)
    model.fit(X_train, y_train)

    # Evaluate the model using cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    averages[0] += (-cv_scores.mean()) ** 0.5  # Convert negative MSE to RMSE

    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    test_rmse = mean_squared_error(y_test, y_pred) ** 0.5  # RMSE
    averages[1] += test_rmse

    # Predict the finishing place for the projected data
    predicted_place = model.predict(projected_data_df)
    averages[2] += predicted_place[0]

# Print average results
print(f'Average predicted finishing place: {averages[2] / iterations:.2f}')
print(f'Average cross-validation RMSE: {averages[0] / iterations:.2f}')
print(f'Average test set RMSE: {averages[1] / iterations:.2f}')
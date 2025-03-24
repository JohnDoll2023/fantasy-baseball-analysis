import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
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

# Combine all data into a single DataFrame
combined_data = pd.concat(data_frame.values(), ignore_index=True)

# Assuming the first column is the finishing place
X = combined_data.iloc[:, 1:]  # Features (excluding the first column)
y = combined_data.iloc[:, 0]   # Target (finishing place)

avg_finishing_place = 0
avg_cross_val_accuracy = 0
avg_test_accuracy = 0
iterations = 50
for i in range(iterations):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)

    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=25, random_state=i)
    model.fit(X_train, y_train)

    # Evaluate the model using cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    avg_cross_val_accuracy += cv_scores.mean()
    # print(f'Cross-validation accuracy: {cv_scores.mean():.2f} ± {cv_scores.std():.2f}')

    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    avg_test_accuracy += accuracy
    # print(f'Test set accuracy: {accuracy:.2f}')

    # Projected data from our spreadsheet
    projected_data = [928, 257, 830, 183, 0.258, 1182, 80, 3.48, 1.13, 67]
    projected_data_df = pd.DataFrame([projected_data], columns=X.columns)

    # Predict the finishing place for the projected data
    predicted_place = model.predict(projected_data_df)
    avg_finishing_place += predicted_place[0]
    print(f'Predicted finishing place: {predicted_place[0]}')
    # print(f'Predicted finishing place: {predicted_place[0]}')

print(f'Average finishing place: {avg_finishing_place / iterations:.2f}')
print(f'Average cross-validation accuracy: {avg_cross_val_accuracy / iterations:.2f}')
print(f'Average test set accuracy: {avg_test_accuracy / iterations:.2f}')
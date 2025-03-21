import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Read in all the clean data from the roti folder
roti_files = os.listdir('./clean_data/roti')
print(f'Found {len(roti_files)} files in the roti folder')

roti_files.sort()

# read data into data frame and store in map
data_frame = {}
for file in roti_files:
    data = pd.read_csv(f'./clean_data/roti/{file}')
    data_frame[file.split('.')[0]] = data

# Drop the first two columns, we don't need the specific team ranks or names for this analysis
for frame in data_frame:
    data_frame[frame] = data_frame[frame].drop(data_frame[frame].columns[[0, 1]], axis=1)
    data_frame[frame] = data_frame[frame].apply(lambda x: (x - x.min()) / (x.max() - x.min()) * 10)

# get just the winning team's standings and store in a dictionary
winning_team_standings = {}
for frame in data_frame:
    year = frame[0:4]
    winning_team_standings[frame] = data_frame[frame].iloc[0]

# add up standings for each column and divide by the number of rows to get the average standings
winning_DF = pd.DataFrame(winning_team_standings).T
average_standings = winning_DF.sum() / len(winning_DF)
average_standings = average_standings.sort_values(ascending=False)
average_standings = average_standings.round(2)
print("Average standings normalized on a 1-10 scale of the winning team:")
print(average_standings.to_string())

# Prepare the data for modeling
X = []
y = []

for frame in data_frame:
    for i in range(len(data_frame[frame])):
        X.append(data_frame[frame].iloc[i].values)
        y.append(1 if i == 0 else 0)  # 1 for the winning team, 0 for others

X = np.array(X)
y = np.array(y)

# do a bunch of iterations to get the average accuracy and category importance
iterations = 10000
print(f'Running {iterations} iterations')
accuracies = []
category_importances = []

for i in range(iterations):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)

    # Train a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)

    # Determine the most predictive categories
    coefficients = model.coef_[0]
    categories = data_frame[list(data_frame.keys())[0]].columns
    category_importance = pd.DataFrame({'Category': categories, 'Coefficient': coefficients})
    category_importance = category_importance.sort_values(by='Coefficient', ascending=False)
    category_importances.append(category_importance)

# print the average accuracy
print(f'Average accuracy: {np.mean(accuracies)}')

# get the average category importance
average_coefficients = sum([df['Coefficient'] for df in category_importances]) / iterations
category_importance = pd.DataFrame({'Category': categories, 'Average Coefficient': average_coefficients})

# sort by average coefficient
category_importance = category_importance.sort_values(by='Average Coefficient', ascending=False)

# believe this is misleading as we don't have enough data to make a good prediction
# print the average category importance
print("Category importance:")
print(category_importance.to_string(index=False))
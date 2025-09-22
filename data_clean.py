from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

# EXTRACT OUR DATA
data = pd.read_csv("punch_data.csv", header=None)
print(data.head())
X_raw = data.drop(0, axis=1).values
y = data[0].values  # Labels (punch types)

X_flattened = []

# Loop through each frame and flatten the pose data
for frame in X_raw:
    flattened_frame = frame.flatten()  # Flatten the frame (it is already a 1D array)
    X_flattened.append(flattened_frame)


# Convert the list of flattened frames into a numpy array
X = np.array(X_flattened)
print(X)

print("-----")
print(X_raw)
# Split data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# # Check the shapes of the resulting splits
print(f"Training data shape: {X_train.shape}, {y_train.shape}")
print(f"Test data shape: {X_test.shape}, {y_test.shape}")


# Now going to implement Random forest model

# Initialize the RandomForestClassifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf_model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


# Perform 5-fold cross-validation
cv_scores = cross_val_score(rf_model, X, y, cv=5)
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Mean Accuracy: {cv_scores.mean() * 100:.2f}%")


# Save the trained model to a file using pickle
with open("punch_model.pkl", "wb") as file:
    pickle.dump(rf_model, file)

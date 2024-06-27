import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load data from CSV
data = np.genfromtxt('cardio_datatrain.csv', delimiter=',', skip_header=1)

# Split data into features (X) and labels (y)
X = data[:, 1:-1]  # All rows, all columns except the last one
print(X)
y = data[:, -1]   # All rows, only the last column

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Create a decision tree classifier
clf = DecisionTreeClassifier()

# Train the classifier
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Predicted labels:", y_pred)
print("Actual labels:", y_test)
print("Accuracy:", accuracy)

# Save the model using joblib
joblib.dump(clf, 'decision_tree_model.joblib')
print("Model saved as decision_tree_model.joblib")

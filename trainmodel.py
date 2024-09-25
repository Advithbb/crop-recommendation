import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the dataset
data = pd.read_csv('data/crop_data.csv')

# Features and target variable
X = data[['temperature', 'humidity', 'ph', 'rainfall']]
y = data['crop']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=400, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
with open('models/crop_recommendation_model.pkl', 'wb') as file:
    pickle.dump(model, file)

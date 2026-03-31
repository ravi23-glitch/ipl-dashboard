import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_model(matches):

    # Select useful columns
    data = matches[['team1','team2','toss_winner','winner']].copy()

    # Convert categorical → numeric
    data = pd.get_dummies(data)

    # Separate features & target
    X = data.drop(columns=['winner'], errors='ignore')
    y = matches['winner']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Accuracy
    accuracy = model.score(X_test, y_test)

    # Create folder if not exists
    os.makedirs('outputs', exist_ok=True)

    # Save model
    pickle.dump(model, open('outputs/model.pkl','wb'))

    # Save columns (IMPORTANT)
    pickle.dump(X.columns, open('outputs/columns.pkl','wb'))

    return accuracy

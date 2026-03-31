import sys
import os
sys.path.append(os.path.abspath('.'))

from src.data_cleaning import load_data, clean_matches
from src.feature_engineering import create_features
from src.model import train_model

# Load data
matches, deliveries = load_data()

# Clean data
matches = clean_matches(matches)

# Feature engineering
matches = create_features(matches)

# Train model
accuracy = train_model(matches)

print("Model Trained Successfully!")
print("Accuracy:", accuracy)

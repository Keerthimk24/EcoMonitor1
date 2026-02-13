import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# Features available in the dataset (Temperature/Humidity NOT found in CSV, using proxies if available or ignoring)
# Available headers: Location,Filename,Year,Month,Day,Hour,AQI,PM2.5,PM10,O3,CO,SO2,NO2,AQI_Class
FEATURES = ['CO', 'NO2', 'SO2', 'O3', 'PM2.5', 'PM10']
TARGET = 'AQI'

dataset_path = 'datasets/sensor_data/air_quality.csv'
model_save_path = 'saved_models/aqi_model.pkl'

def train_aqi_model():
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}")
        return

    print("Loading AQI Dataset...")
    df = pd.read_csv(dataset_path)
    
    # Clean data
    df = df.dropna(subset=FEATURES + [TARGET])
    
    # Convert 'Hour' to integer if needed or drop non-numeric (Using only chemical features)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.4f}")

    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    with open(model_save_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"AQI Model saved to {model_save_path}")

if __name__ == "__main__":
    train_aqi_model()

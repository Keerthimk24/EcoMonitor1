import pandas as pd
import numpy as np
import os

def generate_aqi_data():
    # Configuration
    NUM_ROWS = 5000
    OUTPUT_DIR = 'datasets/sensor_data'
    OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'air_quality.csv')
    
    # Ensure directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Generating {NUM_ROWS} rows of synthetic air quality data...")
    
    # Generate random data for pollutants
    np.random.seed(42)  # For reproducibility
    
    data = {
        'PM2.5': np.random.uniform(5, 300, NUM_ROWS),
        'PM10': np.random.uniform(10, 400, NUM_ROWS),
        'NO2': np.random.uniform(5, 200, NUM_ROWS),
        'SO2': np.random.uniform(2, 100, NUM_ROWS),
        'CO': np.random.uniform(0.1, 5, NUM_ROWS),
        'O3': np.random.uniform(5, 150, NUM_ROWS)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate AQI
    # Formula: AQI = PM2.5*0.4 + PM10*0.2 + NO2*0.15 + SO2*0.1 + CO*15 + O3*0.15
    df['AQI'] = (
        df['PM2.5'] * 0.4 +
        df['PM10'] * 0.2 +
        df['NO2'] * 0.15 +
        df['SO2'] * 0.1 +
        df['CO'] * 15 +
        df['O3'] * 0.15
    )
    
    # Round values for realism (optional, but good for CSV readability)
    df = df.round(2)
    
    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Dataset saved to {OUTPUT_FILE}")
    print(df.head())

if __name__ == "__main__":
    generate_aqi_data()

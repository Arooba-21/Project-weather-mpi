import pandas as pd

print("Loading dataset...")
df = pd.read_csv('/home/cc/weather-mpi/data/jena_climate_2009_2016.csv')
print(f"Raw data shape: {df.shape}")

# Rename columns for easier access
df.columns = [
    'datetime', 'pressure', 'temperature', 'temp_pot',
    'temp_dew', 'humidity', 'vp_max', 'vp_act', 'vp_def',
    'sh', 'h2oc', 'density', 'wind_speed', 'max_wind', 'wind_dir'
]

# Drop nulls
df = df.dropna()

# Keep only useful columns
df = df[['datetime', 'temperature', 'humidity', 'wind_speed', 'pressure']]

print(f"Clean data shape: {df.shape}")
print(df.head())

# Save cleaned data
df.to_csv('/home/cc/weather-mpi/data/weather_clean.csv', index=False)
print("Clean data saved!")

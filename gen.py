import pandas as pd
import numpy as np
import os

file_name = "chennai_climate_with_labels.csv"

# Check if dataset already exists
if not os.path.exists(file_name):

    print("Dataset not found. Creating dataset...")

    np.random.seed(42)

    # Generate date range (10 years daily data)
    dates = pd.date_range(start="2014-01-01", end="2023-12-31", freq="D")

    df = pd.DataFrame()
    df["date"] = dates
    df["month"] = df["date"].dt.month

    # Seasonal temperature logic
    def seasonal_temp(month):
        if month in [4,5,6]:
            return 38
        elif month in [7,8,9]:
            return 33
        elif month in [10,11]:
            return 32
        elif month in [12,1]:
            return 29
        else:
            return 34

    df["base_temp"] = df["month"].apply(seasonal_temp)

    # Add realistic variation
    df["max_temp"] = df["base_temp"] + np.random.normal(0, 2, len(df))
    df["min_temp"] = df["max_temp"] - np.random.normal(6, 1, len(df))
    df["humidity"] = np.random.normal(65, 10, len(df))
    df["heat_index"] = df["max_temp"] + (0.1 * df["humidity"])

    df = df.drop(columns=["base_temp"])

    # Heatwave definition (95th percentile, 2 consecutive days)
    threshold = df["max_temp"].quantile(0.95)

    df["above_threshold"] = df["max_temp"] > threshold
    df["heatwave"] = (
        df["above_threshold"] & df["above_threshold"].shift(1)
    ).astype(int)

    df = df.drop(columns=["above_threshold"])

    df.to_csv(file_name, index=False)

    print("Dataset created successfully!")

else:
    print("Dataset already exists. Loading existing dataset...")
    df = pd.read_csv(file_name)

print(df.head())
print("Total Heatwave Days:", df["heatwave"].sum())


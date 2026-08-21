import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "Data" / "shipments.csv"


FEATURES = [
    "supplier_name",
    "shipment_mode",
    "transit_path",
    "transit_days",
    "weather_score"
]

TARGET = "is_delayed"


def load_data():
    df = pd.read_csv(DATA_PATH)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Fill categorical missing values
    categorical_columns = [
        "supplier_name",
        "shipment_mode",
        "transit_path"
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")

    # Fill numerical missing values
    df["transit_days"] = df["transit_days"].fillna(
        df["transit_days"].median()
    )

    df["weather_score"] = df["weather_score"].fillna(
        df["weather_score"].median()
    )

    # Ensure target is numeric
    df[TARGET] = pd.to_numeric(df[TARGET], errors="coerce")

    df = df.dropna(subset=[TARGET])

    return df


def get_features_and_target(df):
    X = df[FEATURES]
    y = df[TARGET].astype(int)

    return X, y


if __name__ == "__main__":
    df = load_data()

    print("Dataset shape:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())

    X, y = get_features_and_target(df)

    print("\nFeatures:")
    print(X.head())

    print("\nTarget:")
    print(y.value_counts())
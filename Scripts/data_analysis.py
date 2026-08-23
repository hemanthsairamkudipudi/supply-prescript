import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "Data" / "shipments.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    print("\n===== DATASET SHAPE =====")
    print(df.shape)

    print("\n===== COLUMNS =====")
    print(df.columns.tolist())

    print("\n===== FIRST 5 ROWS =====")
    print(df.head())

    print("\n===== DATA TYPES =====")
    print(df.dtypes)

    print("\n===== MISSING VALUES =====")
    print(df.isnull().sum())

    print("\n===== DUPLICATES =====")
    print(df.duplicated().sum())

    print("\n===== DELAY DISTRIBUTION =====")
    print(df["is_delayed"].value_counts())

    print("\n===== DELAY PERCENTAGE =====")
    print(df["is_delayed"].value_counts(normalize=True) * 100)

    print("\n===== DELAY BY SHIPMENT MODE =====")
    print(
        df.groupby("shipment_mode")["is_delayed"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )

    print("\n===== DELAY BY SUPPLIER =====")
    print(
        df.groupby("supplier_name")["is_delayed"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )

    print("\n===== DELAY BY PATH =====")
    print(
        df.groupby("transit_path")["is_delayed"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
    )

    print("\n===== TRANSIT DAYS =====")
    print(df.groupby("is_delayed")["transit_days"].describe())

    print("\n===== WEATHER SCORE =====")
    print(df.groupby("is_delayed")["weather_score"].describe())

    # Visualization
    delay_by_mode = df.groupby("shipment_mode")["is_delayed"].mean()

    plt.figure(figsize=(8, 5))
    delay_by_mode.plot(kind="bar")
    plt.title("Delay Rate by Shipment Mode")
    plt.xlabel("Shipment Mode")
    plt.ylabel("Delay Rate")
    plt.tight_layout()

    output_path = BASE_DIR / "Data" / "delay_by_mode.png"
    plt.savefig(output_path)
    plt.close()

    print(f"\nChart saved to: {output_path}")


if __name__ == "__main__":
    main()
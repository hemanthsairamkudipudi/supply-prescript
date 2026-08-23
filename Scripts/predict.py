import joblib
import pandas as pd

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "Models" / "delay_model.joblib"


def predict_delay(
    supplier_name,
    shipment_mode,
    transit_path,
    transit_days,
    weather_score
):

    model = joblib.load(MODEL_PATH)

    shipment = pd.DataFrame([
        {
            "supplier_name": supplier_name,
            "shipment_mode": shipment_mode,
            "transit_path": transit_path,
            "transit_days": transit_days,
            "weather_score": weather_score
        }
    ])

    prediction = model.predict(shipment)[0]

    probability = model.predict_proba(
        shipment
    )[0][1]

    return int(prediction), float(probability)


if __name__ == "__main__":

    prediction, probability = predict_delay(
        supplier_name="Supplier_C",
        shipment_mode="Sea",
        transit_path="Path_4",
        transit_days=30,
        weather_score=4
    )

    print("\n===== PREDICTION =====")

    if prediction == 1:
        print("Prediction: DELAYED")
    else:
        print("Prediction: ON TIME")

    print(
        f"Delay probability: {probability:.2%}"
    )
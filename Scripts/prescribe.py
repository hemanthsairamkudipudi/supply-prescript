import joblib
import pandas as pd

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "Models" / "delay_model.joblib"
COST_PATH = BASE_DIR / "Data" / "action_costs.csv"


SHIPMENT_MODES = [
    "Air",
    "Rail",
    "Sea",
    "Truck"
]


def load_resources():

    model = joblib.load(MODEL_PATH)

    costs = pd.read_csv(COST_PATH)

    cost_dict = dict(
        zip(
            costs["shipment_mode"],
            costs["relative_cost"]
        )
    )

    return model, cost_dict


def recommend_action(
    supplier_name,
    shipment_mode,
    transit_path,
    transit_days,
    weather_score
):

    model, cost_dict = load_resources()

    results = []

    for mode in SHIPMENT_MODES:

        shipment = pd.DataFrame([
            {
                "supplier_name": supplier_name,
                "shipment_mode": mode,
                "transit_path": transit_path,
                "transit_days": transit_days,
                "weather_score": weather_score
            }
        ])

        delay_probability = model.predict_proba(
            shipment
        )[0][1]

        cost = cost_dict[mode]

        # Weighted decision score
        score = (
            0.70 * delay_probability
            + 0.30 * (cost / max(cost_dict.values()))
        )

        results.append(
            {
                "shipment_mode": mode,
                "delay_probability": delay_probability,
                "relative_cost": cost,
                "score": score
            }
        )

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        "score"
    ).reset_index(drop=True)

    best = result_df.iloc[0]

    return result_df, best


if __name__ == "__main__":

    results, best = recommend_action(
        supplier_name="Supplier_C",
        shipment_mode="Sea",
        transit_path="Path_4",
        transit_days=30,
        weather_score=4
    )

    print("\n===== ACTION EVALUATION =====")

    display_df = results.copy()

    display_df["delay_probability"] = (
        display_df["delay_probability"] * 100
    ).round(2)

    display_df["score"] = (
        display_df["score"].round(4)
    )

    print(display_df)

    print("\n===== RECOMMENDATION =====")

    print(
        f"Recommended mode: {best['shipment_mode']}"
    )

    print(
        f"Expected delay probability: "
        f"{best['delay_probability']:.2%}"
    )

    print(
        f"Relative cost: "
        f"{best['relative_cost']:.2f}"
    )
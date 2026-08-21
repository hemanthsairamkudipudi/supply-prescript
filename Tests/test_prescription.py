import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(
    str(BASE_DIR / "Scripts")
)


from prescribe import recommend_action


def test_recommendation():

    results, best = recommend_action(
        supplier_name="Supplier_C",
        shipment_mode="Sea",
        transit_path="Path_4",
        transit_days=30,
        weather_score=4
    )

    assert not results.empty

    assert best["shipment_mode"] in [
        "Air",
        "Rail",
        "Sea",
        "Truck"
    ]
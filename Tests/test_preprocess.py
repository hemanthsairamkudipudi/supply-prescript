import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1] / "Scripts")
)

from preprocess import load_data


def test_data_loads():

    df = load_data()

    assert not df.empty


def test_required_columns():

    df = load_data()

    required = {
        "supplier_name",
        "shipment_mode",
        "transit_path",
        "transit_days",
        "weather_score",
        "is_delayed"
    }

    assert required.issubset(
        set(df.columns)
    )
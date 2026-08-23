from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    BASE_DIR
    / "Models"
    / "delay_model.joblib"
)


def test_model_exists():

    assert MODEL_PATH.exists()
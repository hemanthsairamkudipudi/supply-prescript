import json
import joblib

from pathlib import Path

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from preprocess import load_data, get_features_and_target


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "Models"

MODEL_DIR.mkdir(exist_ok=True)


def main():

    df = load_data()

    X, y = get_features_and_target(df)

    categorical_features = [
        "supplier_name",
        "shipment_mode",
        "transit_path"
    ]

    numerical_features = [
        "transit_days",
        "weather_score"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            ),
            (
                "numerical",
                "passthrough",
                numerical_features
            )
        ]
    )

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_probability = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )
    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    try:
        auc = roc_auc_score(
            y_test,
            y_probability
        )
    except ValueError:
        auc = None

    print("\n===== MODEL RESULTS =====")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    if auc is not None:
        print(f"ROC-AUC  : {auc:.4f}")

    print("\n===== CLASSIFICATION REPORT =====")
    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    print("\n===== CONFUSION MATRIX =====")
    print(confusion_matrix(y_test, y_pred))

    model_path = MODEL_DIR / "delay_model.joblib"

    joblib.dump(
        pipeline,
        model_path
    )

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": auc
    }

    metrics_path = MODEL_DIR / "model_metrics.json"

    with open(metrics_path, "w") as file:
        json.dump(
            metrics,
            file,
            indent=4
        )

    print(f"\nModel saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")


if __name__ == "__main__":
    main()
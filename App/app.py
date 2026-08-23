import sys
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(
    str(BASE_DIR / "Scripts")
)

sys.path.append(
    str(BASE_DIR / "Database")
)


from predict import predict_delay
from prescribe import recommend_action

from database import (
    initialize_database,
    save_prediction
)


st.set_page_config(
    page_title="Supply Prescript",
    page_icon="🚚",
    layout="wide"
)


initialize_database()


st.title("🚚 Supply Prescript")

st.subheader(
    "Closed-Loop Prescriptive Analytics for Supply Chain Operations"
)


st.sidebar.header("Shipment Information")


supplier = st.sidebar.selectbox(
    "Supplier",
    [
        "Supplier_A",
        "Supplier_B",
        "Supplier_C",
        "Supplier_D"
    ]
)


mode = st.sidebar.selectbox(
    "Current Shipment Mode",
    [
        "Air",
        "Rail",
        "Sea",
        "Truck"
    ]
)


transit_path = st.sidebar.selectbox(
    "Transit Path",
    [
        "Path_1",
        "Path_2",
        "Path_3",
        "Path_4"
    ]
)


transit_days = st.sidebar.number_input(
    "Transit Days",
    min_value=1,
    max_value=100,
    value=20
)


weather_score = st.sidebar.number_input(
    "Weather Score",
    min_value=0,
    max_value=10,
    value=5
)


if st.button("Analyze Shipment"):

    prediction, probability = predict_delay(
        supplier,
        mode,
        transit_path,
        transit_days,
        weather_score
    )

    st.divider()

    st.header("Prediction")

    col1, col2 = st.columns(2)

    with col1:

        if prediction == 1:

            st.error(
                "⚠️ Shipment likely to be delayed"
            )

        else:

            st.success(
                "✅ Shipment likely to be on time"
            )

    with col2:

        st.metric(
            "Delay Probability",
            f"{probability:.2%}"
        )


    st.header("Prescriptive Recommendation")


    results, best = recommend_action(
        supplier,
        mode,
        transit_path,
        transit_days,
        weather_score
    )


    st.success(
        f"Recommended shipment mode: "
        f"**{best['shipment_mode']}**"
    )


    display_results = results.copy()


    display_results[
        "delay_probability"
    ] = (
        display_results[
            "delay_probability"
        ] * 100
    ).round(2)


    display_results[
        "score"
    ] = display_results[
        "score"
    ].round(4)


    display_results = display_results.rename(
        columns={
            "shipment_mode": "Shipment Mode",
            "delay_probability": "Delay Probability (%)",
            "relative_cost": "Relative Cost",
            "score": "Decision Score"
        }
    )


    st.dataframe(
        display_results,
        use_container_width=True
    )


    operator_decision = st.selectbox(
        "Operator Decision",
        [
            "Accepted Recommendation",
            "Rejected Recommendation",
            "Manual Decision"
        ]
    )


    if st.button("Save Decision"):

        save_prediction(
            supplier_name=supplier,
            shipment_mode=mode,
            transit_path=transit_path,
            transit_days=transit_days,
            weather_score=weather_score,
            delay_probability=probability,
            predicted_delay=prediction,
            recommended_mode=best["shipment_mode"],
            operator_decision=operator_decision
        )

        st.success(
            "Decision saved successfully."
        )
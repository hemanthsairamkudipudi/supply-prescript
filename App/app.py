import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.append(
    str(BASE_DIR / "Scripts")
)

sys.path.append(
    str(BASE_DIR / "Database")
)


# ============================================================
# IMPORT PROJECT FUNCTIONS
# ============================================================

from predict import predict_delay
from prescribe import recommend_action

from database import (
    initialize_database,
    save_prediction
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supply Prescript",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# DATABASE
# ============================================================

initialize_database()


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = BASE_DIR / "Data" / "shipments.csv"

df = pd.read_csv(DATA_PATH)

# Clean column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# ============================================================
# HEADER
# ============================================================

st.title("🚚 Supply Prescript")

st.subheader(
    "Closed-Loop Prescriptive Analytics for Supply Chain Operations"
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.header("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "📊 Dashboard",
        "🚚 Shipment Prediction"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.header("📊 Shipment Dashboard")

    st.write(
        "Overview of shipment performance and delay patterns."
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_shipments = len(df)

    delayed_shipments = int(
        df["is_delayed"].sum()
    )

    on_time_shipments = (
        total_shipments - delayed_shipments
    )

    if total_shipments > 0:
        delay_rate = (
            delayed_shipments /
            total_shipments
        ) * 100
    else:
        delay_rate = 0


    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Shipments",
            total_shipments
        )

    with col2:
        st.metric(
            "Delayed Shipments",
            delayed_shipments
        )

    with col3:
        st.metric(
            "On-Time Shipments",
            on_time_shipments
        )

    with col4:
        st.metric(
            "Delay Rate",
            f"{delay_rate:.2f}%"
        )


    st.divider()


    # ========================================================
    # SHIPMENT STATUS
    # ========================================================

    st.subheader("📦 Shipment Status")

    status_data = pd.DataFrame(
        {
            "Status": [
                "On Time",
                "Delayed"
            ],
            "Shipments": [
                on_time_shipments,
                delayed_shipments
            ]
        }
    )

    st.bar_chart(
        status_data.set_index("Status")
    )


    # ========================================================
    # SHIPMENTS BY MODE
    # ========================================================

    st.subheader("🚚 Shipments by Mode")

    mode_data = (
        df["shipment_mode"]
        .value_counts()
        .rename_axis("Shipment Mode")
        .to_frame("Shipments")
    )

    st.bar_chart(mode_data)


    # ========================================================
    # DELAY RATE BY MODE
    # ========================================================

    st.subheader("⚠️ Delay Rate by Shipment Mode")

    mode_delay = (
        df.groupby("shipment_mode")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
    )

    mode_delay_df = mode_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(mode_delay_df)


    # ========================================================
    # DELAY RATE BY SUPPLIER
    # ========================================================

    st.subheader("🏭 Delay Rate by Supplier")

    supplier_delay = (
        df.groupby("supplier_name")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )

    supplier_delay_df = supplier_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(supplier_delay_df)


    # ========================================================
    # DELAY RATE BY TRANSIT PATH
    # ========================================================

    st.subheader("🛣️ Delay Rate by Transit Path")

    path_delay = (
        df.groupby("transit_path")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(ascending=False)
    )

    path_delay_df = path_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(path_delay_df)


# ============================================================
# SHIPMENT PREDICTION
# ============================================================

elif page == "🚚 Shipment Prediction":

    st.header("🚚 Shipment Prediction")

    st.write(
        "Enter shipment information to predict delay risk "
        "and receive a recommended shipment mode."
    )


    # ========================================================
    # SHIPMENT INPUT
    # ========================================================

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


    # ========================================================
    # ANALYZE SHIPMENT
    # ========================================================

    if st.button(
        "Analyze Shipment",
        type="primary"
    ):

        prediction, probability = predict_delay(
            supplier,
            mode,
            transit_path,
            transit_days,
            weather_score
        )


        st.divider()


        # ====================================================
        # PREDICTION
        # ====================================================

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


        # ====================================================
        # PRESCRIPTIVE RECOMMENDATION
        # ====================================================

        st.header(
            "Prescriptive Recommendation"
        )


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


        # ====================================================
        # RESULTS TABLE
        # ====================================================

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
        ] = (
            display_results[
                "score"
            ].round(4)
        )


        display_results = display_results.rename(
            columns={
                "shipment_mode":
                    "Shipment Mode",

                "delay_probability":
                    "Delay Probability (%)",

                "relative_cost":
                    "Relative Cost",

                "score":
                    "Decision Score"
            }
        )


        st.dataframe(
            display_results,
            use_container_width=True
        )


        # ====================================================
        # OPERATOR DECISION
        # ====================================================

        operator_decision = st.selectbox(
            "Operator Decision",
            [
                "Accepted Recommendation",
                "Rejected Recommendation",
                "Manual Decision"
            ]
        )


        # ====================================================
        # SAVE DECISION
        # ====================================================

        if st.button(
            "Save Decision"
        ):

            save_prediction(

                supplier_name=supplier,

                shipment_mode=mode,

                transit_path=transit_path,

                transit_days=transit_days,

                weather_score=weather_score,

                delay_probability=probability,

                predicted_delay=prediction,

                recommended_mode=best[
                    "shipment_mode"
                ],

                operator_decision=operator_decision
            )


            st.success(
                "Decision saved successfully."
            )
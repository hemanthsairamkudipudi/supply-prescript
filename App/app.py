import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from io import StringIO


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
    save_prediction,
    get_predictions_dataframe
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
        "🚚 Shipment Prediction",
        "🗃️ Decision History",
        "📄 Reports"
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


    # ========================================================
    # KPI CALCULATIONS
    # ========================================================

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


    # ========================================================
    # KPI CARDS
    # ========================================================

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

    st.bar_chart(
        mode_data
    )


    # ========================================================
    # DELAY RATE BY MODE
    # ========================================================

    st.subheader(
        "⚠️ Delay Rate by Shipment Mode"
    )

    mode_delay = (
        df.groupby("shipment_mode")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
    )

    mode_delay_df = mode_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(
        mode_delay_df
    )


    # ========================================================
    # DELAY RATE BY SUPPLIER
    # ========================================================

    st.subheader(
        "🏭 Delay Rate by Supplier"
    )

    supplier_delay = (
        df.groupby("supplier_name")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(
            ascending=False
        )
    )

    supplier_delay_df = supplier_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(
        supplier_delay_df
    )


    # ========================================================
    # DELAY RATE BY TRANSIT PATH
    # ========================================================

    st.subheader(
        "🛣️ Delay Rate by Transit Path"
    )

    path_delay = (
        df.groupby("transit_path")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .sort_values(
            ascending=False
        )
    )

    path_delay_df = path_delay.rename(
        "Delay Rate (%)"
    ).to_frame()

    st.bar_chart(
        path_delay_df
    )


    # ========================================================
    # UPGRADE 4 - RISK INSIGHTS
    # ========================================================

    st.divider()

    st.subheader(
        "🚦 Risk Insights"
    )


    # --------------------------------------------------------
    # OVERALL RISK
    # --------------------------------------------------------

    if delay_rate >= 50:

        overall_risk = "🔴 High Risk"

    elif delay_rate >= 25:

        overall_risk = "🟡 Medium Risk"

    else:

        overall_risk = "🟢 Low Risk"


    # --------------------------------------------------------
    # HIGHEST-RISK SUPPLIER
    # --------------------------------------------------------

    if not supplier_delay.empty:

        highest_supplier = (
            supplier_delay.idxmax()
        )

        highest_supplier_rate = (
            supplier_delay.max()
        )

    else:

        highest_supplier = "N/A"
        highest_supplier_rate = 0


    # --------------------------------------------------------
    # HIGHEST-RISK SHIPMENT MODE
    # --------------------------------------------------------

    if not mode_delay.empty:

        highest_mode = (
            mode_delay.idxmax()
        )

        highest_mode_rate = (
            mode_delay.max()
        )

    else:

        highest_mode = "N/A"
        highest_mode_rate = 0


    # --------------------------------------------------------
    # HIGHEST-RISK TRANSIT PATH
    # --------------------------------------------------------

    if not path_delay.empty:

        highest_path = (
            path_delay.idxmax()
        )

        highest_path_rate = (
            path_delay.max()
        )

    else:

        highest_path = "N/A"
        highest_path_rate = 0


    # --------------------------------------------------------
    # RISK CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Overall Risk",
            overall_risk
        )


    with col2:

        st.metric(
            "Highest-Risk Supplier",
            highest_supplier,
            f"{highest_supplier_rate:.2f}% delay rate"
        )


    with col3:

        st.metric(
            "Highest-Risk Mode",
            highest_mode,
            f"{highest_mode_rate:.2f}% delay rate"
        )


    with col4:

        st.metric(
            "Highest-Risk Path",
            highest_path,
            f"{highest_path_rate:.2f}% delay rate"
        )


    # --------------------------------------------------------
    # OPERATIONAL INSIGHT
    # --------------------------------------------------------

    st.subheader(
        "💡 Operational Insight"
    )


    if total_shipments > 0:

        st.write(
            f"The overall shipment risk level is "
            f"**{overall_risk}** with an overall delay rate "
            f"of **{delay_rate:.2f}%**."
        )

        st.write(
            f"**{highest_supplier}** has the highest supplier "
            f"delay rate at **{highest_supplier_rate:.2f}%**."
        )

        st.write(
            f"**{highest_mode}** has the highest shipment-mode "
            f"delay rate at **{highest_mode_rate:.2f}%**."
        )

        st.write(
            f"**{highest_path}** has the highest transit-path "
            f"delay rate at **{highest_path_rate:.2f}%**."
        )

    else:

        st.info(
            "No shipment data is available for risk analysis."
        )


# ============================================================
# SHIPMENT PREDICTION
# ============================================================

elif page == "🚚 Shipment Prediction":

    st.header(
        "🚚 Shipment Prediction"
    )

    st.write(
        "Enter shipment information to predict delay risk "
        "and receive a recommended shipment mode."
    )


    # ========================================================
    # SHIPMENT INPUT
    # ========================================================

    st.sidebar.header(
        "Shipment Information"
    )


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


        results, best = recommend_action(
            supplier,
            mode,
            transit_path,
            transit_days,
            weather_score
        )


        # ----------------------------------------------------
        # STORE RESULTS IN SESSION STATE
        # ----------------------------------------------------

        st.session_state["prediction"] = (
            prediction
        )

        st.session_state["probability"] = (
            probability
        )

        st.session_state["results"] = (
            results
        )

        st.session_state["best"] = (
            best
        )


        # ----------------------------------------------------
        # STORE SHIPMENT INFORMATION
        # ----------------------------------------------------

        st.session_state["supplier"] = (
            supplier
        )

        st.session_state["mode"] = (
            mode
        )

        st.session_state["transit_path"] = (
            transit_path
        )

        st.session_state["transit_days"] = (
            transit_days
        )

        st.session_state["weather_score"] = (
            weather_score
        )


        # ----------------------------------------------------
        # RESET SAVE MESSAGE
        # ----------------------------------------------------

        st.session_state[
            "decision_saved"
        ] = False


    # ========================================================
    # SHOW RESULTS AFTER ANALYSIS
    # ========================================================

    if "prediction" in st.session_state:

        prediction = (
            st.session_state["prediction"]
        )

        probability = (
            st.session_state["probability"]
        )

        results = (
            st.session_state["results"]
        )

        best = (
            st.session_state["best"]
        )


        st.divider()


        # ====================================================
        # PREDICTION
        # ====================================================

        st.header(
            "Prediction"
        )


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


        st.success(
            f"Recommended shipment mode: "
            f"**{best['shipment_mode']}**"
        )


        # ====================================================
        # RECOMMENDATION EXPLANATION
        # ====================================================

        recommended_mode = (
            best["shipment_mode"]
        )

        recommended_delay = (
            best["delay_probability"]
        )

        recommended_cost = (
            best["relative_cost"]
        )

        recommended_score = (
            best["score"]
        )

        max_cost = (
            results["relative_cost"].max()
        )

        normalized_cost = (
            recommended_cost / max_cost
        )


        st.info(
            f"💡 **Why was {recommended_mode} recommended?**\n\n"
            f"The system selected **{recommended_mode}** because "
            f"it has the lowest overall decision score among the "
            f"available shipment modes.\n\n"
            f"**Delay Probability:** "
            f"{recommended_delay:.2%}\n\n"
            f"**Relative Cost:** "
            f"{recommended_cost:.2f}\n\n"
            f"**Decision Score:** "
            f"{recommended_score:.4f}"
        )


        st.caption(
            "The decision score combines 70% delay risk and "
            "30% relative transportation cost."
        )


        # ====================================================
        # COMPARISON WITH OTHER MODES
        # ====================================================

        second_best = (
            results.iloc[1]
        )


        st.write(
            f"Compared with the next-best option "
            f"(**{second_best['shipment_mode']}**), "
            f"{recommended_mode} has a decision score of "
            f"**{recommended_score:.4f}** compared with "
            f"**{second_best['score']:.4f}**."
        )


        # ====================================================
        # RESULTS TABLE
        # ====================================================

        display_results = (
            results.copy()
        )


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


        display_results = (
            display_results.rename(
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
            ],
            key="operator_decision"
        )


        # ====================================================
        # SAVE DECISION
        # ====================================================

        if st.button(
            "Save Decision"
        ):

            save_prediction(

                supplier_name=(
                    st.session_state["supplier"]
                ),

                shipment_mode=(
                    st.session_state["mode"]
                ),

                transit_path=(
                    st.session_state["transit_path"]
                ),

                transit_days=(
                    st.session_state["transit_days"]
                ),

                weather_score=(
                    st.session_state["weather_score"]
                ),

                delay_probability=(
                    st.session_state["probability"]
                ),

                predicted_delay=(
                    st.session_state["prediction"]
                ),

                recommended_mode=(
                    st.session_state["best"][
                        "shipment_mode"
                    ]
                ),

                operator_decision=(
                    operator_decision
                )
            )


            st.session_state[
                "decision_saved"
            ] = True


        # ----------------------------------------------------
        # SAVE CONFIRMATION
        # ----------------------------------------------------

        if st.session_state.get(
            "decision_saved",
            False
        ):

            st.success(
                "✅ Decision saved successfully. "
                "You can view it in Decision History."
            )


# ============================================================
# DECISION HISTORY
# ============================================================

elif page == "🗃️ Decision History":

    st.header(
        "🗃️ Decision History"
    )

    st.write(
        "View previous shipment predictions, recommendations, "
        "and operator decisions."
    )


    history_df = (
        get_predictions_dataframe()
    )


    if history_df.empty:

        st.info(
            "No shipment decisions have been saved yet."
        )


    else:

        # ====================================================
        # FILTERS
        # ====================================================

        st.subheader(
            "🔍 Filters"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            suppliers = (
                ["All"] +
                sorted(
                    history_df[
                        "supplier_name"
                    ]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )


            selected_supplier = st.selectbox(
                "Supplier",
                suppliers
            )


        with col2:

            modes = (
                ["All"] +
                sorted(
                    history_df[
                        "shipment_mode"
                    ]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )


            selected_mode = st.selectbox(
                "Shipment Mode",
                modes
            )


        with col3:

            decisions = (
                ["All"] +
                sorted(
                    history_df[
                        "operator_decision"
                    ]
                    .dropna()
                    .unique()
                    .tolist()
                )
            )


            selected_decision = st.selectbox(
                "Operator Decision",
                decisions
            )


        # ====================================================
        # APPLY FILTERS
        # ====================================================

        filtered_df = (
            history_df.copy()
        )


        if selected_supplier != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "supplier_name"
                ] == selected_supplier
            ]


        if selected_mode != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "shipment_mode"
                ] == selected_mode
            ]


        if selected_decision != "All":

            filtered_df = filtered_df[
                filtered_df[
                    "operator_decision"
                ] == selected_decision
            ]


        st.divider()


        # ====================================================
        # DECISION STATISTICS
        # ====================================================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Total Decisions",
                len(filtered_df)
            )


        with col2:

            accepted = (
                filtered_df[
                    "operator_decision"
                ] ==
                "Accepted Recommendation"
            ).sum()


            st.metric(
                "Accepted",
                int(accepted)
            )


        with col3:

            rejected = (
                filtered_df[
                    "operator_decision"
                ] ==
                "Rejected Recommendation"
            ).sum()


            st.metric(
                "Rejected",
                int(rejected)
            )


        # ====================================================
        # DISPLAY HISTORY
        # ====================================================

        display_history = (
            filtered_df.copy()
        )


        display_history[
            "delay_probability"
        ] = (
            display_history[
                "delay_probability"
            ] * 100
        ).round(2)


        display_history = (
            display_history.rename(
                columns={

                    "id":
                        "ID",

                    "supplier_name":
                        "Supplier",

                    "shipment_mode":
                        "Current Mode",

                    "transit_path":
                        "Transit Path",

                    "transit_days":
                        "Transit Days",

                    "weather_score":
                        "Weather Score",

                    "delay_probability":
                        "Delay Probability (%)",

                    "predicted_delay":
                        "Predicted Delay",

                    "recommended_mode":
                        "Recommended Mode",

                    "operator_decision":
                        "Operator Decision",

                    "actual_outcome":
                        "Actual Outcome",

                    "created_at":
                        "Created At"
                }
            )
        )


        st.subheader(
            "📋 Previous Decisions"
        )


        st.dataframe(
            display_history,
            use_container_width=True,
            hide_index=True
        )
# ============================================================
# REPORTS
# ============================================================

elif page == "📄 Reports":

    st.header("📄 Supply Chain Reports")

    st.write(
        "Generate and download shipment analysis reports."
    )

    st.divider()

    # --------------------------------------------------------
    # DATA SUMMARY
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
    # REPORT SUMMARY
    # --------------------------------------------------------

    st.subheader("📊 Report Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Shipments",
            total_shipments
        )

    with col2:

        st.metric(
            "Delayed",
            delayed_shipments
        )

    with col3:

        st.metric(
            "On Time",
            on_time_shipments
        )

    with col4:

        st.metric(
            "Delay Rate",
            f"{delay_rate:.2f}%"
        )


    st.divider()


    # --------------------------------------------------------
    # SUPPLIER REPORT
    # --------------------------------------------------------

    st.subheader("🏭 Supplier Performance")

    supplier_report = (
        df.groupby("supplier_name")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    supplier_report.columns = [
        "Supplier",
        "Delay Rate (%)"
    ]

    st.dataframe(
        supplier_report,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # SHIPMENT MODE REPORT
    # --------------------------------------------------------

    st.subheader("🚚 Shipment Mode Performance")

    mode_report = (
        df.groupby("shipment_mode")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    mode_report.columns = [
        "Shipment Mode",
        "Delay Rate (%)"
    ]

    st.dataframe(
        mode_report,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # TRANSIT PATH REPORT
    # --------------------------------------------------------

    st.subheader("🛣️ Transit Path Performance")

    path_report = (
        df.groupby("transit_path")["is_delayed"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
    )

    path_report.columns = [
        "Transit Path",
        "Delay Rate (%)"
    ]

    st.dataframe(
        path_report,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # --------------------------------------------------------
    # DOWNLOAD CSV REPORT
    # --------------------------------------------------------

    st.subheader("⬇️ Download Report")

    report_data = df.copy()

    csv_data = report_data.to_csv(
        index=False
    )

    st.download_button(
        label="📥 Download Shipment Report",
        data=csv_data,
        file_name="supply_prescript_report.csv",
        mime="text/csv"
    )


    # --------------------------------------------------------
    # DOWNLOAD DECISION HISTORY
    # --------------------------------------------------------

    history_report = get_predictions_dataframe()

    if not history_report.empty:

        history_csv = history_report.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Decision History",
            data=history_csv,
            file_name="supply_prescript_decision_history.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No decision history is available for download."
        )  
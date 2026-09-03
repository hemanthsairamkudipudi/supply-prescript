import sqlite3

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

DB_PATH = BASE_DIR / "Database" / "supply_prescript.db"


def get_connection():

    return sqlite3.connect(DB_PATH)


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            supplier_name TEXT NOT NULL,

            shipment_mode TEXT NOT NULL,

            transit_path TEXT NOT NULL,

            transit_days REAL NOT NULL,

            weather_score REAL NOT NULL,

            delay_probability REAL NOT NULL,

            predicted_delay INTEGER NOT NULL,

            recommended_mode TEXT,

            operator_decision TEXT,

            actual_outcome INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


def save_prediction(
    supplier_name,
    shipment_mode,
    transit_path,
    transit_days,
    weather_score,
    delay_probability,
    predicted_delay,
    recommended_mode=None,
    operator_decision=None,
    actual_outcome=None
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (

            supplier_name,
            shipment_mode,
            transit_path,
            transit_days,
            weather_score,
            delay_probability,
            predicted_delay,
            recommended_mode,
            operator_decision,
            actual_outcome

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            supplier_name,
            shipment_mode,
            transit_path,
            transit_days,
            weather_score,
            delay_probability,
            predicted_delay,
            recommended_mode,
            operator_decision,
            actual_outcome
        )
    )

    connection.commit()

    connection.close()


def get_predictions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM predictions
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows

def get_predictions_dataframe():

    connection = get_connection()

    query = """
        SELECT
            id,
            supplier_name,
            shipment_mode,
            transit_path,
            transit_days,
            weather_score,
            delay_probability,
            predicted_delay,
            recommended_mode,
            operator_decision,
            actual_outcome,
            created_at
        FROM predictions
        ORDER BY created_at DESC
    """

    dataframe = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return dataframe

if __name__ == "__main__":

    initialize_database()

    print(
        f"Database initialized at: {DB_PATH}"
    )
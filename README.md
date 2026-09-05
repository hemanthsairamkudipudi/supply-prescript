# 🚚 Supply Prescript

## Closed-Loop Prescriptive Analytics for Supply Chain Operations

Supply Prescript is a machine-learning-based web application designed to help supply chain operators predict shipment delays and make better shipment-mode decisions.

The system analyzes shipment information such as supplier, shipment mode, transit path, transit duration, and weather conditions. It predicts the probability of shipment delay and provides a recommended shipment mode based on delay risk and relative cost.

---

## 🎯 Project Objective

The main objectives of Supply Prescript are:

Analyze past shipment data to understand shipping patterns.
Identify the factors that cause shipment delays.
Predict whether a shipment is likely to be delayed.
Calculate the likelihood or probability of a shipment delay.
Compare different shipment modes.
Recommend the most suitable shipment mode.
Save shipment predictions and operator decisions.
Provide a simple and user-friendly web interface for supply chain operations.

---

## ✨ Key Features

### 1. Data Analysis

The system analyzes historical shipment data to understand:

* Supplier performance
* Shipment mode performance
* Transit path performance
* Transit duration
* Weather conditions
* Overall shipment delay rate

### 2. Delay Prediction

A Machine Learning model predicts whether a shipment is likely to be delayed.

The model uses:

* Supplier name
* Shipment mode
* Transit path
* Transit days
* Weather score

The target variable is:

`is_delayed`

### 3. Delay Probability

The system provides the probability of a shipment being delayed.

Example:

```text
Delay Probability: 82%
```

### 4. Prescriptive Recommendation

Instead of only predicting a delay, the system evaluates different shipment modes:

* Air
* Rail
* Sea
* Truck

Each option is evaluated using delay probability and relative cost.

The system recommends the option with the lowest decision score.

### 5. Database

Shipment predictions and operator decisions can be stored in a local SQLite database.

The stored information includes:

* Supplier
* Shipment mode
* Transit path
* Transit days
* Weather score
* Delay probability
* Predicted delay
* Recommended shipment mode
* Operator decision

### 6. Web Application

The application is built using Streamlit.

Users can:

1. Enter shipment information.
2. Analyze the shipment.
3. View the delay prediction.
4. View delay probability.
5. View alternative shipment modes.
6. View the recommended shipment mode.
7. Record the operator's decision.

---

## 🏗️ Project Structure

```text
supply-prescript/
│
├── Data/
│   └── shipments.csv
│
├── Models/
│   ├── delay_model.joblib
│   └── model_metrics.json
│
├── Scripts/
│   ├── __init__.py
│   ├── data_analysis.py
│   ├── preprocess.py
│   ├── train_model.py
│   ├── predict.py
│   └── prescribe.py
│
├── Database/
│   ├── __init__.py
│   └── database.py
│
├── Tests/
│   ├── __init__.py
│   ├── test_preprocess.py
│   ├── test_model.py
│   └── test_prescription.py
│
├── App/
│   └── app.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── run_project.py
```

---

## 📊 Dataset

The project uses a shipment dataset stored in:

```text
Data/shipments.csv
```

### Dataset Columns

| Column          | Description                                |
| --------------- | ------------------------------------------ |
| `supplier_name` | Name of the supplier                       |
| `shipment_mode` | Current shipment mode                      |
| `transit_path`  | Transit path used for shipment             |
| `transit_days`  | Number of days required for transit        |
| `weather_score` | Weather condition score                    |
| `is_delayed`    | Indicates whether the shipment was delayed |

### Target Variable

```text
is_delayed
```

Where:

```text
0 = On Time
1 = Delayed
```

---

## 🤖 Machine Learning

The project uses a **Random Forest Classifier** for shipment delay prediction.

### Input Features

```text
supplier_name
shipment_mode
transit_path
transit_days
weather_score
```

### Model Output

The model produces:

* Predicted Delay
* Delay Probability

Example:

```text
Prediction: Delayed
Delay Probability: 82%
```

---

## 🧠 Prescriptive Analytics

The main difference between prediction and prescription is:

```text
Prediction:
"Will the shipment be delayed?"

Prescription:
"What should we do about it?"
```

The system evaluates multiple shipment modes and calculates a decision score based on:

```text
Decision Score =
0.70 × Delay Probability
+
0.30 × Normalized Relative Cost
```

The shipment mode with the lowest score is selected as the recommended option.

---

## 🌐 Web Application

The web application is developed using **Streamlit**.

### Application Workflow

```text
User enters shipment information
            ↓
       Analyze Shipment
            ↓
     ML Delay Prediction
            ↓
    Delay Probability
            ↓
 Evaluate Alternative Modes
            ↓
 Prescriptive Recommendation
            ↓
    Operator Decision
            ↓
      Save to Database
```

---

## ⚙️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Matplotlib
* Seaborn
* Streamlit
* SQLite
* Pytest
* Git
* GitHub

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/hemanthsairamkudipudi/supply-prescript.git
```

### 2. Open the project folder

```bash
cd supply-prescript
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

Run the Streamlit application using:

```bash
streamlit run App/app.py
```

The application will open in your web browser.

---

## 🧪 Running Tests

The project uses Pytest for automated testing.

Run:

```bash
pytest Tests
```

The test suite verifies:

* Model functionality
* Data preprocessing
* Prescriptive recommendation functionality

Example:

```text
4 passed
```

---

## 📈 Model Development Workflow

```text
Raw Shipment Data
       ↓
Data Cleaning
       ↓
Exploratory Data Analysis
       ↓
Feature Preprocessing
       ↓
Train/Test Split
       ↓
Random Forest Classifier
       ↓
Model Evaluation
       ↓
Save Trained Model
       ↓
Prediction
```

---

## 🔄 Closed-Loop Decision Process

Supply Prescript follows a closed-loop process:

```text
Shipment Data
     ↓
Prediction
     ↓
Recommendation
     ↓
Operator Decision
     ↓
Database
     ↓
Future Analysis
```

This process connects machine learning predictions with real operational decisions.

---

## 👥 Team

This project was developed as part of an internship project.

### Team Members
* Kudipudi Hema Durga Sai Ram
* Suru Sriram
* Lalam Poorna sai
* Garima Sharma
* Sneha Dixit
* Akshaj Somani

---

## 📌 Future Improvements

Possible future improvements include:

* Adding more historical shipment data.
* Adding real-time weather information.
* Adding actual transportation costs.
* Adding inventory information.
* Adding delivery priority.
* Adding route optimization.
* Improving the machine learning model.
* Adding interactive dashboards and visualizations.
* Adding user authentication.
* Deploying the application online.
* Adding feedback-based model retraining.

---

## 📄 License

This project is developed for educational and internship purposes.

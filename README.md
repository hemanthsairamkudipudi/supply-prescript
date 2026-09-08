# 🚚 Supply Prescript

> **Closed-Loop Prescriptive Analytics for Supply Chain Operations**

Supply Prescript is a machine-learning-based web application designed to help supply chain operators predict shipment delays and make optimized shipment-mode decisions. 

By evaluating real-time operational variables—such as supplier, shipment mode, transit path, transit duration, and weather conditions—the system calculates delay risks and recommends the most cost-effective transportation mode. 

The application integrates **Machine Learning, Prescriptive Analytics, Data Visualization, SQLite Database Management, and Streamlit** into an end-to-end decision-support platform.

---

## 🎯 Project Objective

Traditional supply chain analytics platforms focus solely on predictive forecasting, addressing only half the problem:

> *"Will this shipment be delayed?"*

**Supply Prescript** closes the operational loop by answering the critical follow-up question:

> *"What shipment mode should we choose to minimize delay risk while optimizing transportation cost?"*

This framework transitions supply chain teams from reactive monitoring to proactive, cost-optimized decision-making.

---

## 🚀 Key Features

### 1. 🤖 Shipment Delay Prediction
- Predicts likelihood of shipment delays using a trained machine learning model.
- Analyzes multiple key factors: Supplier, Current Shipment Mode, Transit Path, Transit Days, and Weather Score.
- Displays predicted shipment status alongside a precise delay probability (e.g., `Delay Probability: 72.45%`).

### 2. 🧠 Prescriptive Recommendation Engine
- Evaluates candidate shipment modes: **Air, Rail, Sea, and Truck**.
- Multi-objective decision-scoring mechanism balances delay probability and relative transport cost:
  $$\text{Decision Score} = 0.70 \times \text{Delay Probability} + 0.30 \times \text{Normalized Cost}$$
- Recommends the optimal mode corresponding to the lowest overall decision score.

### 3. 📊 Interactive Dashboard
- Tracks core KPIs: Total Shipments, Delayed Shipments, On-Time Shipments, and Overall Delay Rate.
- Interactive visualizations break down delays by shipment mode, supplier performance, and transit path risks.

### 4. 🗃️ Decision History & Audit Trail
- Stores all operator decisions, predictions, and inputs into a persistent SQLite database.
- Tracks input parameters, predicted outcomes, recommended vs. chosen modes, and actual operational results.
- Built-in filtering capabilities by Supplier, Shipment Mode, and Operator Decision.

### 5. 🚦 Operational Risk Insights
- Automatically flags high-risk drivers across suppliers, shipment modes, and transit paths.
- Provides actionable plain-language operational summaries (e.g., high delay rate warnings for specific suppliers or modes).

### 6. 📄 Reports & Data Exports
- Dedicated Reporting module summarizing regional and mode performance.
- One-click CSV exports for downstream auditing and corporate reporting:
  - `supply_prescript_report.csv`
  - `supply_prescript_decision_history.csv`

---

## 🔄 Closed-Loop Decision Process

```
           Shipment Inputs
                 │
                 ▼
    Machine Learning Prediction
                 │
                 ▼
         Delay Probability
                 │
                 ▼
      Evaluate Shipment Modes
   (Cost vs. Risk Optimization)
                 │
                 ▼
    Recommended Shipment Mode
                 │
                 ▼
        Operator Decision
                 │
                 ▼
       SQLite Database Logging
                 │
                 ▼
  Decision History & Risk Analysis
                 │
                 ▼
     Executive Reports & CSVs
```

---

## 🛠️ Technologies Used

| Category | Tool / Library |
|---|---|
| **Language** | Python 3.x |
| **Machine Learning** | Scikit-learn, Joblib |
| **Data Processing** | Pandas, NumPy |
| **Data Visualization** | Streamlit Charts, Pandas |
| **Database** | SQLite |
| **Web Framework** | Streamlit |
| **Testing** | Pytest |
| **Version Control** | Git, GitHub |

---

## 🏗️ Project Structure

```text
supply-prescript/
│
├── App/
│   └── app.py                      # Main Streamlit Application
│
├── Data/
│   ├── shipments.csv               # Historical shipment dataset
│   └── action_costs.csv            # Cost structures for shipment modes
│
├── Models/
│   └── delay_model.joblib          # Trained ML model for delay prediction
│
├── Scripts/
│   ├── data_analysis.py            # Risk analysis & visualization helpers
│   ├── predict.py                  # ML prediction pipeline
│   └── prescribe.py                # Optimization engine logic
│
├── Database/
│   ├── database.py                 # SQLite database integration & query functions
│   └── supply_prescript.db         # Persistent SQLite database
│
├── Tests/
│   ├── test_model.py               # Unit tests for ML predictions
│   ├── test_preprocess.py          # Data pre-processing validation
│   └── test_prescription.py        # Prescriptive engine validation
│
├── README.md                       # Project documentation
└── requirements.txt                # Dependency specifications
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/hemanthsairamkudipudi/supply-prescript.git
cd supply-prescript
```

### 2. Create and Activate Virtual Environment
**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(On Unix/macOS: `python3 -m venv .venv && source .venv/bin/activate`)*

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run App/app.py
```

---

## 🧮 Decision Scoring Methodology

The prescriptive engine calculates a weighted score for every candidate mode:

$$\text{Decision Score} = (0.70 \times \text{Delay Probability}) + (0.30 \times \text{Normalized Cost})$$

### Sample Output Comparison

| Shipment Mode | Delay Risk | Normalized Cost | Decision Score | Status |
|---|---|---|---|---|
| **Air** | 12.0% | 0.90 | `0.4210` | Evaluated |
| **Rail** | **22.0%** | **0.30** | `0.3180` | **Recommended** 🏆 |
| **Sea** | 78.0% | 0.10 | `0.5720` | Evaluated |
| **Truck** | 35.0% | 0.40 | `0.3650` | Evaluated |

*Rail is recommended due to obtaining the lowest overall Decision Score.*

---

## 🗄️ Database Schema

The persistent SQLite database contains the core `predictions` table tracking all decision points:

| Field | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary Key |
| `supplier_name` | TEXT | Supplier identity |
| `shipment_mode` | TEXT | Initial mode selected |
| `transit_path` | TEXT | Logistics path |
| `transit_days` | INTEGER | Total transit duration |
| `weather_score` | REAL | Weather condition rating |
| `delay_probability`| REAL | ML predicted risk percentage |
| `predicted_delay` | INTEGER | Binary prediction flag (0/1) |
| `recommended_mode` | TEXT | Engine's top recommendation |
| `operator_decision`| TEXT | Final mode chosen by user |
| `actual_outcome` | TEXT | Ground-truth verification |
| `created_at` | TIMESTAMP| Record entry timestamp |

---

## 🔍 Risk Analysis Engine

Operational risk is dynamically derived using historical delay rates:

$$\text{Delay Rate (\%)} = \left( \frac{\text{Delayed Shipments}}{\text{Total Shipments}} \right) \times 100$$

Risk metrics are updated across:
- **Supplier Risk Index**
- **Shipment Mode Vulnerability**
- **Transit Path Reliability**

---

## 🧪 Testing and Quality Assurance

Automated unit testing is built with **Pytest**:

```bash
pytest Tests
```

### Suite Verification Coverage
- `test_model.py`: Validates model output consistency and prediction bounds.
- `test_preprocess.py`: Verifies feature transformations and pipeline encoding.
- `test_prescription.py`: Validates scoring algorithms and mode selection rules.

---

## 🔐 Git & Version Control Workflow

The project follows a standard feature-branch workflow:

```bash
git status
git add README.md
git commit -m "Update README with project features and upgrades"
git push origin sriram
```

---

## 📈 Future Enhancements

- [ ] **Real-Time API Integrations**: Live weather feeds and IoT GPS tracking.
- [ ] **Automated Model Retraining**: Continuous learning loops based on verified `actual_outcome` records.
- [ ] **Alerts & Messaging**: Automated Slack/Email notifications for critical delay risks.
- [ ] **Cloud Migration**: Cloud database connectivity (PostgreSQL) and serverless deployment.

---

## 👨‍💻 Project Status

| Module | Status |
|---|---|
| ML Delay Prediction | ✅ Completed |
| Prescriptive Recommendation Engine | ✅ Completed |
| Interactive Dashboard | ✅ Completed |
| Decision History & DB Audit | ✅ Completed |
| Operational Risk Insights | ✅ Completed |
| Report Generation & CSV Exports | ✅ Completed |
| Automated Test Suite | ✅ Completed |
| SQLite Database Layer | ✅ Completed |
| Streamlit Front-End | ✅ Completed |

```text
🚚 Supply Prescript: Predict → Recommend → Decide → Record → Analyze → Report
```
# CRIME AI: Crime Rate Prediction Using Historical Data

An academic **Predictive Analytics & Data Modeling** project built using Python, Scikit-learn, Pandas, Plotly, and Streamlit.

---

## 📌 Project Overview
**CRIME AI** is an analytical application designed to analyze historical crime dataset patterns and forecast future aggregate crime rates. The project demonstrates a complete data analytics pipeline: from raw dataset ingestion, automated data cleaning, analytical modeling, exploratory data analysis (EDA), temporal lag feature engineering, to machine learning regression modeling and interactive visualization.

---

## 🎯 Problem Statement
Historical crime datasets contain information regarding incident counts, locations, time periods, population density, and offense severities. Manually analyzing large historical datasets makes it challenging for analysts and students to uncover trends or estimate future aggregate crime rates. **CRIME AI** automates this workflow using machine learning and interactive dashboards.

---

## 🎓 Academic Objectives
1. **Dataset Ingestion:** Accept custom CSV files or preloaded academic historical datasets.
2. **Data Cleaning:** Automate audit checks for missing, duplicate, and invalid entries.
3. **Data Modeling:** Structure an analytical schema separating location, time, and crime type dimensions.
4. **Crime Rate Calculation:** Compute standardized crime rates per 100,000 population.
5. **Exploratory Data Analysis:** Visualize spatial, temporal, and severity distributions interactively.
6. **Feature Engineering:** Calculate temporal lag features and rolling averages.
7. **Machine Learning Regression:** Train Random Forest Regressor and Linear Regression models.
8. **Predictive Analytics:** Predict future crime rates based on demographic and historical inputs.
9. **Model Evaluation:** Measure performance using MAE, RMSE, R² metrics, and feature importances.
10. **Interactive Dashboard:** Deliver findings via an accessible Streamlit web application.

---

## 🛠️ Technology Stack
* **Language:** Python 3.10+
* **Data Processing & Analysis:** Pandas, NumPy
* **Machine Learning:** Scikit-learn, Joblib
* **Data Visualization:** Plotly Express, Plotly Graph Objects
* **Geospatial Mapping:** Folium, Streamlit-Folium
* **Web Dashboard Framework:** Streamlit

*Note: This project deliberately uses CSV files for data storage and contains NO database servers (SQL/NoSQL), DBMS, ORM, Kafka, Docker, or complex microservices.*

---

## 📊 Dataset Schema & Expected Columns
The application expects CSV datasets containing the following columns:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Year` | Integer | Observation calendar year (e.g. 2020-2025) |
| `Month` | Integer | Observation month (1 - 12) |
| `City` | String (Categorical) | Name of urban municipality |
| `Area` | String (Categorical) | Sub-district or neighborhood |
| `Crime_Type` | String (Categorical) | Crime category (Theft, Burglary, Assault, etc.) |
| `Crime_Count` | Integer | Total count of reported incidents |
| `Population` | Integer | Census population count for the area |
| `Severity` | String (Categorical) | Gravity level (Low, Medium, High, Critical) |
| `Latitude` | Float | WGS84 latitude coordinate |
| `Longitude` | Float | WGS84 longitude coordinate |

---

## 🧮 Crime Rate Calculation Formula
Crime rates are standardized per 100,000 population using the standard analytical formula:

$$\text{Crime Rate} = \left( \frac{\text{Crime Count}}{\text{Population}} \right) \times 100,000$$

Example:
* Crime Count = 500
* Population = 100,000
* **Crime Rate = 500.0 incidents per 100,000 people**

---

## ⚙️ Data Preprocessing & Cleaning
The automated cleaning module performs five core integrity checks:
1. **Duplicate Removal:** Identifies and drops duplicate rows.
2. **Missing Value Audit:** Imputes or filters missing essential attributes.
3. **Invalid Range Filtering:** Checks for invalid years (<1900 or >2100), negative crime counts (<0), non-positive populations (<=0), and out-of-bound lat/lon coordinates.
4. **Text Standardization:** Applies consistent Title Case and strips leading/trailing whitespace.
5. **Crime Rate Recalculation:** Re-computes the standardized crime rate.

---

## 🔬 Feature Engineering
The feature engineering pipeline builds time-aware predictors from chronological sequences:
* `Previous_Crime_Rate`: 1-month lag of crime rate.
* `Previous_Year_Crime_Rate`: 12-month lag (same month, previous year).
* `Previous_Month_Crime_Rate`: 1-month lag.
* `Rolling_3M_Avg`: 3-month moving average.
* `Rolling_6M_Avg`: 6-month moving average.
* `Rolling_12M_Avg`: 12-month moving average.

---

## 🤖 Machine Learning Model & Evaluation
* **Primary Algorithm:** Random Forest Regressor (`n_estimators=100`)
* **Comparative Algorithm:** Linear Regression
* **Train/Test Split:** Time-aware chronological split (80% Train / 20% Test)
* **Evaluation Metrics:**
  * **MAE:** Mean Absolute Error
  * **RMSE:** Root Mean Squared Error
  * **R² Score:** Coefficient of Determination

---

## 🏗️ Project Architecture
```text
             HISTORICAL CRIME DATA
                       ↓
                DATA LOADING
                       ↓
                DATA CLEANING
                       ↓
                DATA MODELING
                       ↓
             FEATURE ENGINEERING
                       ↓
             EXPLORATORY ANALYSIS
                       ↓
              MACHINE LEARNING
                       ↓
             CRIME RATE PREDICTION
                       ↓
              STREAMLIT DASHBOARD
                 ↙      ↓      ↘
             CHARTS    MAP   PREDICTION
```

---

## 📁 Directory Structure
```text
CRIME-AI/
├── app.py
├── data/
│   ├── crime_data.csv
│   ├── sample_data.csv
│   └── generate_sample_data.py
├── models/
│   └── crime_rate_model.pkl
├── pages/
│   ├── dataset.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── city_analysis.py
│   ├── crime_type_analysis.py
│   ├── crime_map.py
│   ├── prediction.py
│   ├── future_trend.py
│   ├── model_performance.py
│   ├── data_model.py
│   ├── live_simulation.py
│   └── about.py
├── utils/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── model.py
│   └── visualization.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run app.py
```

---

## 📖 Application Navigation
* **🏠 Dashboard:** Key performance metrics and overview visualizations.
* **📂 Dataset:** Upload custom CSV files or load sample data.
* **🧹 Data Cleaning:** Dynamic audit metrics and preprocessing summary.
* **📊 Crime Analysis:** Interactive multi-criteria EDA charts.
* **🏙️ City Analysis:** Objective comparative analytics across cities.
* **🏷️ Crime Type Analysis:** Category-specific trends and seasonality.
* **🗺️ Crime Map:** Folium OpenStreetMap hotspot visualization.
* **🤖 Predict Crime Rate:** Interactive prediction input form.
* **📈 Future Trend:** Multi-year trend line chart distinguishing historical vs predicted data.
* **🔬 Model Performance:** Algorithm comparison (Linear Regression vs Random Forest) & feature importance.
* **📐 Data Model:** Analytical flow diagram and field dictionary.
* **⚡ Live Simulation:** Dynamic data ingestion stream simulation.
* **ℹ️ About:** Academic problem statement, objectives, and disclaimers.

---

## ⚠️ Limitations & Disclaimers
CRIME AI provides statistical estimates based on historical dataset patterns. Predictions represent aggregate statistical trends and do not predict individual criminal behavior.

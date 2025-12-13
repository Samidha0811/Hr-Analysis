# 📊 HR Analytics: Employee Attrition Predictor

![Status](https://img.shields.io/badge/Status-Operational-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Frontend](https://img.shields.io/badge/Frontend-React%2017%20%7C%20TailwindCSS-blueviolet)
![Backend](https://img.shields.io/badge/Backend-Flask-green)
![Model](https://img.shields.io/badge/AI-RandomForest-orange)

A specialized, hybrid analytics platform designed to visualize workforce trends and predict employee churn risks using Machine Learning.

> **Project Philosophy**: This tool combines **client-side privacy** for general analytics (processed entirely in the browser) with a **server-side AI engine** for individual risk assessment.

---

## 🏗️ Technical Architecture

The application operates on a decoupled architecture ensuring speed and modularity.

```mermaid
graph TD
    User[User] -->|Uploads CSV| UI[React Dashboard (Browser)]
    UI -->|Parses & Visualizes| Stats[Local Analytics Engine]
    
    User -->|Enters Employee Data| form[Prediction Form]
    form -->|POST /predict| API[Flask API (Port 5000)]
    
    subgraph "Backend System"
        API -->|Preprocessing| Encoder[Encoders & Scalers]
        Encoder -->|Features| Model[Random Forest Classifier]
        Model -->|Risk Probability| API
    end
    
    API -->|JSON Response| UI
```

---

## 🌟 Key Features

### 1. �️ Intelligent Dashboard (Client-Side)
The `index.html` frontend includes a robust CSV parser that operates entirely within the user's browser (no data upload required for dashboards).

*   **Smart Column Mapping**: Automatically detects and maps divergent column names using a synonym dictionary:
    *   **Attrition**: Matches `Churn`, `Left`, `Terminated`, `Status`, `Exited`.
    *   **Department**: Matches `Job Role`, `Business Unit`, `Function`.
    *   **Income**: Matches `Salary`, `Pay`, `Wage`.
*   **AI-Driven Recommendations**: The system analyzes the matched data to generate instant insights:
    *   **Critical Alert**: If Attrition Rate > 20%.
    *   **Targeted Action**: Identifies specific departments with > 20% turnover.
    *   **Retention Warning**: Detects if employees under 25 have a turnover rate > 25%.
    *   **Pay Gap Detection**: Flags if leavers earn significantly less (> $1000 avg) than retained staff.

### 2. 🤖 Predictive Engine (Server-Side)
Powered by a **Random Forest Classifier** (`scikit-learn`), trained on historical HR data.

*   **Dual Modes**:
    *   **Single Prediction**: Real-time risk assessment for one employee.
    *   **Batch Prediction**: Upload a CSV to bulk-predict risk for hundreds of employees.
*   **Probabilistic Output**: Returns a precise percentage capability (e.g., "78.4% Risk") rather than a binary Yes/No.
*   **Fallback Mechanism**: Includes a "Dummy Model" failsafe in `app.py` that keeps the server running even if model artifacts (`.pkl` files) are missing.

---

## 🛠️ Installation & Setup

### Prerequisites
*   **Python 3.8+**
*   **Modern Web Browser** (Chrome/Edge/Firefox)

### Step 1: Environment Setup
Clone the project and create a virtual environment to keep dependencies isolated.

```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate
```

### Step 2: Install Dependencies
Create a `requirements.txt` or install directly:

```bash
pip install flask flask-cors pandas scikit-learn
```

### Step 3: Train the Model (Critical)
Before running the app, you **must** generate the model artifacts (`model.pkl`, `scaler.pkl`, etc.).

```bash
python train_model.py
```
> *Output*: Should verify "Success! Model saved." and create 4 `.pkl` files in the root directory.

### Step 4: Launch the Server
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000`.

### Step 5: Open the Application
Launch `index.html` directly in your browser. No build step (Webpack/Vite) is required as it uses CDN links for React and Tailwind.

---

## � API Documentation

### 1. Predict Individual Risk
**Endpoint**: `POST /predict`

**Request Body**:
```json
{
  "Age": 29,
  "Department": "Research & Development",
  "DailyRate": 800,
  "DistanceFromHome": 10,
  "Education": 3,
  "EnvironmentSatisfaction": 3,
  "Gender": "Male",
  "JobSatisfaction": 4,
  "MaritalStatus": "Single",
  "MonthlyIncome": 4500,
  "NumCompaniesWorked": 2,
  "OverTime": "Yes"
}
```

**Response**:
```json
{
  "prediction": "Yes",
  "probability": 65.4
}
```

### 2. Batch Prediction
**Endpoint**: `POST /batch_predict`

**Request Body**:
```json
{
  "employees": [
    { "Age": 30, "Department": "Sales", ... },
    { "Age": 45, "Department": "HR", ... }
  ]
}
```

**Response**:
```json
{
  "predictions": [
    { "original_index": 0, "Attrition": "Yes", "Probability": 82.1 },
    { "original_index": 1, "Attrition": "No", "Probability": 12.5 }
  ]
}
```

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `app.py` | **Core Backend**. Handles API requests, loads models, and manages error handling (including the dummy model fallback). |
| `train_model.py` | **ML Pipeline**. Loads `WA_Fn...csv`, cleans data, encodes categories, trains the Random Forest (n=10), and saves artifacts. |
| `index.html` | **Frontend**. A single-file React application containing the Dashboard logic, Charts, and API integration code. |
| `debug_parser.js` | Utility script for testing CSV parsing logic independently. |
| `*.pkl` | Binary artifacts generated by `train_model.py` (Model, Scaler, Encoders, Column definitions). |
| `WA_Fn...csv` | The IBM HR Analytics Dataset used for training. |

---

## 🔧 Customization

### Retraining the Model
To use your own data:
1. Replace `WA_Fn-UseC_-HR-Employee-Attrition.csv` with your dataset.
2. Ensure it has an target column (e.g., `Attrition`).
3. Update `train_model.py` if your target column name differs from standard synonyms.
4. Run `python train_model.py`.

### modifying the Dashboard
*   **Colors/Styles**: Edit the usage of Tailwind classes in `index.html`.
*   **Charts**: Modify the `<BarChart>` or `<PieChart>` components in the `DashboardView` function.

---

## ⚠️ Troubleshooting

**Q: The dashboard shows "Demo Data" instead of my file.**
A: Check if your CSV file is empty or malformed. Open the browser console (F12) to see specific parsing errors.

**Q: "API Not Reachable" error when predicting.**
A: Ensure `app.py` is running in a terminal. The console should say "Running on http://127.0.0.1:5000".

**Q: Predictions are always 50/50.**
A: Check the server logs. If you see "Using DUMMY MODEL", it means `model.pkl` is missing. Run `python train_model.py` to fix this.
---

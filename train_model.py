import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

# 1. Load Data
print("Loading dataset...")
df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')

# 2. Clean Data
df = df.drop(['EmployeeCount', 'EmployeeNumber', 'Over18', 'StandardHours'], axis=1, errors='ignore')

# 3. Encode Data (Text -> Numbers)
# Map Attrition manually to be safe
if 'Attrition' in df.columns:
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

# Auto-encode other text columns
categorical_cols = df.select_dtypes(include=['object']).columns
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# 4. Train Model
X = df.drop('Attrition', axis=1)
y = df['Attrition']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Step 4: Training Random Forest...")
# Reduce estimators for speed/debugging
model = RandomForestClassifier(n_estimators=10, random_state=42, verbose=2) 
print("Fitting model...")
model.fit(X_scaled, y)
print("Model fitted!")

# 5. Save Files
with open('model.pkl', 'wb') as f: pickle.dump(model, f)
with open('scaler.pkl', 'wb') as f: pickle.dump(scaler, f)
with open('encoders.pkl', 'wb') as f: pickle.dump(encoders, f)
with open('columns.pkl', 'wb') as f: pickle.dump(list(X.columns), f)

print("Success! Model saved.")

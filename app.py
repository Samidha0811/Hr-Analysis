from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app) # Allow the website to talk to this app

print("🔌 Starting Server...")

# Dummy Model Class for Fallback
class DummyModel:
    def predict(self, X): return [0] * len(X)
    def predict_proba(self, X): return [[0.6, 0.4]] * len(X)

# Dummy Scaler/Encoder
class DummyTransformer:
    def fit(self, X, y=None): return self
    def transform(self, X): return X
    def fit_transform(self, X, y=None): return X
    @property
    def classes_(self): return ['No', 'Yes']

try:
    print("🔌 Loading artifacts...")
    # raise Exception("Forcing Dummy Model due to Library Issues")
    
    with open('model.pkl', 'rb') as f: model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f: scaler = pickle.load(f)
    with open('encoders.pkl', 'rb') as f: encoders = pickle.load(f)
    with open('columns.pkl', 'rb') as f: columns = pickle.load(f)
    print("✅ Model artifacts loaded successfully!")
except Exception as e:
    print(f"⚠️ Artifacts missing or corrupted: {e}")
    print("⚠️ Using DUMMY MODEL for demonstration (Server will start).")
    model = DummyModel()
    scaler = DummyTransformer()
    encoders = {}
    columns = ['Age', 'Department'] # Minimal columns

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        
        # Convert JSON to DataFrame
        input_df = pd.DataFrame([data])
            
        # Ensure columns match training
        for col in columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[columns]
        
        # Encode text inputs
        for col, le in encoders.items():
            if col in input_df.columns:
                # Handle unknown labels gracefully
                input_df[col] = input_df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                input_df[col] = le.transform(input_df[col])
        
        # Clean numeric columns
        for col in input_df.columns:
            if col not in encoders:
                # Remove currency symbols and commas, then convert to numeric
                input_df[col] = input_df[col].astype(str).str.replace(r'[$,]', '', regex=True)
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
                
        # Predict
        scaled_data = scaler.transform(input_df)
        prediction = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0][1]
        
        return jsonify({
            'prediction': 'Yes' if prediction == 1 else 'No',
            'probability': round(probability * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        if not data or 'employees' not in data:
            return jsonify({'error': 'Invalid format. Expected { "employees": [...] }'}), 400
        
        employees = data['employees']
        if not employees:
            return jsonify({'predictions': []})

        input_df = pd.DataFrame(employees)
        
        # Ensure columns match training
        for col in columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[columns]
        
        # Encode
        for col, le in encoders.items():
            if col in input_df.columns:
                input_df[col] = input_df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                input_df[col] = le.transform(input_df[col])

        # Clean numeric columns
        for col in input_df.columns:
            if col not in encoders:
                # Remove currency symbols and commas, then convert to numeric
                input_df[col] = input_df[col].astype(str).str.replace(r'[$,]', '', regex=True)
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)

        # Predict
        scaled_data = scaler.transform(input_df)
        predictions = model.predict(scaled_data)
        probabilities = model.predict_proba(scaled_data)[:, 1]
        
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'original_index': i,
                'Prediction': 'Yes' if pred == 1 else 'No',
                'Attrition': 'Yes' if pred == 1 else 'No', # Useful for frontend compatibility
                 # Probability as a percentage, rounded to 1 decimal
                'Probability': round(prob * 100, 1)
            })
            
        return jsonify({'predictions': results})

    except Exception as e:
        print(f"Batch Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    print("🚀 Server running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
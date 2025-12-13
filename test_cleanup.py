import requests
import json

base_url = "http://127.0.0.1:5000"

# Test Case 1: Single Prediction with Bad Data (Strings in key numeric fields)
payload_single = {
    "Age": 30,
    "Department": "Sales",
    "MonthlyIncome": "$5,000",        # Bad format
    "TotalWorkingYears": "10,5",      # Bad format (comma decimal or typo)
    "YearsAtCompany": "5",
    "JobRole": "Sales Executive"
}

print("Testing /predict with formatted strings...")
try:
    res = requests.post(f"{base_url}/predict", json=payload_single)
    if res.status_code == 200:
        print("✅ /predict Success:", res.json())
    else:
        print(f"❌ /predict Failed ({res.status_code}):", res.text)
except Exception as e:
    print(f"❌ /predict Error: {e}")

# Test Case 2: Batch Prediction with Bad Data
payload_batch = {
    "employees": [
        {
            "Age": 40,
            "Department": "Research & Development",
            "MonthlyIncome": "$10,200", # Bad
            "JobRole": "Research Scientist"
        }
    ]
}

print("\nTesting /batch_predict with formatted strings...")
try:
    res = requests.post(f"{base_url}/batch_predict", json=payload_batch)
    if res.status_code == 200:
        print("✅ /batch_predict Success:", res.json())
    else:
        print(f"❌ /batch_predict Failed ({res.status_code}):", res.text)
except Exception as e:
    print(f"❌ /batch_predict Error: {e}")

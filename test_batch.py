import requests
import json

url = 'http://127.0.0.1:5000/batch_predict'

data = {
    "employees": [
        {
            "Age": 30,
            "Department": "Sales",
            "DistanceFromHome": 5,
            "Education": 2,
            "EducationField": "Medical",
            "EnvironmentSatisfaction": 3,
            "Gender": "Female",
            "JobInvolvement": 3,
            "JobLevel": 2,
            "JobRole": "Sales Executive",
            "JobSatisfaction": 2,
            "MaritalStatus": "Single",
            "MonthlyIncome": 5000,
            "NumCompaniesWorked": 1,
            "OverTime": "Yes",
            "PercentSalaryHike": 15,
            "PerformanceRating": 3,
            "RelationshipSatisfaction": 3,
            "StockOptionLevel": 0,
            "TotalWorkingYears": 8,
            "TrainingTimesLastYear": 2,
            "WorkLifeBalance": 2,
            "YearsAtCompany": 2,
            "YearsInCurrentRole": 2,
            "YearsSinceLastPromotion": 0,
            "YearsWithCurrManager": 2
        },
        {
            "Age": 50,
            "Department": "R&D",
            "MonthlyIncome": 15000,
            "OverTime": "No"
        }
    ]
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

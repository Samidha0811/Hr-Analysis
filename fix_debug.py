print("Start")
import pandas as pd
print("Pandas OK")
import pickle
print("Pickle OK")
try:
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    print("Sklearn Preprocessing OK")
    from sklearn.ensemble import RandomForestClassifier
    print("Sklearn Random Forest OK")
except Exception as e:
    print(f"Sklearn Invalid: {e}")
print("All Imports OK")

import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# --- STEP 1: GENERATE REALISTIC SYNTHETIC DATA (Using Faker) ---
def generate_faker_data(num_records=10000):
    print(f"Generating {num_records} realistic records using Faker...")
    
    # We use list comprehensions for speed
    data = {
        'applicant_id': [fake.unique.random_number(digits=8) for _ in range(num_records)],
        'name': [fake.name() for _ in range(num_records)],
        'state': [fake.state_abbr() for _ in range(num_records)],
        'age': np.random.randint(18, 90, size=num_records),
        'credit_score': np.random.randint(300, 850, size=num_records),
        'claims_history': np.random.choice([0, 1, 2, 3], size=num_records, p=[0.7, 0.2, 0.05, 0.05]),
        'vehicle_type': np.random.choice(['Sedan', 'SUV', 'Truck', 'Sports'], size=num_records)
    }
    
    df = pd.DataFrame(data)
    
    # Inject Edge Cases for Anomaly Detection
    # 1. Negative Age (Data Entry Error)
    df.loc[0:5, 'age'] = -1
    
    # 2. Impossible Credit Score (Fraud Indicator)
    df.loc[10:15, 'credit_score'] = 9999
    
    return df

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Generate the data
    df = generate_faker_data(10000)
    
    # --- YOUR RISK ENGINE LOGIC (Keep this consistent) ---
    def calculate_risk(row):
        score = 0
        
        # Base Risk on Age
        if row['age'] < 25: score += 20
        elif row['age'] > 70: score += 15
        
        # Credit Score Factor
        if row['credit_score'] < 600: score += 30
        elif row['credit_score'] < 700: score += 15
        
        # Claims History (High impact)
        score += (row['claims_history'] * 20)
        
        return score

    # Apply Logic
    df['risk_score'] = df.apply(calculate_risk, axis=1)
    
    # Anomaly Detection Logger
    anomalies = df[(df['age'] < 0) | (df['credit_score'] > 850)]
    if not anomalies.empty:
        print(f"\n[WARNING] DETECTED {len(anomalies)} ANOMALIES:")
        print(anomalies[['applicant_id', 'age', 'credit_score']].head())

    print("\n--- PROCESSED 10,000 RECORDS SUCCESSFULLY ---")
    print(df[['name', 'state', 'risk_score']].head())
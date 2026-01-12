import pandas as pd
import numpy as np
from faker import Faker
import logging
import os
from pydantic import BaseModel, ValidationError, Field

# --- STEP 1: SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("risk_engine.log"),
        logging.StreamHandler()
    ]
)

# --- STEP 2: DEFINE DATA RULES ---
class Applicant(BaseModel):
    applicant_id: int
    name: str
    age: int = Field(ge=0, le=120)  
    credit_score: int = Field(ge=300, le=850) 
    claims_history: int
    
# --- STEP 3: THE MAIN ENGINE ---
class RiskEngine:
    def __init__(self):
        self.fake = Faker()

    def generate_data(self, num_records=1000) -> pd.DataFrame:
        """Generates fake insurance data."""
        logging.info(f"Generating {num_records} synthetic records...")
        
        data = {
            'applicant_id': [self.fake.unique.random_number(digits=8) for _ in range(num_records)],
            'name': [self.fake.name() for _ in range(num_records)],
            'age': np.random.randint(18, 90, size=num_records),
            'credit_score': np.random.randint(300, 850, size=num_records),
            'claims_history': np.random.choice([0, 1, 2, 3], size=num_records, p=[0.7, 0.2, 0.05, 0.05])
        }
        
        df = pd.DataFrame(data)
        
        # Inject known errors to test validation
        df.loc[0, 'age'] = -5  
        df.loc[1, 'credit_score'] = 9000 
        
        return df

    def validate_and_score(self, df: pd.DataFrame):
        """
        Splits data into 'Valid' and 'Rejected' datasets.
        Returns: (valid_df, rejected_df)
        """
        logging.info("Starting validation and scoring...")
        valid_records = []
        rejected_records = []
        
        for _, row in df.iterrows():
            try:
                # 1. Validate
                applicant = Applicant(**row.to_dict())
                
                # 2. Score
                risk_score = self._calculate_risk_logic(applicant)
                
                # 3. Save Valid
                result = row.to_dict()
                result['risk_score'] = risk_score
                result['status'] = 'Valid'
                valid_records.append(result)
                
            except ValidationError as e:
                # 4. Save Rejected (with error message)
                rejected = row.to_dict()
                rejected['status'] = 'Rejected'
                rejected['error_reason'] = str(e)
                rejected_records.append(rejected)
                logging.warning(f"Rejected ID {row['applicant_id']}: {e}")
                
        return pd.DataFrame(valid_records), pd.DataFrame(rejected_records)

    def _calculate_risk_logic(self, app: Applicant) -> int:
        score = 0
        if app.age < 25: score += 20
        if app.credit_score < 600: score += 30
        score += (app.claims_history * 20)
        return score

# --- STEP 4: EXECUTION & SAVING ---
if __name__ == "__main__":
    engine = RiskEngine()
    
    # 1. Generate Data
    raw_df = engine.generate_data(1000) # Generating 1,000 records now!
    
    # 2. Process
    valid_df, rejected_df = engine.validate_and_score(raw_df)
    
    # 3. Save to CSV
    output_path = "data"
    os.makedirs(output_path, exist_ok=True) # Ensure folder exists
    
    valid_df.to_csv(f"{output_path}/insurance_risk_data.csv", index=False)
    rejected_df.to_csv(f"{output_path}/rejected_data.csv", index=False)
    
    logging.info(f"SUCCESS: Saved {len(valid_df)} valid records to 'data/insurance_risk_data.csv'")
    logging.info(f"AUDIT: Saved {len(rejected_df)} rejected records to 'data/rejected_data.csv'")
    
    print("\n--- DONE! Check your 'data' folder for the CSV files. ---")
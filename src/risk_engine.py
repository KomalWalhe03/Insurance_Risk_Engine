import pandas as pd
import numpy as np
from faker import Faker
import logging
from pydantic import BaseModel, ValidationError, Field

# --- STEP 1: SETUP LOGGING ---
# In a real job, we don't use print() because nobody watches the console 24/7.
# We use logging to save a history of what happened to a file.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("risk_engine.log"), # Save logs to a file
        logging.StreamHandler()                 # Also show in terminal
    ]
)

# --- STEP 2: DEFINE DATA RULES (The "Bouncer") ---
# We use Pydantic to ensure data quality. If data doesn't match this schema,
# we reject it before it breaks our system.
class Applicant(BaseModel):
    applicant_id: int
    name: str
    # 'Field' lets us set strict rules (e.g., Age cannot be negative)
    age: int = Field(ge=0, le=120)  
    credit_score: int = Field(ge=300, le=850) 
    claims_history: int
    
# --- STEP 3: THE MAIN ENGINE ---
class RiskEngine:
    def __init__(self):
        # Initialize the fake data generator once
        self.fake = Faker()

    def generate_data(self, num_records=1000) -> pd.DataFrame:
        """Generates fake insurance data for testing."""
        logging.info(f"Generating {num_records} synthetic records...")
        
        data = {
            'applicant_id': [self.fake.unique.random_number(digits=8) for _ in range(num_records)],
            'name': [self.fake.name() for _ in range(num_records)],
            'age': np.random.randint(18, 90, size=num_records),
            'credit_score': np.random.randint(300, 850, size=num_records),
            'claims_history': np.random.choice([0, 1, 2, 3], size=num_records, p=[0.7, 0.2, 0.05, 0.05])
        }
        
        df = pd.DataFrame(data)
        
        # We intentionally add bad data (like negative age) to prove our validation works
        df.loc[0, 'age'] = -5  
        df.loc[1, 'credit_score'] = 9000 
        
        return df

    def validate_and_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        The Core Pipeline: 
        1. Checks if data is valid (Validation)
        2. Calculates risk score (Transformation)
        """
        logging.info("Starting validation and scoring...")
        valid_records = []
        
        for _, row in df.iterrows():
            try:
                # Turn the row into an Applicant object. 
                # If data is bad, this line will crash (raise an error) immediately.
                applicant = Applicant(**row.to_dict())
                
                # If we get here, data is good. Calculate risk.
                risk_score = self._calculate_risk_logic(applicant)
                
                # Save the results
                result = row.to_dict()
                result['risk_score'] = risk_score
                result['status'] = 'Valid'
                valid_records.append(result)
                
            except ValidationError as e:
                # If data was bad, log it as a warning but don't crash the app.
                logging.warning(f"Rejected Applicant ID {row['applicant_id']}: {e}")
                
        return pd.DataFrame(valid_records)

    def _calculate_risk_logic(self, app: Applicant) -> int:
        """
        Simple Actuarial Logic:
        - Young drivers (<25) are higher risk
        - Low credit (<600) is higher risk
        - Past claims increase risk significantly
        """
        score = 0
        if app.age < 25: score += 20
        if app.credit_score < 600: score += 30
        score += (app.claims_history * 20)
        return score

# --- STEP 4: EXECUTION ---
if __name__ == "__main__":
    engine = RiskEngine()
    
    # 1. Generate Raw Data
    raw_df = engine.generate_data(100)
    
    # 2. Process Data (Validate & Score)
    processed_df = engine.validate_and_score(raw_df)
    
    # 3. Show Results
    logging.info(f"Successfully processed {len(processed_df)} valid records.")
    print(processed_df.head())
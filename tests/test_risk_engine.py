import sys
import os
import pytest
from pydantic import ValidationError

# This allows us to import 'src' even though it's in a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from risk_engine import RiskEngine, Applicant

# --- TEST 1: BUSINESS LOGIC ---
def test_risk_calculation():
    """Does the math work correctly?"""
    engine = RiskEngine()
    
    # Create a dummy user: 20 years old (Risk +20), Bad Credit (Risk +30)
    app = Applicant(applicant_id=1, name="Test", age=20, credit_score=500, claims_history=0)
    
    score = engine._calculate_risk_logic(app)
    
    # Expected: 20 + 30 = 50
    assert score == 50

# --- TEST 2: DATA VALIDATION ---
def test_invalid_data_rejection():
    """Does the system block invalid data?"""
    # Trying to create a user with Age -5 should cause a ValidationError
    with pytest.raises(ValidationError):
        Applicant(applicant_id=1, name="Test", age=-5, credit_score=700, claims_history=0)
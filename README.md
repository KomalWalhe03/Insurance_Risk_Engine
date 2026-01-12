# Insurance Risk Engine

## Overview
A Python-based data processing tool that generates realistic synthetic insurance data and calculates risk scores based on actuarial rules. The engine processes 10,000 records per run and includes automated data quality checks to detect anomalies.

## Key Features
- **Synthetic Data Pipeline**: Uses `Faker` and `NumPy` to generate realistic datasets, including PII (names, addresses) and behavioral metrics (credit scores, claim history).
- **Risk Scoring Algorithm**: Implements weighted logic to assess risk based on Applicant Age, Credit Score, and Claims History.
- **Anomaly Detection**: Automatically flags data integrity issues, such as negative ages (data entry errors) or impossible credit scores (potential fraud).

## Tech Stack
- **Python**: Core logic and scripting.
- **Pandas**: Data manipulation and DataFrame management.
- **NumPy**: Random distribution generation for statistical simulation.
- **Faker**: Synthetic entity generation.

## How to Run
1. Install dependencies: 
   ```bash
   pip install -r requirements.txt
   ```

2. Run the engine:

   ```Bash

   python src/risk_engine.py
   ```


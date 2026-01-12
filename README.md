# Insurance Risk Engine

## Overview
A production-grade data processing tool that generates realistic synthetic insurance data, validates it against strict schemas, and calculates risk scores based on actuarial rules. 

Unlike simple scripts, this project demonstrates **MLOps best practices** including robust data validation, automated logging for observability, and unit testing for logic verification.

## Key Features
- **Strict Data Validation**: Uses **Pydantic** to enforce data quality schemas, automatically rejecting invalid records (e.g., negative ages, impossible credit scores) before they corrupt the pipeline.
- **Observability & Logging**: Replaces standard print statements with professional **Logging**, tracking process execution and data quality issues in a persistent `risk_engine.log` file.
- **Synthetic Data Pipeline**: Uses `Faker` and `NumPy` to generate realistic PII (names) and behavioral metrics (claims history).
- **Automated Unit Testing**: Includes `pytest` suite to verify business logic and validation rules before deployment.

## Tech Stack
- **Core Logic**: Python 3.12+
- **Data Manipulation**: Pandas, NumPy
- **Validation**: Pydantic (MLOps Standard)
- **Testing**: Pytest
- **Data Generation**: Faker

## Project Structure
```text
├── src/
│   └── risk_engine.py       # Main application logic (Validation + Scoring)
├── tests/
│   └── test_risk_engine.py  # Unit tests for logic and validation
├── data/                    # Storage for output CSVs
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

## How to Run
1. Install Dependencies
```Bash

pip install -r requirements.txt
```
2. Run the Test Suite (Verify Logic)
Before processing data, ensure the logic is sound by running the unit tests:
```Bash

pytest tests/
```
3. Run the Risk Engine
Generate data, validate it, and calculate scores. Logs will be saved to risk_engine.log.
```Bash

python src/risk_engine.py
```

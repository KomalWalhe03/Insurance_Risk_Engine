install:
	pip install -r requirements.txt

run:
	python src/risk_engine.py

test:
	pytest tests/

clean:
	rm -f risk_engine.log
	rm -rf __pycache__
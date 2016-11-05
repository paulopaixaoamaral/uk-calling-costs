install:
	pip install -r requirements.txt

run:
	python main.py

test:
	python -m unittest discover -s tests -p "*_test.py"
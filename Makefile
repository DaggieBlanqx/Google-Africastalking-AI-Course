
PYTHON := python3
PIP := $(PYTHON) -m pip

install:
	$(PIP) install -r requirements.txt

freeze:
	$(PIP) freeze > requirements.txt

dev:
	FLASK_ENV=development $(PYTHON) app.py

run:
	$(PYTHON) app.py

tunnel:
	ngrok http 9000

lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .





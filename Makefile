.PHONY: venv install backend frontend lint dev clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

venv:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -r requirements.txt

backend:
	$(VENV)/bin/uvicorn backend.main:app --reload --port 8000

frontend:
	PYTHONPATH=. $(VENV)/bin/streamlit run frontend/app.py --server.port 8501

lint:
	$(VENV)/bin/ruff check .

dev:
	@echo "Запусти 'make backend' и 'make frontend' в двух терминалах"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf $(VENV)

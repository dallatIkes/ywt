PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python

HOST = 0.0.0.0
PORT = 8000

.DEFAULT_GOAL := help

.PHONY: help init db-clean db-seed run test verbose_test lint format

help:
	@echo "Usage:"
	@echo "  make init           # Create virtual environment and install dependencies"
	@echo "  make db-clean       # Clean database"
	@echo "  make db-seed        # Seed database with test data"
	@echo "  make run            # Run the FastAPI server"
	@echo "  make test           # Run tests"
	@echo "  make verbose_test   # Run tests with verbose output"
	@echo "  make lint           # Check code style with flake8"
	@echo "  make format         # Format code with black"
	@echo ""

init:
	@echo "============================================"
	@echo "🐍 Python venv + dependencies setup"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

db-clean:
	@echo "============================================"
	@echo "🧹 Cleaning database"
	@echo "--------------------------------------------"
	@echo ""
	rm -rf ./app/db/*.db

db-seed:
	@echo "============================================"
	@echo "🌱 Seeding database with test data"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m scripts.seed_db

run:
	@echo "============================================"
	@echo "🚀 Starting FastAPI backend"
	@echo ""
	@echo "URL: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m uvicorn main:app --reload --host $(HOST) --port $(PORT)

test:
	@echo "============================================"
	@echo "🧪 Running tests"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m pytest

verbose_test:
	@echo "============================================"
	@echo "🧪 Running tests (verbose mode)"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m pytest -vv

lint:
	@echo "============================================"
	@echo "🔍 Checking code style with flake8"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m flake8 --max-line-length=120 --ignore=E203,E501,W503 app/ tests/ scripts/ main.py

format:
	@echo "============================================"
	@echo "🎨 Formatting code with black"
	@echo "--------------------------------------------"
	@echo ""
	$(PYTHON_VENV) -m black app/ tests/ scripts/ main.py
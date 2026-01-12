# ============================================
# Development Makefile
# ============================================
BACKEND_DIR=backend
VENV_DIR=$(BACKEND_DIR)/.venv
VENV_PYTHON=$(VENV_DIR)/bin/python
BACKEND_CMD=$(VENV_PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
FRONTEND_DIR=frontend
FRONTEND_CMD=npm run dev

.DEFAULT_GOAL := help

.PHONY: help venv back front dev freeze db-clean db-seed back-deps front-deps deps

# -----------------------
# HELP
# -----------------------
help:
	@echo ""
	@echo "============================================"
	@echo "📖 Available commands"
	@echo "============================================"
	@echo ""
	@echo "make venv       → Check Python virtual environment"
	@echo "make back       → Start FastAPI backend"
	@echo "make front      → Start SvelteKit frontend"
	@echo "make dev        → Start backend and frontend together"
	@echo "make freeze     → Update requirements.txt from venv"
	@echo "make db-clean   → Clean database"
	@echo "make db-seed    → Seeding database with test data"
	@echo "make back-deps  → Install backend dependencies"
	@echo "make front-deps → Install frontend dependencies"
	@echo "make deps       → Install both backend and frontend dependencies"
	@echo ""
	@echo "👉 Example:"
	@echo "   make dev"
	@echo ""

# -----------------------
# VENV
# -----------------------
venv:
	@echo "============================================"
	@echo "🐍 Checking Python virtual environment"
	@echo "--------------------------------------------"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "❌ Virtual environment not found."; \
		echo "👉 Run: python -m venv $(VENV_DIR)"; \
		exit 1; \
	fi
	@echo "✅ Virtual environment detected at $(VENV_DIR)/"
	@echo "👉 Python executable: $(VENV_PYTHON)"
	@echo ""
	@echo "💡 To activate the venv, run: source $(VENV_DIR)/bin/activate"

# -----------------------
# BACKEND
# -----------------------
back: venv
	@echo "============================================"
	@echo "🚀 Starting FastAPI backend"
	@echo "--------------------------------------------"
	@echo "👉 URL: http://localhost:8000"
	@echo "👉 Docs: http://localhost:8000/docs"
	@echo ""
	cd $(BACKEND_DIR) && .venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

back-deps: venv
	@echo "============================================"
	@echo "📦 Installing backend dependencies"
	@echo "--------------------------------------------"
	$(VENV_PYTHON) -m pip install -r $(BACKEND_DIR)/requirements.txt
	@echo "✅ Backend dependencies installed"

# -----------------------
# FRONTEND
# -----------------------
front:
	@echo "============================================"
	@echo "🎨 Starting SvelteKit frontend"
	@echo "--------------------------------------------"
	@echo "👉 Directory: $(FRONTEND_DIR)"
	@echo "👉 URL: http://localhost:5173"
	@echo ""
	cd $(FRONTEND_DIR) && $(FRONTEND_CMD)

front-deps:
	@echo "============================================"
	@echo "📦 Installing frontend dependencies"
	@echo "--------------------------------------------"
	cd $(FRONTEND_DIR) && npm install
	@echo "✅ Frontend dependencies installed"

# -----------------------
# INSTALL ALL DEPENDENCIES
# -----------------------
deps: back-deps front-deps
	@echo "============================================"
	@echo "✅ All dependencies installed"
	@echo "============================================"

# -----------------------
# DEVELOPMENT (backend + frontend)
# -----------------------
dev: venv
	@echo "============================================"
	@echo "🔥 Launching development environment"
	@echo "--------------------------------------------"
	@echo "👉 Backend: FastAPI"
	@echo "👉 Frontend: SvelteKit"
	@echo "👉 Press Ctrl+C to stop everything"
	@echo "============================================"
	@echo ""
	@bash -c '\
		set -m; \
		cd $(BACKEND_DIR) && $(BACKEND_CMD) & \
		BACK_PID=$$!; \
		cd ../$(FRONTEND_DIR) && $(FRONTEND_CMD) & \
		FRONT_PID=$$!; \
		trap "echo \"Stopping dev environment...\"; kill -TERM $$BACK_PID $$FRONT_PID 2>/dev/null; exit 0" INT TERM; \
		wait \
	'

# -----------------------
# FREEZE DEPENDENCIES
# -----------------------
freeze: venv
	@echo "============================================"
	@echo "📦 Freezing Python dependencies"
	@echo "--------------------------------------------"
	@echo "👉 Writing to $(BACKEND_DIR)/requirements.txt"
	@echo ""
	$(VENV_PYTHON) -m pip freeze > $(BACKEND_DIR)/requirements.txt
	@echo "✅ requirements.txt updated"

# -----------------------
# DATABASE
# -----------------------
db-clean:
	@echo "============================================"
	@echo "🧹 Cleaning database"
	@echo "--------------------------------------------"
	@if [ -f "$(BACKEND_DIR)/test.db" ]; then \
		rm $(BACKEND_DIR)/test.db && echo "✅ test.db removed"; \
	else \
		echo "ℹ️ test.db not found"; \
	fi
	@echo ""

db-seed: venv
	@echo "============================================"
	@echo "🌱 Seeding database with test data"
	@echo "--------------------------------------------"
	@echo ""
	cd $(BACKEND_DIR) && .venv/bin/python -m scripts.seed_db
	@echo "✅ Database seeded"
# ============================================
# Development Makefile
# ============================================
VENV_PYTHON=.venv/bin/python
BACKEND_CMD=.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
FRONTEND_DIR=frontend
FRONTEND_CMD=npm run dev

.DEFAULT_GOAL := help

.PHONY: help venv back front dev freeze db-clean db-seed

help:
	@echo ""
	@echo "============================================"
	@echo "📖 Available commands"
	@echo "============================================"
	@echo ""
	@echo "make venv     → Check Python virtual environment"
	@echo "make back     → Start FastAPI backend"
	@echo "make front    → Start SvelteKit frontend"
	@echo "make dev      → Start backend and frontend together"
	@echo "make freeze   → Update requirements.txt from venv"
	@echo "make db-clean → Clean database"
	@echo "make db-seed  → Seeding database with test data"
	@echo ""
	@echo "👉 Example:"
	@echo "   make dev"
	@echo ""

venv:
	@echo "============================================"
	@echo "🐍 Checking Python virtual environment"
	@echo "--------------------------------------------"
	@if [ ! -d ".venv" ]; then \
		echo "❌ Virtual environment not found."; \
		echo "👉 Run: python -m venv .venv"; \
		exit 1; \
	fi
	@echo "✅ Virtual environment detected at .venv/"
	@echo "👉 Python executable: $(VENV_PYTHON)"
	@echo ""

back: venv
	@echo "============================================"
	@echo "🚀 Starting FastAPI backend"
	@echo "--------------------------------------------"
	@echo "👉 URL: http://localhost:8000"
	@echo "👉 Docs: http://localhost:8000/docs"
	@echo ""
	$(BACKEND_CMD)

front:
	@echo "============================================"
	@echo "🎨 Starting SvelteKit frontend"
	@echo "--------------------------------------------"
	@echo "👉 Directory: $(FRONTEND_DIR)"
	@echo "👉 URL: http://localhost:5173"
	@echo ""
	cd $(FRONTEND_DIR) && $(FRONTEND_CMD)

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
		$(BACKEND_CMD) & \
		BACK_PID=$$!; \
		cd $(FRONTEND_DIR) && $(FRONTEND_CMD) & \
		FRONT_PID=$$!; \
		trap "echo \"Stopping dev environment...\"; kill -TERM $$BACK_PID $$FRONT_PID 2>/dev/null; exit 0" INT TERM; \
		wait \
	'

freeze: venv
	@echo "============================================"
	@echo "📦 Freezing Python dependencies"
	@echo "--------------------------------------------"
	@echo "👉 Writing to requirements.txt"
	@echo ""
	$(VENV_PYTHON) -m pip freeze > requirements.txt
	@echo "✅ requirements.txt updated"
	@echo ""

db-clean:
	@echo "============================================"
	@echo "🧹 Cleaning database"
	@echo "--------------------------------------------"
	@if [ -f "test.db" ]; then \
		rm test.db && echo "✅ test.db removed"; \
	else \
		echo "ℹ️ test.db not found"; \
	fi
	@echo ""

db-seed: venv
	@echo "============================================"
	@echo "🌱 Seeding database with test data"
	@echo "--------------------------------------------"
	@echo ""
	$(VENV_PYTHON) -m scripts.seed_db
	@echo "✅ Database seeded"
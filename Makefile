# ============================================
# Development Makefile
# ============================================

VENV_PYTHON=.venv/bin/python
BACKEND_CMD=$(VENV_PYTHON) run_server.py
FRONTEND_DIR=frontend
FRONTEND_CMD=npm run dev

.DEFAULT_GOAL := help

.PHONY: help venv back front dev freeze

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

dev: venv
	@echo "============================================"
	@echo "🔥 Launching development environment"
	@echo "--------------------------------------------"
	@echo "👉 Backend: FastAPI"
	@echo "👉 Frontend: SvelteKit"
	@echo "👉 Press Ctrl+C to stop everything"
	@echo "============================================"
	@echo ""
	$(BACKEND_CMD) & \
	cd $(FRONTEND_DIR) && $(FRONTEND_CMD)

freeze: venv
	@echo "============================================"
	@echo "📦 Freezing Python dependencies"
	@echo "--------------------------------------------"
	@echo "👉 Writing to requirements.txt"
	@echo ""
	$(VENV_PYTHON) -m pip freeze > requirements.txt
	@echo "✅ requirements.txt updated"
	@echo ""

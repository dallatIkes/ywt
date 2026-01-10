# YWT (Yo Watch This!)

A simple web app to share cool videos with your friends.

This project uses:
- **FastAPI** for the backend
- **SvelteKit** for the frontend
- A **Makefile** to manage development commands easily

---

## Prerequisites

- Python 3.10+
- Node.js & npm
- make
- A Unix-like environment (Linux / macOS)

---

## Project structure

- backend: FastAPI app (entrypoint: main:app)
- frontend: SvelteKit app
- test.db: SQLite database (created at runtime)
- Makefile: development commands

---

## How to run the project

### 1. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Run backend only

```bash
make back
```

- Backend URL: http://localhost:8000
- API docs: http://localhost:8000/docs

---

### 3. Run frontend only

```bash
make front
```

- Frontend URL: http://localhost:5173

---

### 4. Run full development environment (recommended)

This starts **backend and frontend together**:

```bash
make dev
```

Press **Ctrl+C** to stop everything.

---

## Database commands

Clean the database:

```bash
make db-clean
```

Seed the database with test data:

```bash
make db-seed
```

---

## Other useful commands

Update requirements.txt from the virtual environment:

```bash
make freeze
```

Display all available commands:

```bash
make help
```

---

## Notes

- Authentication uses OAuth2 with JWT tokens.
- The frontend communicates with the backend via HTTP API.
- This project is intended for development usage.

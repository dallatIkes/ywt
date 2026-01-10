# YWT (Yo Watch This!)

A simple web application to share cool videos with your friends.

## Prerequisites

- Python 3.10+
- make installed on your system

## How to run the project

### 1. Install dependencies

Using the Makefile (recommended):

```bash
make install
```

Or manually:

```bash
pip install -r requirements.txt
```

### 2. Run the backend server

Using the Makefile:

```bash
make run
```

Or manually:

```bash
python3 run_server.py
```

The API will be available at:

http://localhost:8000

### 3. API documentation

Once the server is running, you can access the automatic API documentation at:

- Swagger UI  
  http://localhost:8000/docs

- ReDoc  
  http://localhost:8000/redoc

## Notes

- Authentication is handled using OAuth2 with JWT tokens.
- A local SQLite database (test.db) is used by default.

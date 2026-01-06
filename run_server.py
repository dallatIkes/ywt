import uvicorn

from main import app

def run_server():
    uvicorn.run("main:app", port=8000, reload=True)

if __name__ == "__main__":
    run_server()
import uvicorn

from main import app

def run_server():
    uvicorn.run(app, port=8000)

if __name__ == "__main__":
    run_server()
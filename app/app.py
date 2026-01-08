import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "This is a morloc app"}

def run_app(host = "0.0.0.0", port = 8000):
    uvicorn.run(app, host=host, port=port)
















#

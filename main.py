import uvicorn
import logging
from fastapi import FastAPI

from endpoints import agent, skillsets

app = FastAPI()

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "Welcome to the GitHub agent API!"}

app.include_router(agent.router)
app.include_router(skillsets.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
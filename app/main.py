from fastapi import FastAPI
from app.routes.thread import router as thread_router

app = FastAPI(title="Parallel Processing Final Project")

app.include_router(thread_router)


@app.get("/")
def home():
    return {
        "message": "Parallel Processing Final Project is running"
    }
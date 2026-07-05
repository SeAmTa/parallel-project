from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.thread import router as thread_router
from app.routes.process import router as process_router
from app.routes.stream import router as stream_router

app = FastAPI(title="Parallel Processing Final Project")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(thread_router)
app.include_router(process_router)
app.include_router(stream_router)


@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse(
        "app/templates/index.html",
        media_type="text/html"
    )
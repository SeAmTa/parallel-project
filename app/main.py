from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.thread import router as thread_router
from app.routes.process import router as process_router
from app.routes.stream import router as stream_router

app = FastAPI(title="Parallel Processing Final Project")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(thread_router)

app.include_router(process_router)

app.include_router(stream_router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )
import time
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.dispatcher import run_thread_scenario

router = APIRouter(
    prefix="/stream",
    tags=["Live Stream"]
)


def event_generator(method: str, section: int, scenario: int):
    if method != "thread":
        yield f"data: {json.dumps({'type': 'error', 'message': 'Only thread is supported now'})}\n\n"
        return

    result = run_thread_scenario(section, scenario)

    if "error" in result:
        yield f"data: {json.dumps({'type': 'error', 'message': result['error']})}\n\n"
        return

    yield f"data: {json.dumps({'type': 'title', 'message': result['title']})}\n\n"
    time.sleep(0.3)

    for line in result["output"]:
        yield f"data: {json.dumps({'type': 'log', 'message': line})}\n\n"
        time.sleep(0.25)

    yield f"data: {json.dumps({'type': 'explanation', 'message': result['explanation']})}\n\n"
    yield f"data: {json.dumps({'type': 'done', 'message': 'Execution finished'})}\n\n"


@router.get("/{method}/{section}/{scenario}")
def stream_api(method: str, section: int, scenario: int):
    return StreamingResponse(
        event_generator(method, section, scenario),
        media_type="text/event-stream"
    )
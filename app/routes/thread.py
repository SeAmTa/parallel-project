from fastapi import APIRouter

from app.services.dispatcher import run_thread_scenario

router = APIRouter(
    prefix="/api/thread",
    tags=["Thread"]
)


@router.get("/{section}/{scenario}")
def thread_api(
        section: int,
        scenario: int
):
    return run_thread_scenario(
        section,
        scenario
    )
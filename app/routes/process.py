from fastapi import APIRouter

from app.services.dispatcher import run_process_scenario

router = APIRouter(
    prefix="/api/process",
    tags=["Process"]
)


@router.get("/{section}/{scenario}")
def process_api(
        section: int,
        scenario: int
):
    return run_process_scenario(
        section,
        scenario
    )
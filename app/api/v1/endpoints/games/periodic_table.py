from fastapi import APIRouter
from fastapi import Request
from app.schemas.periodic_table_schema import ElementSchema
from app.services import periodic_table_service as service

router = APIRouter(prefix="/periodic-table")


@router.get("/elements", response_model=list[ElementSchema])
def get_elements():
    """Get all elements from the periodic table."""
    elements = service.get_all_elements()
    return elements


@router.get("/elements/{number}/stream", response_model=str)
async def get_element_voice(number: int, request: Request):
    """Get the voice URL for a specific element."""
    file_path = service.get_audio_path(f"elements/{number}.mp3")
    range_header = request.headers.get("range")
    return service.stream_audio_response(file_path, range_header)

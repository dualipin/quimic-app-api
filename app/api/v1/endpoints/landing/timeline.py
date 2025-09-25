from fastapi import APIRouter, Request
from app.services import audio_service as service

router = APIRouter()


@router.get("/timeline/{number}/stream", response_model=str)
async def get_element_voice(number: int, request: Request):
    """Get the voice URL for a specific element."""
    file_path = service.get_audio_path(f"timeline/{number}.mp3")
    range_header = request.headers.get("range")
    return service.stream_audio_response(file_path, range_header)

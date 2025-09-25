from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from typing import Generator, Optional
from pathlib import Path


def get_audio_path(filename: str) -> str:
    path = Path("app") / "statics" / "audio" / filename
    if not Path.exists(path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return path


def parse_range(range_header: str, file_size: int) -> tuple[int, int]:
    # "bytes=1000-" or "bytes=1000-2000"
    bytes_unit, byte_range = range_header.strip().split("=")
    start, end = byte_range.split("-")
    start = int(start)
    end = int(end) if end else file_size - 1
    return start, end


def iter_file(file_path: str, start: int = 0) -> Generator[bytes, None, None]:
    with open(file_path, "rb") as f:
        f.seek(start)
        while chunk := f.read(1024 * 1024):
            yield chunk


def stream_audio_response(
    file_path: str, range_header: Optional[str]
) -> StreamingResponse:
    file_size = Path(file_path).stat().st_size

    if range_header:
        start, end = parse_range(range_header, file_size)
        length = end - start + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            "Content-Type": "audio/mpeg",
        }

        return StreamingResponse(
            iter_file(file_path, start), status_code=206, headers=headers
        )

    headers = {
        "Content-Length": str(file_size),
        "Accept-Ranges": "bytes",
        "Content-Type": "audio/mpeg",
    }

    return StreamingResponse(iter_file(file_path), status_code=200, headers=headers)

from typing import BinaryIO
import gzip

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from settings import tags_metadata
from routes.games import router as games_router
from routes.companies import router as companies_router


def read_in_chunks(file_object: BinaryIO, chunk_size: int) -> bytes:
    while True:
        chunk = file_object.read(chunk_size)
        if not chunk:
            break
        yield chunk


def compress_file(file_path: str, chunk_size: int) -> bytes:
    with open(file_path, "rb") as file:
        for chunk in read_in_chunks(file, chunk_size):
            yield gzip.compress(chunk)


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(games_router)
app.include_router(companies_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/download/")
async def download():
    file_path = "common.rpf"
    chunk_size = 8192
    media_type = "application/gzip"
    headers = {
        "Content-Disposition": f"filename={file_path}"
    }
    return StreamingResponse(
        compress_file(file_path, chunk_size),
        headers=headers,
        media_type=media_type
    )

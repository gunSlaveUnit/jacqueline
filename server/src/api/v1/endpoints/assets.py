from typing import List

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from starlette import status
from starlette.responses import Response, FileResponse

from server.src.core.controllers.assets import AssetsController
from server.src.core.models.game import Game
from server.src.core.settings import ASSETS_ROUTER_PREFIX, GAMES_ASSETS_PATH, GAMES_ASSETS_HEADER_DIR
from server.src.core.utils.db import get_db

router = APIRouter(prefix=ASSETS_ROUTER_PREFIX)


@router.get('/header/')
async def download_header(game_id: int,
                          db=Depends(get_db)):
    """Returns an image for the header section of the game."""

    game = await Game.by_id(db, game_id)

    searching_directory = GAMES_ASSETS_PATH.joinpath(game.directory, GAMES_ASSETS_HEADER_DIR)

    files = list(searching_directory.glob('*'))

    if files and len(files) != 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Multiple files found but one is required"
        )

    if not files or not files[0].is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )

    return FileResponse(
        searching_directory.joinpath(files[0].name),
        headers={"Content-Disposition": f"filename={files[0].name}"},
        media_type="image/webp"
    )


@router.post('/header/')
async def upload_header(game_id: int,
                        file: UploadFile,
                        assets_controller: AssetsController = Depends(AssetsController)):
    """Uploads a header game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    await assets_controller.upload_header(game_id, file)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/capsule/')
async def download_capsule(game_id: int):
    """Returns an image for the capsule section of the game."""

    pass


@router.post('/capsule/')
async def upload_capsule(file: UploadFile):
    """Uploads a capsule game section file to the server.
    If exists, will be overwritten.
    Associated game will become unpublished.
    """

    pass


@router.get('/screenshots/')
async def screenshots_info(game_id: int):
    """Returns the names of the screenshot files.
    If "filename" query param was provided, returns a file.
    """

    pass


@router.post('/screenshots/')
async def upload_screenshots(game_id: int):
    """Uploads screenshots to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    pass


@router.get('/trailers/')
async def trailers_info(filename: str | None = None):
    """Returns the names of the trailers files.
    If "filename" query param was provided, returns a file.
    """
    pass


@router.post('/trailers/')
async def upload_trailers(game_id: int,
                          files: List[UploadFile],
                          assets_controller: AssetsController = Depends(AssetsController)):
    """Uploads trailers to the server.
    All will be overwritten.
    Associated game will become unpublished.
    """

    await assets_controller.upload_trailers(game_id, files)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

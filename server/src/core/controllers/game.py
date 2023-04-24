import uuid

from fastapi import Depends, HTTPException
from starlette import status

from server.src.core.logic.company import CompanyLogic
from server.src.core.logic.game import GameLogic
from server.src.core.logic.game_status import GameStatusLogic
from server.src.core.models.game import Game
from server.src.core.models.user import User
from server.src.core.settings import GAMES_ASSETS_PATH, GameStatusType
from server.src.core.utils.db import get_db
from server.src.schemas.game import GameCreateSchema


class GameController:
    def __init__(self, db=Depends(get_db)):
        self.db = db
        self.game_logic = GameLogic(db)
        self.company_logic = CompanyLogic(db)
        self.game_status_logic = GameStatusLogic(db)

    async def items(self):
        items = await self.game_logic.items()
        return items.all()

    async def create(self, game_data: GameCreateSchema, current_user: User):
        potentially_not_existing_company = await self.company_logic.item_by_owner(current_user.id)

        if potentially_not_existing_company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current user does not have a registered company"
            )

        if not potentially_not_existing_company.is_approved:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Information about the user's company may be inaccurate. Creating is temporarily disabled"
            )

        game = Game(**vars(game_data))
        game.owner_id = current_user.id

        not_send_status = await self.game_status_logic.item_by_title(GameStatusType.NOT_SEND)
        game.status_id = not_send_status.id

        new_directory_uuid = str(uuid.uuid4())
        assets_directory = GAMES_ASSETS_PATH.joinpath(new_directory_uuid)
        assets_directory.mkdir(parents=True)
        game.directory = new_directory_uuid

        return await self.game_logic.create(game)

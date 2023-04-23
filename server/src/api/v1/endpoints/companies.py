from fastapi import APIRouter, Depends

from server.src.core.controllers.company import CompanyController
from server.src.core.models.user import User
from server.src.core.settings import Tags, COMPANIES_ROUTER_PREFIX
from server.src.core.utils.auth import get_current_user
from server.src.schemas.company import CompanyCreateSchema

router = APIRouter(prefix=COMPANIES_ROUTER_PREFIX, tags=[Tags.COMPANIES])


@router.get('/')
async def items(company_controller: CompanyController = Depends(CompanyController)):
    return await company_controller.items()


@router.post('/')
async def create(new_company_data: CompanyCreateSchema,
                 current_user: User = Depends(get_current_user),
                 company_controller: CompanyController = Depends(CompanyController)):
    return await company_controller.create(new_company_data, current_user)

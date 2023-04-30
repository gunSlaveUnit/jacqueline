from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from server.src.core.models.company import Company
from server.src.core.models.user import User
from server.src.core.settings import RoleType, templates
from server.src.core.utils.auth import GetCurrentUser
from server.src.core.utils.db import get_db

router = APIRouter(prefix='/companies')


@router.get('/', response_class=HTMLResponse)
async def items(request: Request,
                current_user: User = Depends(GetCurrentUser(scopes=(RoleType.ADMIN,))),
                db: Session = Depends(get_db)):
    companies = db.query(Company).order_by(Company.is_approved, desc(Company.created_at)).all()
    companies = [c.dict() for c in companies]

    return templates.TemplateResponse("companies.html", {"request": request, "companies": companies})

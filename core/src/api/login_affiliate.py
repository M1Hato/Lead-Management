from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.cfg.auth_utils import create_access_token
from src.database import get_async_session
from src.models.affiliates_model import AffiliatesModel
from src.models.offers_model import OffersModel
from src.models.leads_model import LeadModel
from src.schemas.login_shemas import LoginSchema

router = APIRouter(
    prefix="/login",
    tags=["login"],
)

@router.post("/")
async def login_affiliate(
        data: LoginSchema,
        db: AsyncSession = Depends(get_async_session)
):
    affiliate_id = data.affiliate_id
    query = select(AffiliatesModel).where(AffiliatesModel.id == affiliate_id)
    result = await db.execute(query)
    affiliate = result.scalars().first()

    if not affiliate:
        raise HTTPException(status_code=404, detail="Affiliate not found")

    token_data = {"id": str(affiliate.id)}
    access_token = create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}